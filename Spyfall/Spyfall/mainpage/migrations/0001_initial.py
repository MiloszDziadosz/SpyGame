# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-18 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gametemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_temp_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=250)),
                ('gametemp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.Gametemp')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('gametemp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.Gametemp')),
            ],
        ),
    ]
