# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0029_auto_20150319_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddefinition',
            name='fieldtype',
            field=models.PositiveSmallIntegerField(choices=[(0, 'STRING'), (1, 'INTEGER'), (2, 'FLOAT'), (3, 'FINANCE_NUMBER_TBD'), (4, 'DATE'), (5, 'DATETIME'), (6, 'BLOB_TBD'), (7, 'ENUM_TBD')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fielddefinition',
            name='type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'NORMAL'), (1, 'INTERNAL'), (2, 'JAVASCRIPT_INTERNAL')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='processinstance',
            name='runstatus',
            field=models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='processstep',
            name='actiontype',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'NOT_USED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='process',
            field=models.ForeignKey(null=True, to='process.ProcessDefinition', related_name='schemes'),
            preserve_default=True,
        ),
    ]
