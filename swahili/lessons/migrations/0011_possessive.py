# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_questionword'),
    ]

    operations = [
        migrations.CreateModel(
            name='Possessive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stem', models.CharField(max_length=200)),
                ('chart_type', models.ForeignKey(to='lessons.ChartWord')),
            ],
        ),
    ]
