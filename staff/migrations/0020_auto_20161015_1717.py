# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0019_auto_20161015_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='floor_plans',
            field=models.ManyToManyField(blank=True, to='staff.FloorPlan'),
        ),
    ]
