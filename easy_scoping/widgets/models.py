from django.db import models
from .options import COLORS, SIZES, SHAPES
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet
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


# Basic scopes for testing filtering
Widget.scope('basic_query_widget', lambda qs: qs.f(color='blue',
                                                   size='small',
                                                   shape='circle'))
Widget.scope('blue', lambda qs: qs.f(color='blue'))
Widget.scope('small', lambda qs: qs.f(size='small'))
Widget.scope('circle', lambda qs: qs.f(shape='circle'))
Widget.scope('before_y2k',
             lambda qs: qs.f(used_on__lte=datetime.date(2000, 1, 1)))
Widget.scope('after_y2k',
             lambda qs: qs.f(used_on__gte=datetime.date(2000, 1, 1)))

# Basic scopes for testing excluding
Widget.scope('not_basic_query_widget', lambda qs: qs.e(color='blue',
                                                       size='small',
                                                       shape='circle'))
Widget.scope('not_blue', lambda qs: qs.e(color='blue'))
Widget.scope('not_small', lambda qs: qs.e(size='small'))
Widget.scope('not_circle', lambda qs: qs.e(shape='circle'))
Widget.scope('not_before_y2k',
             lambda qs: qs.e(used_on__lte=datetime.date(2000, 1, 1)))
Widget.scope('not_after_y2k',
             lambda qs: qs.e(used_on__gte=datetime.date(2000, 1, 1)))

# Scope takes argument
Widget.scope('take_args', lambda qs, i: qs.f(color=i))
Widget.scope('take_more_args', lambda qs, i, r: qs.f(color=i, size=r))
Widget.scope('take_kwargs', lambda qs, **kwargs: qs.f(**kwargs))

# Custom aggregate functions
Widget.register_aggregate('num_blue', lambda qs: qs.g('Count',
                                                      color='blue'))

Widget.register_aggregate('num_blue_small', lambda qs: qs.g('count',
                                                            color='blue',
                                                            size='small'))

Widget.register_aggregate('num_kwargs', lambda qs, **kwargs: qs.g('count',
                                                                  **kwargs))
