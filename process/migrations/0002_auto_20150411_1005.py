# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_squashed_initial_2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Statuslist',
            new_name='Status',
        ),
        migrations.RenameModel(
            old_name='PycLog',
            new_name='PycessLog',
        ),
        migrations.RenameModel(
            old_name='StatusScheme',
            new_name='StatusTransition',
        ),
        migrations.AlterModelOptions(
            name='statustransition',
            options={'verbose_name_plural': '4. Status Transitions'},
        ),
        migrations.AlterField(
            model_name='processinstance',
            name='currentstatus',
            field=models.ForeignKey(blank=True, null=True, to='process.Status'),
        ),
        migrations.AlterField(
            model_name='statustransition',
            name='prestatus',
            field=models.ForeignKey(blank=True, null=True, related_name='scheme_prestatus', to='process.Status'),
        ),
        migrations.AlterField(
            model_name='statustransition',
            name='status',
            field=models.ForeignKey(null=True, related_name='scheme_status', to='process.Status'),
        ),
    ]
