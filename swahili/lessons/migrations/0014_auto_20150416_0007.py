# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_auto_20150415_2257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adjective',
            old_name='adjective',
            new_name='stem',
        ),
    ]
