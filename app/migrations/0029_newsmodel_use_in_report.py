# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20170605_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsmodel',
            name='use_in_report',
            field=models.BooleanField(default=False),
        ),
    ]
