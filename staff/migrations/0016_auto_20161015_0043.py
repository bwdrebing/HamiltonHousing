# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0015_auto_20161015_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floorplan',
            name='building_name',
            field=models.CharField(default='', help_text='This can be an abbreviation. Just for sorting purposes.', max_length=100),
        ),
    ]