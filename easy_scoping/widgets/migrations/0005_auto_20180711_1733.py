# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-11 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0004_auto_20180711_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]