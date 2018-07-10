from django.test import TestCase
from widgets.models import Widget
from django.core import management as man


class ScopingTests(TestCase):

    def setUp(self):
        man.call_command('loaddata',
                         'tests/fixtures/filter_test_data.json')

    def test_db_data_loaded(self):
        obj = Widget.objects.all()
        self.assertEqual(obj.count(), 336)

        obj = obj.a()
        self.assertEqual(obj.count(), 336)

    def test_created_recent_days(self):
        import datetime
        today = datetime.date.today()
        days_ago = today - datetime.timedelta(days=30)
        obj1 = Widget.objects.filter(used_on__range=(days_ago, today))
        obj2 = Widget.a().recent_30()
        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
