# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200)),
                ('fldhelp', models.CharField(max_length=200)),
                ('fldtype', models.PositiveSmallIntegerField()),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.ForeignKey(to='process.FieldDef')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessDef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='StepScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remark', models.CharField(max_length=200)),
                ('logic', models.CharField(max_length=200)),
                ('prestep', models.ForeignKey(related_name='prestep', to='process.ProcessStep')),
                ('selfstep', models.ForeignKey(related_name='selfstep', to='process.ProcessStep')),
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
