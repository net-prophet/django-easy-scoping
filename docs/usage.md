---
id: usage
title: Usage
---

Example Django Model located at
[bottom of page](https://net-prophet.github.io/django-easy-scoping/docs/usage.html#example-django-models).

A scope enables easier database filtering in Django. A user can specify one or more
filters for a scope and then simply use the scope to search the database, rather
than making long filter calls. Additionally, users can chain together scopes to
combine the filters used by both.

Aggregates also allows for simpler database queries. By encompassing Django filter,
annotation, and aggregation calls in a single aggregate, the user can more easily
extract, view, and analyze iheir data.

## Basic Usage

Some notes on using DjangoEasyScoping:
* Only `models.py` files need to import DjangoEasyScoping (ScopingMixin,
ScopingQuerySet). Therefore, a different file or shell does not need to import
DjangoEasyScoping to scope and aggregate a model's objects.
* However, unless the scoping is performed within a `models.py` file, then the
file or shell still needs to import the model that has implemented scoping.
* Use regular Django methods to create objects (see
[here](https://docs.djangoproject.com/en/2.0/topics/db/queries/#creating-objects)
or
[here](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#django.db.models.query.QuerySet.create))
that will be scoped:
```python
<Object Type>.objects.create(<feature1>=<value1>, ...)
```

### Scoping

Here are some simple examples just to see the syntax. 

[Register the scope](https://net-prophet.github.io/django-easy-scoping/docs/api.html#register-scope)
`models.py`:
```python
<Object Type>.register_scope('<scope name>', <filtering method(s)>)
```
The filtering call will likely take forms such as:
```python
# Single filter
lambda qs: qs.filter(<feature>=<value>)

# Or multiple filters
lambda qs: qs.filter(<feature1>=<value1>).filter(<feature2>=<value2>).<...>

# Or taking paramters
lambda qs, param1, param2, <...>: qs.filter(<feature1>=param1).filter(<feature2>=param2).<...>
```

For example, for
[`widgets/models.py`](https://net-prophet.github.io/django-easy-scoping/docs/usage.html#widgets-modelspy)
```python
Widget.register_scope('blue', lambda qs: qs.filter(color='blue'))
```
This registers a scope named `blue`, which when invoked, filters for Widget objects
whose color is `blue`.

Using a scope will return all objects with the To filter with a scope, use the following syntax:
```python
<Object Type>.objects.all().<scope name>()
```

For example,

Without easy scoping:
```python
Widget.objects.filter(color='blue')
```
With easy scoping:

```python
Widget.objects.all().blue()
```

### Chaining Scopes

Let's look at that same query where we chain these calls instead.

[Register the scopes](https://net-prophet.github.io/django-easy-scoping/docs/api.html#register-scope)
on `models.py`, calling `register_scope()` for each scope:
```python
Widget.register_scope('blue', lambda qs: qs.filter(color='blue'))
Widget.register_scope('small', lambda qs: qs.filter(size='small'))
Widget.register_scope('circle', lambda qs: qs.filter(shape='circle'))
```

Then, chain together multiple scope calls using the syntax:
```python
<Object Type>.objects.all().<scope1 name>().<scope2 name>().<...>
```

Without easy scoping:

```python
Widget.objects.filter(color='blue').filter(size='small').filter(shape='circle')
```

With easy scoping:

```python
Widget.objects.all().blue().small().circle()
```

### Registering Multiple Scopes Under the Same Name

If a scope (denote it by scope1) has already been registered under a name (say
`name1`), then another scope (scope2) can also be registered under the same name.
However, for scope2, the name passed to `register_scope()` is automatically preceded
by an underscore (`_name1`).

If three or more scopes (denoted scope1, scope2, scope3, ..., scopeN) are registered
under the same name (`name1`), then scope1 is unaffected: its name remains as
`name1`. scope2's name is preceded by an underscore: `_name1`. Then, scope3's name
becomes `_name1`, overriding scope2. Then, scope4's name becomes `_name1`, overriding
scope3, etc. So in the end, scope1's name is `name1`, and scopeN's name is `_name1`,
and scope2 through scopeN-1 are no longer accessible.

### Registering Multiple Aggregates Under the Same Name

If multiple aggregates are registered using the same name, then the behavior is the
same as when multiple scopes are registered under the same name.

### Using Other Queryset Methods

As the return value is a queryset, we can perform other django operations on
these querysets. The full list of operations can be found [here](https://docs.djangoproject.com/en/2.0/ref/models/querysets/).

To do so, use the syntax:
```python
<Object Type>.objects.all().<scope1 name>().<...>.<scopeN name>().<query set operation>()
```

Let's consider ordering these by their color in ascending
alphabetical order.

```python
Widget.objects.all().blue().small().circle().order_by('color')
```

## Real-World Usage

Consider the example models located at the
[bottom of the page](https://net-prophet.github.io/django-easy-scoping/docs/usage.html#example-django-models).
We have Customers who make many Purchases and Purchases that have many Widgets.

### Scoping Example

Register the scopes on `purchases/models.py`:
```python
from purchases/models import Purchase

MIDWEST = {
    'customer__state__in': ('Indiana', 'Illinois', 'Michigan', 'Ohio',
                            'Wisconsin', 'Iowa', 'Nebraska', 'Kansas',
                            'North Dakota', 'Minnesota', 'South Dakota', 'Missouri',)
}

# Create a scope for male customers from the Midwest with a mimimum age of 65
Purchase.register_scope('male_seniors_midwest', 
                        lambda qs: qs.filter(customer__age__gte=65)
                                     .filter(customer__gender__in='M')
                                     .filter(**MIDWEST))

# Create a scope for female customers from the Midwest with a mimimum age of 65
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

Note: To create a scope that accepts a parameter, use the method:
```python
lambda qs, parameter: qs.filter(<feature>=parameter)
```
within the `register_scope()` method.

Then, use the scope via:
```python
<Class Type>.objects.all().<scope name>(<parameter value to filter for>)
```

So now we have a scope for all customers of a particular gender, age, and
geographical region. 

```python
>>> Purchase.objects.all().male_seniors_midwest()
<ScopingQuerySet[<Purchase: PurchaseObjects(1)>, ...]

>>> Purchase.objects.all().female_seniors_midwest()
<ScopingQuerySet[<Purchase: PurchaseObjects(2)>, ...]

# Or using our gender-taking scope

>>> Purchase.objects.all().gender_seniors_midwest('M')
<ScopingQuerySet[<Purchase: PurchaseObjects(1)>, ...]
>>> Purchase.objects.all().gender_seniors_midwest('F')
<ScopingQuerySet[<Purchase: PurchaseObjects(2)>, ...]
```

### Aggregate Example

So now you've created some scopes and want a way to compare them!
Well, let's register some aggregates!

[Register the aggregates](https://net-prophet.github.io/django-easy-scoping/docs/api.html#register-aggregate)
on `models.py`:
```python
<Object Type>.register_aggregate('<aggregate name>', <filtering/annotating/aggratating/etc. method(s)>)
```
The filtering call will likely take forms such as:
```python
lambda qs: qs.filter(<feature>=<value>)
             .aggregate(<label1>=<aggregating function1>,
                        <label2>=<aggregating function2>,
                        <...>)

lambda qs: qs.filter(<feature1>=<value1>)
             .annotate(<label1>=<function1/value1>)
             .aggregate(<label2>=<aggregating function2>,
                        <label3>=<aggregating function3>,
                        <...>)
```
For example, on
[`purchases/models.py`](https://net-prophet.github.io/django-easy-scoping/docs/usage.html#purchases-modelspy):
```python
import pytz
from datetime import datetime as dt, timedelta as td
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
many days. We then
[annotate](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#annotate)
each purchase with the item count for it (my example
implementation randomly chooses between 1 and 9 items). Finally, we
[aggregate](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#aggregate)
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
Midwest, but when we do females are buying more items and returning much more
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
