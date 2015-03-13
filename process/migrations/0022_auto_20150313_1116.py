# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0021_auto_20150313_0013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fielddefinition',
            options={'verbose_name_plural': '4. Field Definitions'},
        ),
        migrations.AlterModelOptions(
            name='processdef',
            options={'verbose_name_plural': '1. Process Definitions'},
        ),
        migrations.AlterModelOptions(
            name='processstep',
            options={'verbose_name_plural': '2. Process Steps'},
        ),
        migrations.AlterModelOptions(
            name='procinstance',
            options={'verbose_name_plural': '6. Process Instances'},
        ),
        migrations.AlterModelOptions(
            name='roledef',
            options={'verbose_name_plural': '5. Role Definitions'},
        ),
        migrations.AlterModelOptions(
            name='roleinstance',
            options={'verbose_name_plural': '8. Role Instances'},
        ),
        migrations.AlterModelOptions(
            name='statusscheme',
            options={'verbose_name_plural': '3. Status Schemes (Process Step Transitions)'},
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='parameter',
            field=models.TextField(default='{}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='procinstance',
            name='procdata',
            field=models.TextField(default='{}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roleinstance',
            name='role',
            field=models.ForeignKey(to='process.RoleDef', related_name='role_instance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(null=True, blank=True, to='process.ProcessStep', related_name='status_prestep'),
            preserve_default=True,
        ),
    ]
