from django.db import models
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, attr):
        for plugin in ['scopes', 'aggregates']:
            if attr in getattr(self.model, '__%s__'%plugin):
                def scoped_query(*args, **kwargs):
                    return getattr(self.model, '__%s__'%plugin)[attr](self, *args, **kwargs)
                return scoped_query
        raise AttributeError('Queryset for %s has no attribute %s' %(self.model, attr))

class ScopingMixin(object):

    @classmethod
    def check_names(cls, name):
        if name in cls.scopes():
            raise AttributeError('%s already has a scope named %s' %(cls, name))

        if name in cls.aggregates():
            raise AttributeError('%s already has an aggregate named %s' %(cls, name))

    @classmethod
    def scopes(cls):
        if not getattr(cls, '__scopes__', None):
            setattr(cls, '__scopes__', dict())
        return cls.__scopes__

    @classmethod
    def register_scope(cls, name, func):
        from types import MethodType

        cls.check_names(name)
        cls.__scopes__[name] = func

        def scoped_query_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'scope_%s'%name, classmethod(scoped_query_classmethod))

        def instance_in_scope(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_scope_%s'%name, MethodType(instance_in_scope, cls))

    @classmethod
    def aggregates(cls):
        if not getattr(cls, '__aggregates__', None):
            setattr(cls, '__aggregates__', dict())
        return cls.__aggregates__

    @classmethod
    def register_aggregate(cls, name, func):
        from types import MethodType

        cls.check_names(name)
        cls.__aggregates__[name] = func

        def aggregate_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'agg_%s'%name, classmethod(aggregate_classmethod))

        def instance_in_agg(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_agg_%s'%name, MethodType(instance_in_agg, cls))

