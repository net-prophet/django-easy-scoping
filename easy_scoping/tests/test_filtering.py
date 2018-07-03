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

    def test_redundant_chain(self):
        obj1 = Widget.a().basic_query_widget()
        obj2 = obj1.blue().circle().small()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
        self.assertEqual(obj1.get(), obj2.get())

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

    def test_query_chaining(self):
        obj1 = Widget.objects.filter(color='blue') \
                             .filter(size='small') \
                             .filter(shape='circle')
        obj2 = Widget.a().blue().small().circle()

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
