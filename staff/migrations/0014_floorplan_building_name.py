# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0013_floorplan_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='floorplan',
            name='building_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.Building'),
        ),
    ]