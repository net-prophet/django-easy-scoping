from django.contrib import admin
from .models import Purchase


class WidgetInLine(admin.TabularInline):
    model = Purchase.items.through


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ('sale_date', 'sale_price', 'profit')
    list_filter = ('sale_date', 'sale_price', 'profit')
    inlines = [WidgetInLine]


admin.site.register(Purchase, PurchaseAdmin)
