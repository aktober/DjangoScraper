# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170523_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='coindeskmodel',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
    ]
