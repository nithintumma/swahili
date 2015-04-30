# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20150414_2159'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Nouns',
            new_name='Noun',
        ),
        migrations.AddField(
            model_name='verb',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tags', blank=True),
        ),
        migrations.AlterField(
            model_name='adjective',
            name='exceptions',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='adjective',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tags', blank=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='verb',
            name='exceptions',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
