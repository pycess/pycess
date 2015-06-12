# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(blank=True, max_length=200)),
                ('fieldhelp', models.CharField(blank=True, max_length=200)),
                ('fieldtype', models.PositiveSmallIntegerField(choices=[(0, 'STRING'), (1, 'INTEGER'), (2, 'FLOAT'), (3, 'FINANCE_NUMBER_TBD'), (4, 'DATE'), (5, 'DATETIME'), (6, 'BLOB_TBD'), (7, 'ENUM_TBD')])),
                ('length', models.PositiveSmallIntegerField(default=1)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'NORMAL'), (1, 'INTERNAL'), (2, 'JAVASCRIPT_INTERNAL')], default=0)),
                ('parent', models.ForeignKey(blank=True, null=True, to='process.FieldDefinition')),
            ],
            options={
                'verbose_name_plural': '5. Field Definitions',
            },
        ),
        migrations.CreateModel(
            name='FieldPerstep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction', models.PositiveSmallIntegerField(default=0)),
                ('parameter', models.TextField(default='{}')),
                ('editdefault', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('field_definition', models.ForeignKey(to='process.FieldDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(blank=True, max_length=200)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')])),
                ('version', models.PositiveSmallIntegerField(default=1)),
                ('refering', models.ForeignKey(blank=True, null=True, to='process.ProcessDefinition')),
            ],
            options={
                'verbose_name_plural': '1. Process Definitions',
            },
        ),
        migrations.CreateModel(
            name='ProcessInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procdata', models.TextField(default='{}')),
                ('starttime', models.DateTimeField()),
                ('stoptime', models.DateTimeField(null=True)),
                ('runstatus', models.PositiveSmallIntegerField(choices=[(0, 'PLANNED'), (1, 'IN_DEVELOPMENT'), (2, 'USABLE'), (3, 'ACTIVE'), (4, 'DEPRECATED'), (5, 'DISABLED')])),
            ],
            options={
                'verbose_name_plural': '7. Process Instances',
            },
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(blank=True, max_length=200)),
                ('index', models.PositiveSmallIntegerField(default=0)),
                ('actiontype', models.PositiveSmallIntegerField(choices=[(0, 'NOT_USED')], default=0)),
                ('process', models.ForeignKey(null=True, related_name='steps', to='process.ProcessDefinition')),
            ],
            options={
                'verbose_name_plural': '2. Process Steps',
            },
        ),
        migrations.CreateModel(
            name='PycessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('action', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RoleDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(blank=True, max_length=200)),
                ('process', models.ForeignKey(to='process.ProcessDefinition')),
            ],
            options={
                'verbose_name_plural': '6. Role Definitions',
            },
        ),
        migrations.CreateModel(
            name='RoleInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrytime', models.DateTimeField()),
                ('exittime', models.DateTimeField(blank=True, null=True)),
                ('procinst', models.ForeignKey(blank=True, null=True, to='process.ProcessInstance')),
                ('pycuser', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(related_name='role_instance', to='process.RoleDefinition')),
            ],
            options={
                'verbose_name_plural': '9. Role Instances',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('process', models.ForeignKey(null=True, related_name='status_list', to='process.ProcessDefinition')),
                ('role', models.ForeignKey(null=True, to='process.RoleDefinition')),
                ('step', models.ForeignKey(null=True, related_name='status_step', to='process.ProcessStep')),
            ],
            options={
                'verbose_name_plural': '3. Status',
            },
        ),
        migrations.CreateModel(
            name='StatusTransition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('remark', models.CharField(blank=True, max_length=200)),
                ('logic', models.CharField(blank=True, max_length=200)),
                ('prestatus', models.ForeignKey(blank=True, null=True, related_name='scheme_prestatus', to='process.Status')),
                ('process', models.ForeignKey(null=True, related_name='schemes', to='process.ProcessDefinition')),
                ('status', models.ForeignKey(null=True, related_name='scheme_status', to='process.Status')),
            ],
            options={
                'verbose_name_plural': '4. Status Transitions',
            },
        ),
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pycuser', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('usergroup', models.ForeignKey(related_name='member_of_group', to='process.Usergroup')),
            ],
            options={
                'verbose_name_plural': 'B. Usergroup-Members',
            },
        ),
        migrations.AddField(
            model_name='roledefinition',
            name='usergroup',
            field=models.ForeignKey(blank=True, null=True, to='process.Usergroup'),
        ),
        migrations.AddField(
            model_name='processinstance',
            name='currentstatus',
            field=models.ForeignKey(blank=True, null=True, to='process.Status'),
        ),
        migrations.AddField(
            model_name='processinstance',
            name='process',
            field=models.ForeignKey(related_name='instances', to='process.ProcessDefinition'),
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(related_name='field_perstep', to='process.ProcessStep'),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='process',
            field=models.ForeignKey(null=True, to='process.ProcessDefinition'),
        ),
        migrations.AlterUniqueTogether(
            name='status',
            unique_together=set([('process', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='fieldperstep',
            unique_together=set([('step', 'field_definition')]),
        ),
    ]
