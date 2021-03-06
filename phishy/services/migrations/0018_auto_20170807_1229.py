# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 10:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_auto_20170807_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='sending_profiles',
            name='created_date',
            field=models.CharField(default=datetime.datetime(2017, 8, 7, 12, 29, 34, 43000), max_length=100),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='date_created',
            field=models.CharField(default=datetime.datetime(2017, 8, 7, 12, 29, 34, 41000), max_length=100),
        ),
        migrations.AlterField(
            model_name='groups',
            name='created_date',
            field=models.CharField(default=datetime.datetime(2017, 8, 7, 12, 29, 34, 41000), max_length=100),
        ),
        migrations.AlterField(
            model_name='members',
            name='register_date',
            field=models.CharField(default=datetime.datetime(2017, 8, 7, 12, 29, 34, 25000), max_length=100),
        ),
        migrations.AlterField(
            model_name='userss',
            name='sent_date',
            field=models.CharField(default=datetime.datetime(2017, 8, 7, 12, 29, 34, 41000), max_length=100),
        ),
    ]
