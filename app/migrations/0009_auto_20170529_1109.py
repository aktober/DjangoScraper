# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170529_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinmarketmodel',
            name='symbol',
            field=models.CharField(max_length=10),
        ),
    ]
