# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0013_procinstance_currentstep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(related_name='fields', to='process.ProcessStep'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='procinstance',
            name='process',
            field=models.ForeignKey(related_name='instances', to='process.ProcessDef'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='procinstance',
            name='stoptime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roleinstance',
            name='procinst',
            field=models.ForeignKey(blank=True, to='process.ProcInstance', null=True),
            preserve_default=True,
        ),
    ]
