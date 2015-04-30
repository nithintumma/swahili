# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_possessive'),
    ]

    operations = [
        migrations.AddField(
            model_name='possessive',
            name='english_translation',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
