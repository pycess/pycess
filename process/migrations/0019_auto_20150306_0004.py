# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0018_auto_20150227_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldperstep',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(related_name='field_perstep', to='process.ProcessStep'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(related_name='status_prestep', to='process.ProcessStep', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='selfstep',
            field=models.ForeignKey(related_name='status_thisstep', to='process.ProcessStep', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='statusscheme',
            unique_together=set([]),
        ),
    ]
