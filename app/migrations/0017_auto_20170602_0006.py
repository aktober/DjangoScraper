# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20170602_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recapmarketweek',
            name='previous',
            field=models.CharField(max_length=15),
        ),
    ]
