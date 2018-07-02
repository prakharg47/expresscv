# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-25 21:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('app_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('plan', models.IntegerField(default=0, max_length=50)),
                ('expiry_date', models.DateTimeField()),
                ('job_suggestions', models.BooleanField(default=True)),
            ],
        ),
    ]