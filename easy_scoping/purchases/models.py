import django
from django.db import models
from django.db.models import Sum
from widgets.models import Widget
from customers.models import Customer
from datetime import datetime as dt, timedelta as td
from DjangoEasyScoping.ScopingMixin import ScopingMixin, ScopingQuerySet



class Purchase(ScopingMixin, models.Model):
    items = models.ManyToManyField(Widget, blank=True)
    sale_date = models.DateTimeField(default=django.utils.timezone.now)
    sale_price = models.FloatField(default=0, blank=True)
    profit = models.FloatField(default=0, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    objects = ScopingQuerySet.as_manager()

    def get_items(self):
        return self.items.all()

    def get_item_count(self):
        return self.items.all().count()

    def get_sale_date(self):
        return self.sale_date

    def get_sale_price(self):
        return self.sale_price

    def get_cost(self):
        return round(self.items.aggregate(cost=Sum('cost'))['cost'], 2)

    def get_profit(self):
        return self.profit

    def set_sale_price(self):
        cost_plus_profit= 1.1
        cost = self.get_cost()
        self.sale_price = round(cost*cost_plus_profit, 2)

    def set_profit(self):
        profit_margin = .1
        cost = self.get_cost()
        self.profit = round(cost*profit_margin, 2)

    def save(self, *args, **kwargs):
        if self.id:
            for item in Widget.objects.filter(purchase=self):
                self.items.add(item)
            self.set_sale_price()
            self.set_profit()
        super(Purchase, self).save(*args, **kwargs)

Purchase.register_aggregate('profit_last_days',
                            lambda qs, d: round(
                                qs.filter(sale_date__gte=dt.now() - td(days=d))
                                  .aggregate(x=Sum('profit'))['x'])
                            )

'''

Purchase.register_aggregate('test',
                            lambda qs, d, **kwargs: round(
                                sum_field_last_days(qs, d, **kwargs))
                            )
'''
