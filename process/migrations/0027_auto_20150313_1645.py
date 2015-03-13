# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0026_auto_20150313_1643'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProcInstance', new_name='ProcessInstance',
        ),
    ]
