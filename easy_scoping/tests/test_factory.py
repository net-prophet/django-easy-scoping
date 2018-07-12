import itertools
from django.test import TestCase
from widgets.models import Widget
from purchases.models import Purchase
from widgets.options import COLORS, SIZES, SHAPES
from tests.factories import PurchaseFactory


class FactoryTests(TestCase):

    def setUp(self):
        for color, size, shape in itertools.product(COLORS, SIZES, SHAPES):
            Widget.objects.create(color=color[0],
                                  size=size[0],
                                  shape=shape[0])
        for i in range(0, 200):
            PurchaseFactory.create()

    def test_factory(self):
        widgets = Widget.objects.all()
        self.assertEqual(widgets.count(), 336)
        purchases = Purchase.objects.all()
        self.assertEqual(purchases.count(), 200)


class ScopingMixinTests(TestCase):

    def setUp(self):
        for color, size, shape in itertools.product(COLORS, SIZES, SHAPES):
            Widget.objects.create(color=color[0],
                                  size=size[0],
                                  shape=shape[0])

    def test_scoping_blue(self):
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.objects.all().blue()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)

    def test_not_scope_agg(self):
        with self.assertRaises(AttributeError):
            Widget.objects.all().not_a_scope()

    def test_get_scope(self):
        obj1 = Widget.objects.all().blue()

        # this returns the scope function then to test we execute
        obj2 = Widget.get_scope('blue')()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)

        obj3 = Widget.objects.all().get_scope('blue')()

        self.assertQuerysetEqual(obj2,
                                 obj3,
                                 transform=lambda x: x,
                                 ordered=False)

    def test_get_aggregate(self):
        obj1 = Widget.objects.all().num_blue()

        # this returns the aggregate function then to test we execute
        obj2 = Widget.get_aggregate('num_blue')()

        self.assertEqual(obj1, obj2)

        obj3 = Widget.objects.all().get_aggregate('num_blue')()

        self.assertEqual(obj2, obj3)
