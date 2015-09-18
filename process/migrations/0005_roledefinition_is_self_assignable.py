# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_remove_fieldperstep_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='roledefinition',
            name='is_self_assignable',
            field=models.BooleanField(default=False),
        ),
    ]
