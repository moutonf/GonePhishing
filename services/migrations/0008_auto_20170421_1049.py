# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20170421_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='victims',
            name='auto_id',
            field=models.IntegerField(default='', max_length=300),
        ),
    ]