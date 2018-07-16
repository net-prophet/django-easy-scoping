from django.db import models
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, attr):
        for plugin in [self.model.scopes(), self.model.aggregates()]:
            if attr in plugin:
                def plugin_query(*args, **kwargs):
                    return plugin[attr](self, *args, **kwargs)
                return plugin_query
        raise AttributeError('Queryset for %s has no attribute %s'%(self.model, attr))

    def get_scope(self, name):
        return self.model.get_scope(name)

    def get_aggregate(self, name):
        return self.model.get_aggregate(name)


class ScopingMixin(object):

    @classmethod
    def scopes(cls):
        if not getattr(cls, '__scopes__', None):
            setattr(cls, '__scopes__', dict())
        return cls.__scopes__

    @classmethod
    def get_scope(cls, name):
        if hasattr(cls, '__scopes__') and name in cls.scopes():
            return getattr(cls.objects.all(), name)

    @classmethod
    def aggregates(cls):
        if not getattr(cls, '__aggregates__', None):
            setattr(cls, '__aggregates__', dict())
        return cls.__aggregates__

    @classmethod
    def get_aggregate(cls, name):
        if hasattr(cls, '__aggregates__') and name in cls.aggregates():
            return getattr(cls.objects.all(), name)

    @classmethod
    def register_scope(cls, name, func):
        from types import MethodType

        if name in cls.scopes():
            name = '_%s'%(name)

        if cls.get_aggregate(name):
            raise AttributeError('%s already has an aggregate named %s'%(cls, name))

        cls.__scopes__[name] = func

        def scoped_query_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'scope_%s'%name, classmethod(scoped_query_classmethod))

        def instance_in_scope(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_scope_%s'%name, MethodType(instance_in_scope, cls))

    @classmethod
    def register_aggregate(cls, name, func):
        from types import MethodType

        if name in cls.aggregates():
            name = '_%s'%(name)

        if cls.get_scope(name):
            raise AttributeError('%s already has a scope named %s'%(cls, name))

        cls.__aggregates__[name] = func

        def aggregate_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'agg_%s'%name, classmethod(aggregate_classmethod))

        def instance_in_agg(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_agg_%s'%name, MethodType(instance_in_agg, cls))
