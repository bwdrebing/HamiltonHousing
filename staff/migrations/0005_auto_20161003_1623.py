# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20161003_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='class_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='lottery_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]