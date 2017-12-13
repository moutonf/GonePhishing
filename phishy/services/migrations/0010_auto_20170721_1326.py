# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 11:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20170721_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_groups',
            fields=[
                ('user_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='services.groups')),
            ],
        ),
        migrations.AlterField(
            model_name='campaign',
            name='date_created',
            field=models.CharField(default=datetime.datetime(2017, 7, 21, 13, 26, 16, 569867), max_length=100),
        ),
        migrations.AlterField(
            model_name='members',
            name='register_date',
            field=models.CharField(default=datetime.datetime(2017, 7, 21, 13, 26, 16, 554867), max_length=100),
        ),
        migrations.AddField(
            model_name='user_groups',
            name='member_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='services.members'),
        ),
        migrations.AddField(
            model_name='user_groups',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='services.quick_attack'),
        ),
    ]