# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-26 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_auto_20191125_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='password',
            field=models.CharField(max_length=10),
        ),
    ]