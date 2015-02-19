# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0012_auto_20150212_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='procinstance',
            name='currentstep',
            field=models.ForeignKey(blank=True, to='process.ProcessStep', null=True),
            preserve_default=True,
        ),
    ]
