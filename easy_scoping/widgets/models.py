from django.db import models
from .options import COLORS, SIZES, SHAPES
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet
from django.db.models import Count, Case, When


class Widget(ScopingMixin, models.Model):
    name = models.CharField(max_length=30, blank=True)
    color = models.CharField(choices=COLORS, max_length=30)
    size = models.CharField(choices=SIZES, max_length=30)
    shape = models.CharField(choices=SHAPES, max_length=30)
    cost = models.FloatField(default=0,
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
            self.name = '%s.%s.%s' % (self.color, self.size, self.shape)

        color_sum = sum([ord(x) for x in self.color])
        size_sum = sum([ord(x) for x in self.size])
        shape_sum = sum([ord(x) for x in self.shape])
        self.cost = color_sum + size_sum + shape_sum
        super(Widget, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Scopes for getting full test coverage of the ScopingMixin
Widget.register_scope(
    'blue',
    lambda qs: qs.filter(color='blue')
)
Widget.register_aggregate(
    'num_blue',
    lambda qs: qs.aggregate(ret=Count(Case(When(then=1, color='blue'))))['ret']
)
