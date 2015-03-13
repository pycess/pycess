# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0024_auto_20150313_1609'),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProcessDef", new_name='ProcessDefinition',
        ),
    ]
