# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_remove_newsmodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsmodel',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
