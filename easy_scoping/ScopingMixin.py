from django.db import models
class ScopingQuerySet(models.QuerySet):
    def __getattr__(self, name):
        if name in self.model.scopes():
            def scoped_query(*args, **kwargs):
                return self.model.scopes()[name](self.model, *args, **kwargs)
            return scoped_query
        raise AttributeError('Queryset for %s has no attribute %s' %(self.model, name))

    def f(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def restrict(self, *args, **kwargs):
        kwargs['qs'] = self
        return self.models.restrict(*args, **kwargs)

class ScopingManager(models.Manager):
    use_for_related_fields = True

    def __getattr__(self, name):
        if not name.startswith('__'):
            if name in self.model.scopes():
                def scoped_query(*args, **kwargs):
                    return self.model.scopes()[name](self.model, *args, **kwargs)
                return scoped_query
        return object.__getattribute__(self, name)

    def restrict(self, *args, **kwargs):
        return self.models.restrict(self, *args, **kwargs)

    def get_queryset(self):
        return ScopingQuerySet(self.model, using=self._db)

class ScopingMixin(object):

    @classmethod
    def f(self, *args, **kwargs):
        return self.objects.filter(*args, **kwargs)

    @classmethod
    def a(self):
        return self.objects.all()

    @classmethod
    def scopes(cls):
        if not getattr(cls, '__scopes__', None):
            setattr(cls, '__scopes__', dict())
        return cls.__scopes__

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
