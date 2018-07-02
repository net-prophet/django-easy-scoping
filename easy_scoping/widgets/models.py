from django.db import models
from .options import COLORS, SIZES, SHAPES
from ScopingMixin import ScopingMixin, ScopingManager
import datetime


class Widget(ScopingMixin, models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(choices=COLORS, max_length=30)
    size = models.CharField(choices=SIZES, max_length=30)
    shape = models.CharField(choices=SHAPES, max_length=30)
    used_on = models.DateField(default=datetime.date.today)

    objects = ScopingManager()


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


Widget.scope('basic_query_widget', lambda qs: qs.f(color='blue',
                                                  size='small',
                                                  shape='circle'))

Widget.scope('blue', lambda qs: qs.f(color='blue'))
Widget.scope('small', lambda qs: qs.f(size='small'))
Widget.scope('circle', lambda qs: qs.f(shape='circle'))
