# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0005_auto_20141206_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='fielddef',
            name='process',
            field=models.ForeignKey(to='process.ProcessDef', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='interaction',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='process',
            field=models.ForeignKey(to='process.ProcessDef', null=True),
            preserve_default=True,
        ),
    ]
