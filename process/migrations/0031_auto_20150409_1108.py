# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0030_auto_20150328_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusscheme',
            name='role',
        ),
        migrations.AddField(
            model_name='statuslist',
            name='role',
            field=models.ForeignKey(to='process.RoleDefinition', null=True),
            preserve_default=True,
        ),
    ]
