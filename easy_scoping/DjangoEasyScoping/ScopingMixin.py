from django.db import models
from django.db.models import Count, Case, When
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, name):
        if name in self.model.scopes():
            def scoped_query(*args, **kwargs):
                return self.model.scopes()[name](self, *args, **kwargs)
            return scoped_query
        elif name not in self.model.aggs():
            raise AttributeError('Queryset for %s has no attribute %s' %(self.model, name))

        if name in self.model.aggs():
            def aggregate_query(*args, **kwargs):
                return self.model.aggs()[name](self, *args, **kwargs)
            return aggregate_query
        elif name not in self.model.scopes():
            raise AttributeError('Aggregate for %s has no attribute %s' %(self.model, name))

    def a(self, *args, **kwargs):
        return self.all()

    def f(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def e(self, *args, **kwargs):
        return self.exclude(*args, **kwargs)

    def g(self, operation, *args, **kwargs):
        if operation.lower() == 'count':
            return self.aggregate(ret=Count(Case(When(then=1, **kwargs))))['ret']

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

    @classmethod
    def aggs(cls):
        if not getattr(cls, '__aggs__', None):
            setattr(cls, '__aggs__', dict())
        return cls.__aggs__

    @classmethod
    def register_aggregate(cls, name, func):
        from types import MethodType
        if name in cls.aggs():
            name = '_%s'%(name)

        cls.__aggs__[name] = func

        def aggregate_classmethod(klss, *args, **kwargs):
            return getattr(klss.a(), name)(*args, **kwargs)

        setattr(cls, 'agg_%s'%name, classmethod(aggregate_classmethod))

        def instance_in_agg(self, *args, **kwargs):
            return bool(func(self.a(), *args, **kwargs).g(pk=self.pk))

        setattr(cls, 'in_agg_%s'%name, MethodType(instance_in_agg, cls))
