Django Easy Scoping allows you to register scopes and aggregate functions on
your Django models. 

## Installation

`$ pip install django-easy-scoping`

Import `ScopingMixin` and `ScopingQuerySet` from `ScopingMixin.py`.
```python
from ScopingMixin import ScopingMixin, ScopingQuerySet
```

Mix `ScopingMixin` in with the Django model(s) you'd like to create scopes for.
```python
class Purchase(ScopingMixin, models.Model):
```

Override the Queryset for that model using `ScopingQuerySet`.
```python
    objects = ScopingQuerySet.as_manager()
```

Done!

## Implementing with existing Managers/Querysets

If you'd like to continue using your own custom manager/queryset then you can! 
You only need to take action if you'd like to name the ScopingQuerySet override
something other than `objects`, for instance:

```python 
other_name = ScopingQuerySet.as_manager()
```

Then simply open `ScopingMixin.py` and edit the following methods
```python
class ScopingMixin(object):

    @classmethod
    def get_scope(cls, name)
        if hasattr(cls, '__scopes__') and name in cls.scopes():
            return getattr(cls.objects.all(), name)

    @classmethod
    def get_aggregate(cls, name)
        if hasattr(cls, '__aggregate__') and name in cls.aggregates():
            return getattr(cls.objects.all(), name)
```
 becomes
```python
class ScopingMixin(object):

    @classmethod
    def get_scope(cls, name)
        if hasattr(cls, '__scopes__') and name in cls.scopes():
            return getattr(cls.other_name.all(), name)

    @classmethod
    def get_aggregate(cls, name)
        if hasattr(cls, '__aggregate__') and name in cls.aggregates():
            return getattr(cls.other_name.all(), name)
```
