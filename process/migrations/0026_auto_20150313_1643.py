# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0025_auto_20150313_1614'),
    ]

    operations = [
        migrations.RenameModel(
            old_name="RoleDef", new_name='RoleDefinition',
        ),
    ]
