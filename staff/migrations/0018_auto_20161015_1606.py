# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0017_auto_20161015_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='floorplan',
            name='building_name',
        ),
        migrations.AddField(
            model_name='floorplan',
            name='related_building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.Building', verbose_name='building'),
        ),
    ]