---
id: usage
title: Usage
---


## Example Django Model

```python


from django.db import models
from .options import COLORS, SIZES, SHAPES
from ScopingMixin import ScopingMixin, ScopingQuerySet
import datetime


class Widget(ScopingMixin, models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(choices=COLORS, max_length=30)
    size = models.CharField(choices=SIZES, max_length=30)
    shape = models.CharField(choices=SHAPES, max_length=30)
    used_on = models.DateField(default=datetime.date.today)

    objects = ScopingQuerySet.as_manager()


    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_size(self):
        return self.size

    def get_shape(self):
        return self.shape

    def get_used_on(self):
        return self.used_on

# Scopes for filtering
Widget.scope('basic_filter_widget', lambda qs: qs.f(color='blue',
                                                  size='small',
                                                  shape='circle'))
Widget.scope('blue', lambda qs: qs.f(color='blue'))
Widget.scope('small', lambda qs: qs.f(size='small'))
Widget.scope('circle', lambda qs: qs.f(shape='circle'))
Widget.scope('before_y2k', lambda qs: qs.f(used_on__lte=datetime.date(2000,1,1)))

# Scopes for excluding
Widget.scope('basic_exclude_widget', lambda qs: qs.e(color='blue',
                                                       size='small',
                                                       shape='circle'))
Widget.scope('not_blue', lambda qs: qs.e(color='blue'))
Widget.scope('not_small', lambda qs: qs.e(size='small'))
Widget.scope('not_circle', lambda qs: qs.e(shape='circle'))
Widget.scope('not_before_y2k', lambda qs: qs.e(used_on__lte=datetime.date(2000,1,1)))
```

## Usage

### Basic Scoping

Now, Let's say we wanted to find all of the widgets in our database which were
blue.

Without easy scoping:
```python
Widget.objects.filter(color='blue')
```
With easy scoping:

```python
Widget.a().blue()
```

### Basic Scoping Multiple Fields
How about finding all of the widgets which are blue, small, and a circle.

Without easy scoping:
```python
Widget.objects.filter(color='blue', size='small', shape='circle')
```
With easy scoping:

```python
Widget.a().basic_filter_widget()
```

### Chaining Scopes

Let's look at that same query where we chain these calls instead.

Without easy scoping:

```python
Widget.objects.filter(color='blue').filter(size='small').filter(shape='circle')
```

With easy scoping:

```python
Widget.a().blue().small().circle()
```

### Chaining Scopes + Django Methods

Of course, the return values of these scope methods are querysets so the
following holds.

```python
blue_objs = Widget.objects.filter(color='blue')
blue_small_objs = blue_objs.small()
blue_small_circles = blue_small_objs.circle()
```

### Exluding Scopes 

You can exclude here too. Let's consider all blue, small, but not
circle shaped objects.

Without easy scoping:

```python
Widget.objects.filter(color='blue').filter(size='small').exclude(shape='circle')
```

With easy scoping:

```python
Widget.a().blue().small().not_circle()
```

### Using Other Queryset Methods

As the return value is a queryset we can perform other django operations on
these querysets. The full list of operations can be found [here](https://docs.djangoproject.com/en/2.0/ref/models/querysets/).

Let's consider ordering these by their color in ascending
alphabetical order.

```python
Widget.a().blue().small().not_circle().order_by('color')
```
