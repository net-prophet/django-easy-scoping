---
id: installation
title: Getting Started
---

## Installation

`$ pip install django-easy-scoping`

Import `ScopingMixin` and `ScopingQuerySet` from `ScopingMixin.py`.
```python
from ScopingMixin import ScopingMixin, ScopingQuerySet
```

Mix `ScopingMixin` in with the Django model(s) you'd like to create scopes for.
```python
class Widget(ScopingMixin, models.Model):
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

Then simply open `ScopingMixin.py` and edit the following line
```python
class ScopingMixin(object):

    @classmethod
    def a(self):
        return self.objects.all()
```
 becomes
```python
class ScopingMixin(object):

    @classmethod
    def a(self):
        return self.other_name.all()
```
