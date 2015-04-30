# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_auto_20150415_0506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chartword',
            old_name='nc12',
            new_name='nc11',
        ),
    ]
