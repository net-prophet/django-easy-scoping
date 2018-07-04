---
id: api
title: API
---

## ScopingMixin

### Scope
```python
scope(name, [functions])
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/ScopingMixin.py#L32-L47)

Registers scopes for a Django model. These scopes can be used on their own and are also 
chainable with both other scopes and typical Django querysets.

**Arguments:**

name (*String*): Name of scope and calling method.

[functions] (...*): Function(s) which will be called when this scope is called.

**Returns:**

(*Queryset*): Returns the resultant queryset.

**Example:**

```python
Widget.scope('scope_example', lambda queryset: queryset.filter(color='blue'))
```
---

### a

```python
a()
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/ScopingMixin.py#L21-L23)

A helper method to shorten the queryset `cls.objects.all()` syntax. Here,
`objects` is the name of the `ScopingQuerySet` which was overridden on the
Django model. 

**Returns:**

(*Queryset*): Returns the resultant `.all()` queryset.

**Example:**

```python
Widget.a()
```
---

## ScopingQuerySet

### f

```python
f(*args, **kwargs)
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/ScopingMixin.py#L13-L14)

A helper method to shorten the syntax of `.filter()`.

**Arguments:**

*args : Arguments needed for the functions registered with `.scope()`.

**kargs : Keyword arguments needed for the functions registered with `.scope()`.

**Returns:**

(*Queryset*): The resultant queryset.

**Example:**

```python
Widget.a().f(color='blue')

A more typical use case would be when registering scopes.

Widget.scope('scope_example', lambda queryset: queryset.f(color='blue'))
```
---

### e

```python
e(*args, **kwargs)
```
[source](http://www.github.com/net-prophet/django-easy-scoping/blob/master/easy_scoping/ScopingMixin.py#L13-L14)

A helper method to shorten the syntax of `.exclude()`.

**Arguments:**

*args : Arguments needed for the functions registered with `.scope()`.

**kargs : Keyword arguments needed for the functions registered with `.scope()`.

**Returns:**

(*Queryset*): The resultant queryset.

**Example:**

```python
Widget.a().e(color='blue')

A more typical use case would be when registering scopes.

Widget.scope('scope_example', lambda queryset: queryset.e(color='blue'))
```
---
