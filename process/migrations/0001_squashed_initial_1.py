# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('process', '0001_initial'), ('process',
                                              '0002_rename_step_to_status_scheme'), ('process', '0003_rename_and_add_fields')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDef',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldPerstep',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('field', models.ForeignKey(to='process.FieldDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessDef',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('status', models.PositiveSmallIntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('refering', models.ForeignKey(to='process.ProcessDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('index', models.PositiveSmallIntegerField()),
                ('actiontype', models.PositiveSmallIntegerField()),
                ('process', models.ForeignKey(to='process.ProcessDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcInstance',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('starttime', models.DateTimeField()),
                ('stoptime', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField()),
                ('process', models.ForeignKey(to='process.ProcessDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PycLog',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('action', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleDef',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('process', models.ForeignKey(to='process.ProcessDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleInstance',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('entrytime', models.DateTimeField()),
                ('exittime', models.DateTimeField()),
                ('procinst', models.ForeignKey(to='process.ProcInstance')),
                ('role', models.ForeignKey(to='process.RoleDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusScheme',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('remark', models.CharField(max_length=200)),
                ('logic', models.CharField(max_length=200)),
                ('prestep', models.ForeignKey(
                    related_name='prestep', to='process.ProcessStep')),
                ('selfstep', models.ForeignKey(
                    related_name='selfstep', to='process.ProcessStep')),
                ('name', models.CharField(max_length=20, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fieldperstep',
            name='step',
            field=models.ForeignKey(to='process.ProcessStep'),
            preserve_default=True,
        ),
    ]
