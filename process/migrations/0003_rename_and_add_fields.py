# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_rename_step_to_status_scheme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fielddef',
            old_name='fldhelp',
            new_name='fieldhelp',
        ),
        migrations.RenameField(
            model_name='fielddef',
            old_name='fldtype',
            new_name='fieldtype',
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='name',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
    ]
