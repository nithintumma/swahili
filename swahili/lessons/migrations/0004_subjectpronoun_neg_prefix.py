# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20150415_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectpronoun',
            name='neg_prefix',
            field=models.CharField(default=b'ha', max_length=200),
        ),
    ]
