# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-29 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DataExtraction', '0003_delete_year_data'),
        ('PNL', '0005_auto_20180429_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='companypnldata',
            name='q6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr6', to='DataExtraction.quarter_data'),
        ),
        migrations.AddField(
            model_name='companypnldata',
            name='q7',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr7', to='DataExtraction.quarter_data'),
        ),
        migrations.AddField(
            model_name='companypnldata',
            name='q8',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr8', to='DataExtraction.quarter_data'),
        ),
    ]
