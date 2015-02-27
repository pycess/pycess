# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0016_auto_20150227_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldperstep',
            old_name='field',
            new_name='field_definition',
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(related_name='step_fields', to='process.ProcessStep'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='fieldperstep',
            unique_together=set([('step', 'field_definition')]),
        ),
    ]
