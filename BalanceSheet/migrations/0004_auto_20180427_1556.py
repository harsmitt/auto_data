# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-27 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BalanceSheet', '0003_auto_20180427_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companybalancesheetdata',
            name='tlm',
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='lrq',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lrq', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Year_1', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Year_2', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Year_3', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Year_4', to='DataExtraction.quarter_data'),
        ),
    ]
