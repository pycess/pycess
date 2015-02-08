# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0010_auto_20150208_0002'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fieldperstep',
            unique_together=set([('step', 'field')]),
        ),
    ]
