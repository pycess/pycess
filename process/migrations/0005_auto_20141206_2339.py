# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_auto_20141206_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processdef',
            name='refering',
            field=models.ForeignKey(blank=True, to='process.ProcessDef', null=True),
        ),
    ]
