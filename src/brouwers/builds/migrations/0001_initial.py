# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 20:30
from __future__ import unicode_literals

import autoslug.fields
import brouwers.builds.models
import brouwers.forum_tools.fields
import brouwers.kits.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('kits', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a descriptive build title.', max_length=255, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=brouwers.builds.models.get_build_slug, unique=True, verbose_name='slug')),
                ('topic', brouwers.forum_tools.fields.ForumToolsIDField(blank=True, null=True, type=b'topic', unique=True, verbose_name='build report topic')),
                ('topic_start_page', models.PositiveSmallIntegerField(default=1, verbose_name='topic start page')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('kits', brouwers.kits.fields.KitsManyToManyField(blank=True, related_name='builds', to='kits.ModelKit', verbose_name='kits')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['kits__scale', 'kits__brand__name'],
                'verbose_name': 'build report',
                'verbose_name_plural': 'build reports',
            },
        ),
        migrations.CreateModel(
            name='BuildPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.URLField(blank=True, help_text='Link to an image')),
                ('order', models.PositiveSmallIntegerField(blank=True, help_text='Order in which photos are shown', null=True)),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='builds.Build', verbose_name='build')),
                ('photo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.Photo')),
            ],
            options={
                'ordering': ['order', 'id'],
                'verbose_name': 'build photo',
                'verbose_name_plural': 'build photos',
            },
        ),
    ]
