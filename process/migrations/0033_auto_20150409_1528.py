# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('process', '0032_auto_20150409_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'verbose_name_plural': 'A. Usergroups',
            },
        ),
        migrations.CreateModel(
            name='UsergroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pycuser', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('usergroup', models.ForeignKey(related_name='member_of_group', to='process.Usergroup')),
            ],
            options={
                'verbose_name_plural': 'B. Usergroup-Members',
            },
        ),
        migrations.AddField(
            model_name='roledefinition',
            name='usergroup',
            field=models.ForeignKey(blank=True, to='process.Usergroup', null=True),
        ),
    ]
