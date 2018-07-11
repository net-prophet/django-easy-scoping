from django.contrib import admin
from .models import Widget


class WidgetAdmin(admin.ModelAdmin):
    model = Widget
    list_display = ('name', 'color', 'size', 'shape', 'cost')
    list_filter = ('color', 'size', 'shape', 'cost')


admin.site.register(Widget, WidgetAdmin)
