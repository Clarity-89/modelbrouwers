# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 16:59
from __future__ import unicode_literals

import brouwers.kits.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boxart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=brouwers.kits.models.get_uuid, max_length=36, verbose_name='uuid')),
                ('image', models.ImageField(upload_to='kits/box_images/%Y/%m')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'boxart image upload',
                'verbose_name_plural': 'boxart image uploads',
            },
        ),
    ]