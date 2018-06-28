from django.contrib import admin
from .models import Widget


class WidgetAdmin(admin.ModelAdmin):
    model = Widget
    list_display = ('name', 'color', 'size', 'shape', 'used_on',)
    list_filter = ('color', 'size', 'shape', 'used_on')


admin.site.register(Widget, WidgetAdmin)
