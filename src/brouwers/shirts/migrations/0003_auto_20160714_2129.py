# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shirts', '0002_shirtorder_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirtorder',
            name='user',
        ),
        migrations.DeleteModel(
            name='ShirtOrder',
        ),
    ]