# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0017_auto_20150227_1352'),
    ]

    operations = [
        migrations.RenameModel( 'FieldDef', 'FieldDefinition' )
    ]
