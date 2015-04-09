# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0031_auto_20150409_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusscheme',
            name='step',
        ),
        migrations.AddField(
            model_name='statuslist',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='status_step', null=True),
        ),
    ]
