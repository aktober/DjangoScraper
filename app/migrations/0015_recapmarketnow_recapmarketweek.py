# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_coinmarketbtclowhigh'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecapMarketNow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RecapMarketWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous', models.IntegerField()),
            ],
        ),
    ]