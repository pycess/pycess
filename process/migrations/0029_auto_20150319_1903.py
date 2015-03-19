# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0028_auto_20150314_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processstep',
            name='role',
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='role',
            field=models.ForeignKey(to='process.RoleDefinition', null=True),
            preserve_default=True,
        ),
    ]
