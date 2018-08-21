# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-27 11:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BalanceSheet', '0002_auto_20180323_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='tlm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_5', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_1', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_2', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_3', to='DataExtraction.quarter_data'),
        ),
        migrations.AlterField(
            model_name='companybalancesheetdata',
            name='y4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_4', to='DataExtraction.quarter_data'),
        ),
    ]