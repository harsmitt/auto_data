# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-07-17 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_auto_20180717_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team_sector',
            name='team_user',
        ),
        migrations.AddField(
            model_name='team_sector',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.TeamName'),
        ),
    ]