# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 08:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20170605_0829'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CoinMarketModel',
        ),
    ]
