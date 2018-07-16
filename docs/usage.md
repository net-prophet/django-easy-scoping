---
id: usage
title: Usage
---

Example Django Model located at bottom of page.



## Basic Usage

### Scoping

Here are some simple examples just to see the syntax.

Register the scope on `models.py`:
```python
Widget.register_scope('blue', lambda qs: qs.filter(color='blue'))
```

Without easy scoping:
```python
Widget.objects.filter(color='blue')
```
With easy scoping:

```python
Widget.a().blue()
```

### Chaining Scopes

Let's look at that same query where we chain these calls instead.

Register the scope on `models.py`:
```python
Widget.register_scope('blue', lambda qs: qs.filter(color='blue'))
Widget.register_scope('small', lambda qs: qs.filter(size='small'))
Widget.register_scope('circle', lambda qs: qs.filter(shape='circle'))
```

Without easy scoping:

```python
Widget.objects.filter(color='blue').filter(size='small').filter(shape='circle')
```

With easy scoping:

```python
Widget.a().blue().small().circle()
```
### Using Other Queryset Methods

As the return value is a queryset we can perform other django operations on
these querysets. The full list of operations can be found [here](https://docs.djangoproject.com/en/2.0/ref/models/querysets/).

Let's consider ordering these by their color in ascending
alphabetical order.

```python
Widget.a().blue().small().circle().order_by('color')
```

## Real-World Usage

Consider the example models located at the bottom of the page. We have Customers
who make many purchases and purchases who have many widgets.

### Scoping Example

Register the scopes on `purchases/models.py`:
```python
MIDWEST = {
    'customer__state__in': ('Indiana', 'Illinois', 'Michigan', 'Ohio',
                            'Wisconsin', 'Iowa', 'Nebraska', 'Kansas',
                            'North Dakota', 'Minnesota', 'South Dakota', 'Missouri',)
}

Purchase.register_scope('male_seniors_midwest', 
                        lambda qs: qs.filter(customer__age__gte=65)
                                     .filter(customer__gender__in='M')
                                     .filter(**MIDWEST))

Purchase.register_scope('female_seniors_midwest', 
                        lambda qs: qs.filter(customer__age__gte=65)
                                     .filter(customer__gender__in='F')
                                     .filter(**MIDWEST))

# We can also just make one scope for this age/region combo which takes a gender
Purchase.register_scope('gender_seniors_midwest', 
                        lambda qs, g: qs.filter(customer__age__gte=65)
                                        .filter(customer__gender__in=g)
                                        .filter(**MIDWEST))

# Let's also make one for millenials
Purchase.register_scope('gender_millenials_midwest', 
                        lambda qs, g: qs.filter(customer__age__gte=22)
                                        .filter(customer__age_lte=37)
                                        .filter(customer__gender__in=g)
                                        .filter(**MIDWEST))
```

So now we have a scope for all customers of a particular gender, age, and
geographical region. 

```python
>>> Purchase.objects.all().male_seniors_midwest()
<ScopingQuerySet[<Purchase: PurchaseObjects(1)>, ...]

>>> Purchase.objects.all().female_seniors_midwest()
<ScopingQuerySet[<Purchase: PurchaseObjects(2)>, ...]

# Or using our gender taking scope

>>> Purchase.objects.all().gender_seniors_midwest('M')
<ScopingQuerySet[<Purchase: PurchaseObjects(1)>, ...]
>>> Purchase.objects.all().gender_seniors_midwest('F')
<ScopingQuerySet[<Purchase: PurchaseObjects(2)>, ...]
```

### Aggregate Example

So now you've created some scopes and want a way to compare them!
Well, let's register some aggregates!

Register the aggregates on `purchases/models.py`:
```python
import pytz
from datetime import datetime as dt, timedelta as tdse.register_aggregate('data_last_days',
Purchase.register_aggregate('data_last_days',
                            lambda qs, days: qs.filter(sale_date__gte=dt.utcnow().replace(tzinfo=pytz.utc) - td(days=days))
                                               .annotate(item_count=Count('items')) 
                                               .aggregate(total_sales=Count('customer'),
                                                          average_items_per_sale=Avg('item_count'),
                                                          total_profit=Sum('profit'),
                                                          average_profit=Avg('profit'))
                            )
```

So here our aggregate is called on a queryset and takes as an argument a
number of days. It then returns a queryset of all purchases from today back that
many days. We then annotate each purchase with the item count for it (my example
implementation randomly chooses between 1 and 9 items). Finally, we aggregate
the total amount of sales over that date range, the average amount of items per
sale, our total profit, and our average profit.


```python
>>> Purchase.objects.all().data_last_days(100)
{'total_sales': 155, 'total_profit': 174403.49, 'average_profit': 1125.18, 'average_items_per_sale': 4.9}
```

### Putting it Together

Ok, so we've got some scopes and an aggregate function. Let's use them to
compare!

```python
>>> Purchase.objects.all().male_seniors_midwest().data_last_days(100)
{'total_sales': 6, 'total_profit': 5313.0, 'average_profit': 885.5, 'average_items_per_sale': 3.83}

>>> Purchase.objects.all().female_seniors_midwest().data_last_days(100)
{'total_sales': 5, 'total_profit': 6380.5, 'average_profit': 1276.1, 'average_items_per_sale': 5.6}
```

So, from our data it seems like we aren't selling many widgets to seniors in the
Northwest but when we do females are buying more items and returning much more
profit! 

Let's check out millenials.

```python
>>> Purchase.objects.all().gender_millenials_midwest('M').data_last_days(100)
{'total_sales': 18, 'total_profit': 24107.1, 'average_profit': 4017.84, 'average_items_per_sale': 7.98}
```

So male millenials in the midwest are buying a lot of our products!


## Example Django Models

These are the django models used in the examples above for your reference. You
can find these on our github aswell.


### widgets/models.py
```python

from django.db import models
from .options import COLORS, SIZES, SHAPES


class Widget(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(choices=COLORS, max_length=30)
    size = models.CharField(choices=SIZES, max_length=30)
    shape = models.CharField(choices=SHAPES, max_length=30)
```

### customers/models.py

```python
from django.db import models


class Customer(ScopingMixin, models.Model):
    name = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    age = models.IntegerField(blank=True)


    def get_purchases(self):
        from purchases.models import Purchase
        return Purchase.objects.all().filter(customer=self)
```

### purchases/models.py
```python
import pytz
import django
from django.db import models
from .state_regions import NORTHEAST, MIDWEST, SOUTH, WEST
from django.db.models import Sum, Count, Avg
from widgets.models import Widget
from customers.models import Customer
from datetime import datetime as dt, timedelta as td
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet


class Purchase(ScopingMixin, models.Model):
    items = models.ManyToManyField(Widget, blank=True)
    sale_date = models.DateTimeField(default=django.utils.timezone.now)
    sale_price = models.FloatField(default=0, blank=True)
    profit = models.FloatField(default=0, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    objects = ScopingQuerySet.as_manager()

    def get_items(self):
        return self.items.all()

    def get_item_count(self):
        return self.items.all().count()

    def get_sale_date(self):
        return self.sale_date

    def get_sale_price(self):
        return self.sale_price

    def get_cost(self):
        return round(self.items.aggregate(cost=Sum('cost'))['cost'], 2)

    def get_profit(self):
        return self.profit

    def set_sale_price(self):
        cost_plus_profit = 1.1
        cost = self.get_cost()
        self.sale_price = round(cost*cost_plus_profit, 2)

    def set_profit(self):
        profit_margin = .1
        cost = self.get_cost()
        self.profit = round(cost*profit_margin, 2)

    def save(self, *args, **kwargs):
        if self.id:
            for item in Widget.objects.filter(purchase=self):
                self.items.add(item)
                self.set_sale_price()
                self.set_profit()
                super(Purchase, self).save(*args, **kwargs)

        else:
            super(Purchase, self).save(*args, **kwargs)


Purchase.register_scope('male_seniors_midwest',
                        lambda qs: qs.filter(customer__age__gte=65)
                                     .filter(customer__gender__in='M')
                                     .filter(**MIDWEST)
                        )

Purchase.register_scope('female_seniors_midwest',
                        lambda qs: qs.filter(customer__age__gte=65)
                                     .filter(customer__gender__in='F')
                                     .filter(**MIDWEST)
                        )

Purchase.register_scope('gender_seniors_midwest',
                        lambda qs, g: qs.filter(customer__age__gte=65)
                                        .filter(customer__gender__in=g)
                                        .filter(**MIDWEST)
                        )

Purchase.register_aggregate('data_last_days',
                            lambda qs, days:
                            qs.filter(sale_date__gte=dt.utcnow().replace(tzinfo=pytz.utc) - td(days=days))
                            .annotate(item_count=Count('items'))
                            .aggregate(total_sales=Count('customer'),
                                       average_items_per_sale=Avg('item_count'),
                                       total_profit=Sum('profit'),
                                       average_profit=Avg('profit'))
                            )

Purchase.register_scope('senior',
                        lambda qs: qs.filter(customer__age__gte=65))
Purchase.register_scope('millenial',
                        lambda qs: qs.filter(customer__age__gte=22)
                                     .filter(customer__age__lte=37))

Purchase.register_scope('male',
                        lambda qs: qs.filter(customer__gender__in='M'))
Purchase.register_scope('female',
                        lambda qs: qs.filter(customer__gender__in='F'))

Purchase.register_scope('northeast',
                        lambda qs: qs.filter(**NORTHEAST))

Purchase.register_scope('midwest',
                        lambda qs: qs.filter(**MIDWEST))

Purchase.register_scope('southern',
                        lambda qs: qs.filter(**SOUTH))

Purchase.register_scope('western',
                        lambda qs: qs.filter(**WEST))
```
