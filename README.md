Django Easy Scoping allows you to register scopes and aggregate functions on
your Django models. 

## Installation

To get the `ScopingMixin.py` file you can download it or use pip.

### Downloading File

Download the ScopingMixin file from github.
[ScopingMixin.py](http://github.com/net-prophet/django-easy-scoping/blob/master/DjangoEasyScoping/DjangoEasyScoping/ScopingMixin.py)

Import `ScopingMixin` and `ScopingQuerySet` from `ScopingMixin.py`.
```python
from <path to file>.ScopingMixin import ScopingMixin, ScopingQuerySet
```

### Using pip

`$ pip install django-easy-scoping`

Import `ScopingMixin` and `ScopingQuerySet` from `ScopingMixin.py`.
```python
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet
```

### Implementing

Mix `ScopingMixin` in with the Django model(s) you'd like to create scopes for.

For example, in the [purchases](https://net-prophet.github.io/django-easy-scoping/docs/usage.html#purchases-modelspy) model:
```python
class Purchase(ScopingMixin, models.Model):
```

Override the Queryset for that model using `ScopingQuerySet`. By default, the override's name must be `objects`
(see [below](https://net-prophet.github.io/django-easy-scoping/docs/installation.html#implementing-with-existing-managers-querysets)
 for changing the default).
```python
    objects = ScopingQuerySet.as_manager()
```

Done!

## Implementing with existing Managers/Querysets

If you'd like to continue using your own custom manager/queryset then you can! 
You only need to take action if you'd like to replace the default name (`objects`)
of the ScopingQuerySet override, for instance:

```python 
other_name = ScopingQuerySet.as_manager()
```

Then, simply open `ScopingMixin.py` in your `sites-packages` and edit the following 
methods on lines 6 and 11.

```python
1  class ScopingMixin(object):
2
3      @classmethod
4      def get_scope(cls, name)
5          if hasattr(cls, '__scopes__') and name in cls.scopes():
6              return getattr(cls.objects.all(), name)
7
8      @classmethod
9      def get_aggregate(cls, name)
10         if hasattr(cls, '__aggregate__') and name in cls.aggregates():
11             return getattr(cls.objects.all(), name)
```
 becomes
```python
1  class ScopingMixin(object):
2
3      @classmethod
4      def get_scope(cls, name)
5          if hasattr(cls, '__scopes__') and name in cls.scopes():
6              return getattr(cls.other_name.all(), name)
7
8      @classmethod
9      def get_aggregate(cls, name)
10         if hasattr(cls, '__aggregate__') and name in cls.aggregates():
11             return getattr(cls.other_name.all(), name)
```
