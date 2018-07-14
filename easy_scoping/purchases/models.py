import pytz
import django
from django.db import models
from .state_regions import NORTHEAST, MIDWEST, SOUTH, WEST
from django.db.models import Sum, Count, Avg
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

Purchase.register_aggregate('data_last_days',
        lambda qs, days:
                qs.filter(sale_date__gte=dt.utcnow().replace(tzinfo=pytz.utc) - td(days=days))
                  .annotate(item_count=Count('items'))
                  .aggregate(total_sales=Count('customer'),
                             average_items_per_sale=Avg('item_count'),
                             total_profit=Sum('profit'),
                             average_profit=Avg('profit'))
                          )

Purchase.register_scope('senior', lambda qs: qs.filter(customer__age__gte=65))
Purchase.register_scope('millenial', lambda qs: qs.filter(customer__age__gte=22)
                                                  .filter(customer__age__lte=37))

Purchase.register_scope('male', lambda qs: qs.filter(customer__gender__in='M'))
Purchase.register_scope('female', lambda qs: qs.filter(customer__gender__in='F'))

Purchase.register_scope('northeast', lambda qs: qs.filter(**NORTHEAST))

Purchase.register_scope('midwest', lambda qs: qs.filter(**MIDWEST))

Purchase.register_scope('southern', lambda qs: qs.filter(**SOUTH))

Purchase.register_scope('western', lambda qs: qs.filter(**WEST))
