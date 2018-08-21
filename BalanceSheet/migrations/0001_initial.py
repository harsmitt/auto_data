# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-22 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DataExtraction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyBalanceSheetData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gbc_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.CompanyList')),
                ('lrq', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Latest_Reporting_Quarter', to='DataExtraction.quarter_data')),
                ('q1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Quarter_1', to='DataExtraction.quarter_data')),
                ('q2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Quarter_2', to='DataExtraction.quarter_data')),
                ('q3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Quarter_3', to='DataExtraction.quarter_data')),
                ('q4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Quarter_4', to='DataExtraction.quarter_data')),
                ('s2section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.S2Section')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.Section')),
                ('subsection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.SubSection')),
                ('tlm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_5', to='DataExtraction.year_data')),
                ('y1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_1', to='DataExtraction.year_data')),
                ('y2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_2', to='DataExtraction.year_data')),
                ('y3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_3', to='DataExtraction.year_data')),
                ('y4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Previous_Year_4', to='DataExtraction.year_data')),
            ],
            options={
                'verbose_name_plural': 'Balance Sheet data',
                'ordering': ('id',),
                'verbose_name': 'Balance Sheet data',
            },
        ),
    ]
