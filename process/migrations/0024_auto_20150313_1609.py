# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0023_auto_20150313_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='actiontype',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='processstep',
            name='index',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
