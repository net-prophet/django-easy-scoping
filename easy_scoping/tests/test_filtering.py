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
        obj = Widget.objects.filter(color='blue', size='small', shape='circle')
        print(obj)
        self.assertEqual(obj.count(), 1)
