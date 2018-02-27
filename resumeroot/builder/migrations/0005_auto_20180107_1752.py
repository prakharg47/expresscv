# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-07 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0004_theme_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme_model',
            name='font_family',
            field=models.CharField(choices=[('computer modern', 'computer modern'), ('arial', 'arial'), ('calibri', 'calibri')], default='computer modern', max_length=60),
        ),
        migrations.AlterField(
            model_name='theme_model',
            name='theme',
            field=models.CharField(choices=[('standard', 'standard'), ('express', 'express'), ('compact', 'compact')], default='standard', max_length=60),
        ),
    ]