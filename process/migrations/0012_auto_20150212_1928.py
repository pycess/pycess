# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0011_auto_20150208_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(
                related_name='steps', to='process.ProcessStep'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(
                null=True, to='process.ProcessStep', related_name='prestep'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='selfstep',
            field=models.ForeignKey(
                null=True, to='process.ProcessStep', related_name='selfstep'),
            preserve_default=True,
        ),
    ]
