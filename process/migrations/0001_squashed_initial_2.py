# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('process', '0001_squashed_initial_1'), ('process', '0002_auto_20141120_1902'), ('process', '0003_auto_20141206_2332'), ('process', '0004_auto_20141206_2334'), ('process', '0005_auto_20141206_2339'), ('process', '0006_auto_20150201_1344'), ('process', '0007_auto_20150207_1429'), ('process', '0008_auto_20150207_1437'), ('process', '0009_auto_20150207_1443'), ('process', '0010_auto_20150208_0002'), ('process', '0011_auto_20150208_0036'), ('process', '0012_auto_20150212_1928'), ('process', '0013_procinstance_currentstep'), ('process', '0014_auto_20150220_1404'), ('process', '0015_procinstance_procdata'), ('process', '0016_auto_20150227_1306'), ('process', '0017_auto_20150227_1352'), ('process', '0018_auto_20150227_1357'), ('process', '0019_auto_20150306_0004'), ('process', '0020_roleinstance_pycuser'), ('process', '0021_auto_20150313_0013'), ('process', '0022_auto_20150313_1116'), ('process', '0023_auto_20150313_1226'), ('process', '0024_auto_20150313_1609'), ('process', '0025_auto_20150313_1614'), ('process', '0026_auto_20150313_1643'), ('process', '0027_auto_20150313_1645'), ('process', '0028_auto_20150314_2342'), ('process', '0029_auto_20150319_1903'), ('process', '0030_auto_20150328_1034'), ('process', '0031_auto_20150409_1108'), ('process', '0032_auto_20150409_1244'), ('process', '0033_auto_20150409_1528')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDef',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('fieldhelp', models.CharField(max_length=200)),
                ('fieldtype', models.PositiveSmallIntegerField()),
                ('length', models.PositiveSmallIntegerField()),
                ('editable', models.NullBooleanField()),
                ('must', models.NullBooleanField()),
                ('type', models.PositiveSmallIntegerField()),
                ('parent', models.ForeignKey(to='process.FieldDef')),
            ],
        ),
        migrations.CreateModel(
            name='FieldPerstep',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('field', models.ForeignKey(to='process.FieldDef')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessDefinition',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('status', models.PositiveSmallIntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('refering', models.ForeignKey(to='process.ProcessDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('index', models.PositiveSmallIntegerField()),
                ('actiontype', models.PositiveSmallIntegerField()),
                ('process', models.ForeignKey(to='process.ProcessDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='ProcInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('starttime', models.DateTimeField()),
                ('stoptime', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField()),
                ('process', models.ForeignKey(to='process.ProcessDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='PycLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('time', models.DateTimeField()),
                ('action', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RoleDef',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('process', models.ForeignKey(to='process.ProcessDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='RoleInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('entrytime', models.DateTimeField()),
                ('exittime', models.DateTimeField(blank=True, null=True)),
                ('procinst', models.ForeignKey(to='process.ProcInstance', blank=True, null=True)),
                ('role', models.ForeignKey(to='process.RoleDef')),
                ('pycuser', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusScheme',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('remark', models.CharField(max_length=200)),
                ('logic', models.CharField(max_length=200)),
                ('prestep', models.ForeignKey(to='process.ProcessStep', related_name='prestep')),
                ('selfstep', models.ForeignKey(to='process.ProcessStep', related_name='selfstep')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep'),
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='refering',
            field=models.ForeignKey(to='process.ProcessDefinition', null=True),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', null=True),
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='refering',
            field=models.ForeignKey(to='process.ProcessDefinition', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddef',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', null=True),
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='interaction',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', null=True),
        ),
        migrations.RemoveField(
            model_name='fielddef',
            name='editable',
        ),
        migrations.RemoveField(
            model_name='fielddef',
            name='must',
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='parent',
            field=models.ForeignKey(to='process.FieldDef', null=True),
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='parent',
            field=models.ForeignKey(to='process.FieldDef', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processstep',
            name='role',
            field=models.ForeignKey(to='process.RoleDef', null=True),
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='length',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='logic',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='remark',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='statusscheme',
            unique_together=set([('process', 'selfstep', 'prestep')]),
        ),
        migrations.AlterUniqueTogether(
            name='fieldperstep',
            unique_together=set([('step', 'field')]),
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='steps'),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(to='process.ProcessStep', related_name='prestep', null=True),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='selfstep',
            field=models.ForeignKey(to='process.ProcessStep', related_name='selfstep', null=True),
        ),
        migrations.AddField(
            model_name='procinstance',
            name='currentstep',
            field=models.ForeignKey(to='process.ProcessStep', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='fields'),
        ),
        migrations.AlterField(
            model_name='procinstance',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', related_name='instances'),
        ),
        migrations.AlterField(
            model_name='procinstance',
            name='stoptime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='procinstance',
            name='procdata',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='editdefault',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='descript',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='fieldhelp',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fielddef',
            name='type',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='descript',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='version',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='descript',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='roledef',
            name='descript',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.RenameField(
            model_name='fieldperstep',
            old_name='field',
            new_name='field_definition',
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='step_fields'),
        ),
        migrations.AlterUniqueTogether(
            name='fieldperstep',
            unique_together=set([('step', 'field_definition')]),
        ),
        migrations.RenameModel(
            old_name='FieldDef',
            new_name='FieldDefinition',
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='field_perstep'),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(to='process.ProcessStep', related_name='status_prestep', null=True),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='selfstep',
            field=models.ForeignKey(to='process.ProcessStep', related_name='status_thisstep', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='statusscheme',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='parameter',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterModelOptions(
            name='fielddefinition',
            options={'verbose_name_plural': '4. Field Definitions'},
        ),
        migrations.AlterModelOptions(
            name='processdefinition',
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
            model_name='procinstance',
            name='procdata',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='roleinstance',
            name='role',
            field=models.ForeignKey(to='process.RoleDef', related_name='role_instance'),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='prestep',
            field=models.ForeignKey(to='process.ProcessStep', blank=True, null=True, related_name='status_prestep'),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', related_name='steps', null=True),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='actiontype',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.RenameModel(
            old_name='RoleDef',
            new_name='RoleDefinition',
        ),
        migrations.RenameModel(
            old_name='ProcInstance',
            new_name='ProcessInstance',
        ),
        migrations.CreateModel(
            name='Statuslist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('process', models.ForeignKey(to='process.ProcessDefinition', null=True)),
            ],
            options={
                'verbose_name_plural': '3. Status',
            },
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
            field=models.ForeignKey(to='process.Statuslist', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='prestatus',
            field=models.ForeignKey(to='process.Statuslist', blank=True, null=True, related_name='scheme_prestatus'),
        ),
        migrations.AddField(
            model_name='statusscheme',
            name='status',
            field=models.ForeignKey(to='process.Statuslist', related_name='scheme_status', null=True),
        ),
        migrations.RemoveField(
            model_name='processstep',
            name='role',
        ),
        migrations.AlterField(
            model_name='fielddefinition',
            name='fieldtype',
            field=models.PositiveSmallIntegerField(choices=[(0, 'STRING'), (1, 'INTEGER'), (2, 'FLOAT'), (3, 'FINANCE_NUMBER_TBD'), (4, 'DATE'), (5, 'DATETIME'), (6, 'BLOB_TBD'), (7, 'ENUM_TBD')]),
        ),
        migrations.AlterField(
            model_name='fielddefinition',
            name='type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'NORMAL'), (1, 'INTERNAL'), (2, 'JAVASCRIPT_INTERNAL')]),
        ),
        migrations.AlterField(
            model_name='processdefinition',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')]),
        ),
        migrations.AlterField(
            model_name='processinstance',
            name='runstatus',
            field=models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')]),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='actiontype',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'NOT_USED')]),
        ),
        migrations.AlterField(
            model_name='statusscheme',
            name='process',
            field=models.ForeignKey(to='process.ProcessDefinition', related_name='schemes', null=True),
        ),
        migrations.AddField(
            model_name='statuslist',
            name='role',
            field=models.ForeignKey(to='process.RoleDefinition', null=True),
        ),
        migrations.AddField(
            model_name='statuslist',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep', related_name='status_step', null=True),
        ),
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'A. Usergroups',
            },
        ),
        migrations.CreateModel(
            name='UsergroupMember',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pycuser', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('usergroup', models.ForeignKey(to='process.Usergroup', related_name='member_of_group')),
            ],
            options={
                'verbose_name_plural': 'B. Usergroup-Members',
            },
        ),
        migrations.AddField(
            model_name='roledefinition',
            name='usergroup',
            field=models.ForeignKey(to='process.Usergroup', blank=True, null=True),
        ),
    ]
