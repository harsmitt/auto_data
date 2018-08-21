# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-22 10:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DataExtraction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPNLData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gbc_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.CompanyList')),
                ('lrq', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLLRQ', to='DataExtraction.quarter_data')),
                ('q1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr1', to='DataExtraction.quarter_data')),
                ('q2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr2', to='DataExtraction.quarter_data')),
                ('q3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr3', to='DataExtraction.quarter_data')),
                ('q4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLQtr4', to='DataExtraction.quarter_data')),
                ('s2section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.S2Section')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.Section')),
                ('subsection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.SubSection')),
                ('tlm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLyr5', to='DataExtraction.year_data')),
                ('y1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLyr1', to='DataExtraction.year_data')),
                ('y2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLyr2', to='DataExtraction.year_data')),
                ('y3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLyr3', to='DataExtraction.year_data')),
                ('y4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PNLyr4', to='DataExtraction.year_data')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'PNL data',
                'verbose_name_plural': 'PNL data',
            },
        ),
        migrations.CreateModel(
            name='DITSectorSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=2000)),
                ('i_synonyms', models.CharField(blank=True, max_length=400, null=True)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlditcreatedby', to=settings.AUTH_USER_MODEL)),
                ('dit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.SectorDit')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlditmodifiedby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DITSectorSubSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=2000)),
                ('neg_ro', models.BooleanField(default=False)),
                ('i_synonyms', models.CharField(blank=True, max_length=2000, null=True)),
                ('i_breakdown', models.CharField(blank=True, max_length=5000, null=True)),
                ('i_keyword', models.CharField(blank=True, max_length=1000, null=True)),
                ('i_deduction', models.CharField(blank=True, max_length=2000, null=True)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlditsubcreatedby', to=settings.AUTH_USER_MODEL)),
                ('dit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.SectorDit')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlditsubmodifiedby', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PNL.DITSectorSection')),
            ],
        ),
        migrations.CreateModel(
            name='SectorSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=2000)),
                ('i_synonyms', models.CharField(blank=True, max_length=400, null=True)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlcreatedby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlmodifiedby', to=settings.AUTH_USER_MODEL)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.Sector')),
            ],
        ),
        migrations.CreateModel(
            name='SectorSubSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=2000)),
                ('neg_ro', models.BooleanField(default=False)),
                ('i_synonyms', models.CharField(blank=True, max_length=2000, null=True)),
                ('i_breakdown', models.CharField(blank=True, max_length=5000, null=True)),
                ('i_keyword', models.CharField(blank=True, max_length=1000, null=True)),
                ('i_deduction', models.CharField(blank=True, max_length=2000, null=True)),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlsubcreatedby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnlsubmodifiedby', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PNL.SectorSection')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataExtraction.Sector')),
            ],
        ),
    ]
