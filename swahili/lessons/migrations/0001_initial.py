# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infinitive', models.CharField(max_length=200)),
                ('english_translation', models.CharField(max_length=200)),
                ('exceptions', jsonfield.fields.JSONField()),
            ],
        ),
    ]
