from django.contrib import admin
from .models import Customer
from purchases.models import Purchase


class PurchaseInLine(admin.TabularInline):
    model = Purchase


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('name', 'state', 'gender', 'age', 'get_purchases')
    list_filter = ('name', 'state', 'gender', 'age')
    inlines = [PurchaseInLine]


admin.site.register(Customer, CustomerAdmin)
