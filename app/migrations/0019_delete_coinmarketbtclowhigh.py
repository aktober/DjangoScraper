# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170602_0721'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CoinMarketBtcLowHigh',
        ),
    ]
