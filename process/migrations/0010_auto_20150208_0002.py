# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0009_auto_20150207_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstep',
            name='role',
            field=models.ForeignKey(to='process.RoleDef', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='length',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='logic',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='remark',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='statusscheme',
            unique_together=set([('process', 'selfstep', 'prestep')]),
        ),
    ]
