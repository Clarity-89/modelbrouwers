# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-13 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0006_auto_20160311_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='modelkit',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kits.Brand', verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='modelkit',
            name='scale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kits.Scale', verbose_name='scale'),
        ),
    ]
