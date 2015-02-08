# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_auto_20150201_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fielddef',
            name='editable',
        ),
        migrations.RemoveField(
            model_name='fielddef',
            name='must',
        ),
    ]
