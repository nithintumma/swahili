# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_auto_20150415_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartword',
            name='nc12',
            field=models.CharField(default=b'h', max_length=200),
        ),
    ]
