from django.test import TestCase
from widgets.models import Widget
from django.core import management as man
from django.db.models import Count, Case, When


class AggregationTests(TestCase):

    def setUp(self):
        man.call_command('loaddata',
                         'tests/fixtures/random_test_data.json')

    def test_db_data_loaded(self):
        obj = Widget.objects.all()
        self.assertEqual(obj.count(), 2500)

        obj = obj.a()
        self.assertEqual(obj.count(), 2500)

    def test_num_blue(self):
        obj1 = Widget.a().aggregate(ret=Count(Case(When(color='blue',
                                                        then=1))))['ret']
        obj2 = Widget.a().num_blue()

        self.assertEqual(obj1, obj2)

    def test_num_blue_filtered(self):
        obj1 = Widget.a().blue().not_small() \
                     .aggregate(ret=Count(Case(When(color='blue', then=1))))['ret']
        obj2 = Widget.a().blue().not_small().num_blue()

        self.assertEqual(obj1, obj2)

    def test_no_blue_filtered(self):
        obj1 = Widget.a().not_blue() \
                     .aggregate(ret=Count(Case(When(color='blue', then=1))))['ret']

        obj2 = Widget.a().not_blue().num_blue()

        self.assertEqual(obj1, obj2)

    def test_multiple_aggs(self):
        obj1 = Widget.a().basic_query_widget() \
                     .aggregate(ret=Count(Case(When(color='blue',
                                                    size='small',
                                                    then=1))))['ret']

        obj2 = Widget.a().basic_query_widget().num_blue_small()

        self.assertEqual(obj1, obj2)

        obj3 = Widget.a().not_circle().before_y2k() \
                     .aggregate(ret=Count(Case(When(color='blue',
                                                    size='small',
                                                    then=1))))['ret']

        obj4 = Widget.a().not_circle().before_y2k().num_blue_small()

        self.assertEqual(obj3, obj4)

    def test_passing_kwags(self):
        obj1 = Widget.a().basic_query_widget() \
                     .aggregate(ret=Count(Case(When(color='blue',
                                                    size='small',
                                                    then=1))))['ret']

        obj2 = Widget.a().basic_query_widget().num_kwargs(color='blue',
                                                          size='small')

        self.assertEqual(obj1, obj2)

        obj3 = Widget.a().not_circle().before_y2k() \
                     .aggregate(ret=Count(Case(When(color='blue',
                                                    size='small',
                                                    then=1))))['ret']

        obj4 = Widget.a().not_circle().before_y2k().num_blue_small()

        self.assertEqual(obj3, obj4)
