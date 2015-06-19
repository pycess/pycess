# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_fielddefinition_type_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldperstep',
            name='parameter',
        ),
    ]
