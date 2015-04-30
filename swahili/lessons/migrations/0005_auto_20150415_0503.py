# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_subjectpronoun_neg_prefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartword',
            name='nc10',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc12',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc13',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc14',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc15',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc16',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc17',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc18',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc5',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc6',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc7',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc8',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AddField(
            model_name='chartword',
            name='nc9',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AlterField(
            model_name='chartword',
            name='nc1',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AlterField(
            model_name='chartword',
            name='nc2',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AlterField(
            model_name='chartword',
            name='nc3',
            field=models.CharField(default=b'h', max_length=200),
        ),
        migrations.AlterField(
            model_name='chartword',
            name='nc4',
            field=models.CharField(default=b'h', max_length=200),
        ),
    ]
