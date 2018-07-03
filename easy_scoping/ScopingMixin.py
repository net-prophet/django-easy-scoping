# So we override the queryset to getattrs set in the .scope() method
# of the mixin.
from django.db import models
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, name):
        if name in self.model.scopes():
            def scoped_query(*args, **kwargs):
                return self.model.scopes()[name](self.model, *args, **kwargs)
            return scoped_query
        raise AttributeError('Queryset for %s has no attribute %s' %(self.model, name))

class ScopingMixin(object):

    # Just to shorten the syntax in use
    @classmethod
    def a(self):
        return self.objects.all()

    # This method should `return self.filter(...)` but it's not receiving a
    # queryset
    @classmethod
    def f(self, *args, **kwargs):
        return self.objects.filter(*args, **kwargs)

    # this just checks if the scope is actually registered
    @classmethod
    def scopes(cls):
        if not getattr(cls, '__scopes__', None):
            setattr(cls, '__scopes__', dict())
        return cls.__scopes__

    # Here is where we actually register the scopes. This appears to be working
    # just fine, the problem is that we aren't able to chain.
    @classmethod
    def scope(cls, name, func):
        from types import MethodType
        if name in cls.scopes():
            name = '%s_%s'%(cls.label, name)

        cls.__scopes__[name] = func

        def scoped_query_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'scope_%s'%name, classmethod(scoped_query_classmethod))

        def instance_in_scope(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_scope_%s'%name, MethodType(instance_in_scope, cls))
