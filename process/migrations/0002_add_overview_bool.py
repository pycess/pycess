# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldperstep',
            name='is_part_of_overview',
            field=models.BooleanField(default=False),
        ),
    ]
