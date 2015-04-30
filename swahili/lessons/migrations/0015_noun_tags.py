# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0014_auto_20150416_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='noun',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tags', blank=True),
        ),
    ]
