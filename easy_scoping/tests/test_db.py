# The purpose of these tests are just to make sure our
# django db is set up correctly with our models.
from django.test import TestCase
from widgets.models import Widget
import datetime


class WidgetTests(TestCase):

    def setUp(self):
        basic_obj = Widget(name='testwidget',
                           color='Black',
                           size='Small',
                           shape='Rectangle')
        basic_obj.save()
        dummy_obj = Widget(name='dummywidget',
                           color='Green',
                           size='Medium',
                           shape='Ellipse')
        dummy_obj.save()

    def test_get_name(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_name(), 'testwidget')

    def test_get_color(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_color(), 'Black')

    def test_get_size(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_size(), 'Small')

    def test_get_shape(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_shape(), 'Rectangle')

    def test_get_used_on(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_used_on(), datetime.date.today())

    def test_all(self):
        obj = Widget.objects.get(name='testwidget')
        self.assertEqual(obj.get_name(), 'testwidget')
        self.assertEqual(obj.get_color(), 'Black')
        self.assertEqual(obj.get_size(), 'Small')
        self.assertEqual(obj.get_shape(), 'Rectangle')
        self.assertEqual(obj.get_used_on(), datetime.date.today())

    def test_create_new(self):
        obj = Widget.objects.create(name='otherwidget',
                                    color='Red',
                                    size='Large',
                                    shape='Triangle')
        obj.save()

        other = Widget.objects.get(name='otherwidget')
        self.assertEqual(other.get_name(), 'otherwidget')
        self.assertEqual(other.get_color(), 'Red')
        self.assertEqual(other.get_size(), 'Large')
        self.assertEqual(other.get_shape(), 'Triangle')
        self.assertEqual(other.get_used_on(), datetime.date.today())
