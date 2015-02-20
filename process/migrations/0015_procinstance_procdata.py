# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0014_auto_20150220_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='procinstance',
            name='procdata',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
