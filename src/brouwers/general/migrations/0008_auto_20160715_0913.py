# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 07:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_registrationquestion_lang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='preference',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='refuse',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='secret_santa',
        ),
    ]