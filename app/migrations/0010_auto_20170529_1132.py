# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20170529_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinmarketmodel',
            name='market_cap_usd',
            field=models.FloatField(max_length=20),
        ),
        migrations.AlterField(
            model_name='coinmarketmodel',
            name='percent_change_7d',
            field=models.FloatField(max_length=6),
        ),
        migrations.AlterField(
            model_name='coinmarketmodel',
            name='price_usd',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='coinmarketmodel',
            name='rank',
            field=models.IntegerField(),
        ),
    ]
