# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_add_overview_bool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddefinition',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'NORMAL'), (1, 'INTERNAL_TBD'), (2, 'JAVASCRIPT_INTERNAL_TBD')], default=0),
        ),
    ]
