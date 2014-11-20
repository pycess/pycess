# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_squashed_initial_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusscheme',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
