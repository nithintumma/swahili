# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_possessive_english_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartword',
            name='word_type',
            field=models.CharField(max_length=2, choices=[(b'p', b'possesive'), (b'd', b'demonstrative'), (b'sp', b'subject_prefix'), (b'np', b'negative_prefix'), (b'op', b'object_prefix'), (b'ap', b'adjective_prefix'), (b'a', b'associative')]),
        ),
    ]
