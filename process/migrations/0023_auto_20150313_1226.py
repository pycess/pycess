# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0022_auto_20150313_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='process',
            field=models.ForeignKey(related_name='steps', null=True, to='process.ProcessDef'),
            preserve_default=True,
        ),
    ]
