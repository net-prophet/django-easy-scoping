---
id: api
title: API
---

## ScopingMixin

### register_scope
```python
register_scope(name, [functions])
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/DjangoEasyScoping/ScopingMixin.py#L42-L62)

Registers scopes for a Django model. These scopes can be used on their own and are also 
chainable with both other scopes and typical Django querysets.

**Arguments:**

name (*String*): Name of scope and calling method.

[functions] (...*): Function(s) which will be called when this scope is called.

**Returns:**

(*Queryset*): Returns the resultant queryset.

**Example:**

```python
Purchase.register_scope('millenial', 
                        lambda queryset: queryset.filter(customer__age__gte=22)
                                                 .filter(customer__age__lte=37))
>>>> Purchase.objects.all().millenial()
<ScopingQuerySet [ <Purchase: Purchase object (1)>, ... ]>
```
---

### register_aggregate

```python
register_aggregate(name, [functions])
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/DjangoEasyScoping/ScopingMixin.py#L64-L84)

Registers aggregates for a Django model. 

**Arguments:**

name (*String*): Name of aggregate and calling method.

[functions] (...*): Function(s) which will be called when this aggregate is called.

**Returns:**

{*Dictionary*}: Returns the resultant dictionary

**Example:**

```python
Purchase.register_aggregate('data_last_days', 
                            lambda queryset, days:
                            queryset.filter(sale_date__gte=datetime.now() - timedelta(days=days))
                                    .annotate(item_count=Count('customer'))
                                    .aggregate(total_sales=Count('customer'),
                                               average_items_per_sale=Avg('item_count'),
                                               total_profit=Sum('profit'),
                                               average_profit=Avg('profit'))
                            )

>>>> Purchase.objects.all().data_last_days(90)
{'average_items_per_sale': 4, 'total_sales': 158, 'average_profit': 1120.55, 'total_profit': 117047.60}
```
---
