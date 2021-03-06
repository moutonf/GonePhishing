# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-20 06:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0021_auto_20171020_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='date_created',
            field=models.CharField(default=datetime.datetime(2017, 10, 20, 8, 36, 15, 285003), max_length=100),
        ),
        migrations.AlterField(
            model_name='groups',
            name='created_date',
            field=models.CharField(default=datetime.datetime(2017, 10, 20, 8, 36, 15, 285503), max_length=100),
        ),
        migrations.AlterField(
            model_name='members',
            name='register_date',
            field=models.CharField(default=datetime.datetime(2017, 10, 20, 8, 36, 15, 267003), max_length=100),
        ),
        migrations.AlterField(
            model_name='sending_profiles',
            name='created_date',
            field=models.CharField(default=datetime.datetime(2017, 10, 20, 8, 36, 15, 287503), max_length=100),
        ),
        migrations.AlterField(
            model_name='userss',
            name='sent_date',
            field=models.CharField(default=datetime.datetime(2017, 10, 20, 8, 36, 15, 286003), max_length=100),
        ),
    ]
