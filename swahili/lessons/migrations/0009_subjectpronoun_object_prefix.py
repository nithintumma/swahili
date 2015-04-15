# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_chartword_nc12'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectpronoun',
            name='object_prefix',
            field=models.CharField(default=b'w', max_length=200),
        ),
    ]
