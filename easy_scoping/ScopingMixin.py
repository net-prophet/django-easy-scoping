from django.db import models
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, name):
        if name in self.model.scopes():
            def scoped_query(*args, **kwargs):
                return self.model.scopes()[name](self, *args, **kwargs)
            return scoped_query
        raise AttributeError('Queryset for %s has no attribute %s' %(self.model, name))

    def a(self, *args, **kwargs):
        return self.all()

    def f(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def e(self, *args, **kwargs):
        return self.exclude(*args, **kwargs)

class ScopingMixin(object):

    @classmethod
    def a(cls):
        return cls.objects.all()

    @classmethod
    def scopes(cls):
        if not getattr(cls, '__scopes__', None):
            setattr(cls, '__scopes__', dict())
        return cls.__scopes__

    @classmethod
    def scope(cls, name, func):
        from types import MethodType
        if name in cls.scopes():
            name = '_%s'%(name)

        cls.__scopes__[name] = func

        def scoped_query_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'scope_%s'%name, classmethod(scoped_query_classmethod))

        def instance_in_scope(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_scope_%s'%name, MethodType(instance_in_scope, cls))
