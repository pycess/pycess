# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0020_roleinstance_pycuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldperstep',
            name='parameter',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roleinstance',
            name='exittime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
