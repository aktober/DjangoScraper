# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_coindeskmodel_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coindeskmodel',
            name='featured',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='coindeskmodel',
            name='image_url',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='coindeskmodel',
            name='pub_date',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
