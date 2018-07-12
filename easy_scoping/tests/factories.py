import datetime as dt
import pytz
import random
import factory
import factory.fuzzy as fuz
from purchases.models import Purchase
from widgets.models import Widget


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase

    sale_date = fuz.FuzzyDateTime(dt.datetime(1950, 1, 1, tzinfo=pytz.UTC))

    @factory.post_generation
    def items(self, create, purchased, **kwargs):
        amt_purchased = random.randint(1, 10)
        purchased = Widget.objects.all().order_by('?')[:amt_purchased]

        if create and purchased:
            for item in purchased:
                self.items.add(item)
