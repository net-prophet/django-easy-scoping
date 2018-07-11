from django.db import models
from .options import COLORS, SIZES, SHAPES
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet
from django.db.models import Count, Case, When


class Widget(ScopingMixin, models.Model):
    name = models.CharField(max_length=30, blank=True)
    color = models.CharField(choices=COLORS, max_length=30)
    size = models.CharField(choices=SIZES, max_length=30)
    shape = models.CharField(choices=SHAPES, max_length=30)
    cost = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               default=0,
                               blank=True)

    objects = ScopingQuerySet.as_manager()

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_size(self):
        return self.size

    def get_shape(self):
        return self.shape

    def get_cost(self):
        return self.cost

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = '%s.%s.%s'%(self.color, self.size, self.shape)

        color_sum = sum([ord(x) for x in self.color])
        size_sum = sum([ord(x) for x in self.size])
        shape_sum = sum([ord(x) for x in self.shape])
        self.cost = color_sum + size_sum + shape_sum
        super(Widget, self).save(*args, **kwargs)

# Basic scopes for testing filtering
Widget.register_scope('basic_query_widget',
                      lambda qs: qs.filter(color='blue',
                                           size='small',
                                           shape='circle'))
Widget.register_scope('blue',
                      lambda qs: qs.filter(color='blue'))
Widget.register_scope('small',
                      lambda qs: qs.filter(size='small'))
Widget.register_scope('circle',
                      lambda qs: qs.filter(shape='circle'))

# Basic scopes for testing excluding
Widget.register_scope('not_basic_query_widget',
                      lambda qs: qs.exclude(color='blue',
                                            size='small',
                                            shape='circle'))
Widget.register_scope('not_blue',
                      lambda qs: qs.exclude(color='blue'))
Widget.register_scope('not_small',
                      lambda qs: qs.exclude(size='small'))
Widget.register_scope('not_circle',
                      lambda qs: qs.exclude(shape='circle'))

# Scope takes argument
Widget.register_scope('take_args',
                      lambda qs, i: qs.filter(color=i))
Widget.register_scope('take_more_args',
                      lambda qs, i, r: qs.filter(color=i, size=r))
Widget.register_scope('take_kwargs',
                      lambda qs, **kwargs: qs.filter(**kwargs))

# Custom aggregate functions
Widget.register_aggregate('num_blue',
                          lambda qs: qs.aggregate(ret=Count(Case(When(then=1,
                          color='blue'))))['ret'])

Widget.register_aggregate('num_blue_small',
                          lambda qs: qs.aggregate(ret=Count(Case(When(then=1,
                          color='blue', size='small'))))['ret'])

Widget.register_aggregate('num_kwargs',
                          lambda qs, **kwargs: qs.aggregate(
                          ret=Count(Case(When(then=1, **kwargs))))['ret'])
