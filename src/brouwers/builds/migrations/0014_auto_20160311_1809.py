# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 17:09
from __future__ import unicode_literals

import brouwers.kits.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0013_auto_20160130_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='kits',
            field=brouwers.kits.fields.KitsManyToManyField(blank=True, related_name='builds', verbose_name='kits'),
        ),
    ]
