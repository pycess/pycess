# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0027_auto_20150313_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statuslist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('process', models.ForeignKey(to='process.ProcessDefinition', null=True)),
            ],
            options={
                'verbose_name_plural': '3. Status',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='statuslist',
            unique_together=set([('process', 'name')]),
        ),
        migrations.AlterModelOptions(
            name='fielddefinition',
            options={'verbose_name_plural': '5. Field Definitions'},
        ),
        migrations.AlterModelOptions(
            name='processinstance',
            options={'verbose_name_plural': '7. Process Instances'},
        ),
        migrations.AlterModelOptions(
            name='roledefinition',
            options={'verbose_name_plural': '6. Role Definitions'},
        ),
        migrations.AlterModelOptions(
            name='roleinstance',
            options={'verbose_name_plural': '9. Role Instances'},
        ),
        migrations.AlterModelOptions(
            name='statusscheme',
            options={'verbose_name_plural': '4. Status Scheme'},
        ),
        migrations.RenameField(
            model_name='processinstance',
            old_name='status',
            new_name='runstatus',
        ),
        migrations.RemoveField(
            model_name='processinstance',
            name='currentstep',
        ),
        migrations.RemoveField(
            model_name='statusscheme',
            name='prestep',
        ),
        migrations.RemoveField(
            model_name='statusscheme',
            name='selfstep',
        ),
        migrations.AddField(
            model_name='processinstance',
            name='currentstatus',
            field=models.ForeignKey(blank=True, to='process.Statuslist', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='prestatus',
            field=models.ForeignKey(related_name='scheme_prestatus', blank=True, to='process.Statuslist', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='status',
            field=models.ForeignKey(related_name='scheme_status', to='process.Statuslist', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='step',
            field=models.ForeignKey(related_name='status_step', to='process.ProcessStep', null=True),
            preserve_default=True,
        ),
    ]
