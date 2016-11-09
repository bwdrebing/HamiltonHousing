# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'', help_text=b'This is a name for this entry - it will not be displayed', max_length=50)),
                ('header_text', models.CharField(default=b'', help_text=b'This text will be displayed on the students home page as a page title', max_length=50, verbose_name=b'Home page main text')),
                ('header_subtext', models.TextField(default=b'', help_text=b'This text will be displayed on the home page below the title in a smaller font', verbose_name=b'Home page lead text')),
                ('lottery_name', models.CharField(default=b'', help_text=b'This is the name of the current lottery; it will display on the home page', max_length=25)),
                ('lottery_text', models.TextField(default=b'', help_text=b'This is a description of the logistics of the this lottery')),
                ('contact', models.TextField(default=b'', help_text=b'This is a block of text explaining who to contact with any immediate questions.')),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'updated',
            },
        ),
    ]
