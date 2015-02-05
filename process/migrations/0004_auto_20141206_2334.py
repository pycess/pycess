# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_auto_20141206_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='process',
            field=models.ForeignKey(to='process.ProcessDef', null=True),
        ),
    ]
