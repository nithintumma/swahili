# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_subjectpronoun_object_prefix'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=200)),
                ('english_translation', models.CharField(max_length=200)),
                ('end', models.BooleanField(default=True)),
            ],
        ),
    ]
