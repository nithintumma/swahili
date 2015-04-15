# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adjective', models.CharField(max_length=200)),
                ('english_translation', models.CharField(max_length=200)),
                ('exceptions', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ChartWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word_type', models.CharField(max_length=2, choices=[(b'p', b'possesive'), (b'd', b'demonstrative'), (b'sp', b'subject_prefix'), (b'op', b'object_prefix'), (b'na', b'neg_adjective')])),
                ('nc1', models.CharField(max_length=200)),
                ('nc2', models.CharField(max_length=200)),
                ('nc3', models.CharField(max_length=200)),
                ('nc4', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Nouns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('noun', models.CharField(max_length=200)),
                ('english_translation', models.CharField(max_length=200)),
                ('noun_class', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubjectPronoun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pronoun', models.CharField(max_length=200)),
                ('english_translation', models.CharField(max_length=200)),
                ('subject_prefix', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='adjective',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tags'),
        ),
    ]
