# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 19:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20170605_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsmodel',
            name='description',
        ),
    ]
