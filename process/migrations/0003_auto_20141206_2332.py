# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20141120_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processdef',
            name='refering',
            field=models.ForeignKey(to='process.ProcessDef', null=True),
        ),
    ]
