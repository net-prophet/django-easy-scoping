from django.test import TestCase
from widgets.models import Widget
from django.core import management as man


class FilterTests(TestCase):

    def setUp(self):
        man.call_command('loaddata',
                         'tests/fixtures/filter_test_data.json',
                         verbosity=2)

    def test_db_data_loaded(self):
        obj = Widget.objects.all()
        self.assertEqual(obj.count(), 336)

    def test_query_widget(self):
        obj1 = Widget.objects.filter(color='blue',
                                     size='small',
                                     shape='circle')
        obj2 = Widget.a().basic_query_widget()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
        self.assertEqual(obj1.get(), obj2.get())

    def test_query_blue(self):
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.a().blue()

        self.assertEqual(obj1.count(), obj2.count())
        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)

    # this is my failing test
    def test_query_chaining(self):

        # Here, these have the same count (as desired)
        # .a() is defined in ScopingMixin and is just objects.all()
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.a().blue()
        print('obj1: ', obj1.count())
        print('obj2: ', obj2.count())


        # This correctly filters the blue elements down as expected
        obj1 = obj1.filter(size='small')
        print('obj1: ', obj1.count())

        # Here, instead of passing the queryset in it just passes the class
        # these represents a new filters of .small()
        obj2 = obj2.small()
        print('obj2: ', obj2.count())

        # The same here, obviously
        obj1 = obj1.filter(shape='circle')
        obj2 = obj2.circle()
        print('obj1: ', obj1.count())
        print('obj2: ', obj2.count())

        # This also just returns the count for .circle()
        # goes off the last 'chained' element
        obj3 = Widget.a().blue().small().circle()
        print('obj3:', obj3.count())

        # These fail, obviously
        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
