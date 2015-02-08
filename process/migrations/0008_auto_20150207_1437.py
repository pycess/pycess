# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0007_auto_20150207_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddef',
            name='parent',
            field=models.ForeignKey(to='process.FieldDef', null=True),
            preserve_default=True,
        ),
    ]
