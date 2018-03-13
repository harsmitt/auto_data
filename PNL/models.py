from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from DataExtraction.models import *


class SectorSection(models.Model):
    sector = models.ForeignKey(Sector)
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=400, blank=True,null=True)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name='pnlcreatedby', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='pnlmodifiedby', blank=True, null=True)

    def __str__(self):
        return str(self.item)


class SectorSubSection(models.Model):
    sector = models.ForeignKey(Sector)
    section = models.ForeignKey(SectorSection)
    item = models.CharField(max_length=2000)
    neg_ro = models.BooleanField(default=False)
    i_synonyms = models.CharField(max_length=2000, blank=True,null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True,null=True)
    i_keyword = models.CharField(max_length =1000,blank=True,null=True)
    i_deduction = models.CharField(max_length=2000, blank=True,null=True)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name='pnlsubcreatedby', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='pnlsubmodifiedby', blank=True, null=True)

    def __str__(self):
        return str(self.item)


class DITSectorSection(models.Model):
    dit = models.ForeignKey(SectorDit)

    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=400, blank=True, null=True)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name='pnlditcreatedby', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='pnlditmodifiedby', blank=True, null=True)

    def __str__(self):
        return str(self.item)


class DITSectorSubSection(models.Model):
    dit = models.ForeignKey(SectorDit)
    section = models.ForeignKey(DITSectorSection)
    item = models.CharField(max_length=2000)
    neg_ro = models.BooleanField(default=False)
    i_synonyms = models.CharField(max_length=2000, blank=True, null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True, null=True)
    i_keyword = models.CharField(max_length=1000, blank=True, null=True)
    i_deduction = models.CharField(max_length=2000, blank=True, null=True)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name='pnlditsubcreatedby', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='pnlditsubmodifiedby', blank=True, null=True)

    def __str__(self):
        return str(self.item)


class CompanyPNLData(models.Model):
    gbc_name = models.ForeignKey(CompanyList)
    section =models.ForeignKey(Section,blank=True,null=True)
    subsection = models.ForeignKey(SubSection,blank=True,null=True)
    s2section =models.ForeignKey(S2Section,blank=True,null=True)
    # s3section =models.ForeignKey(SubSubSubsection,blank=True,null=True)
    q1 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'PNLQtr1')
    q2 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'PNLQtr2')
    q3 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'PNLQtr3')
    q4 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'PNLQtr4')
    lrq = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'PNLLRQ')
    y1 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'PNLyr1')
    y2 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'PNLyr2')
    y3 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'PNLyr3')
    y4 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'PNLyr4')
    tlm = models.ForeignKey(year_data,blank=True,null=True, related_name = 'PNLyr5')


    def __str__(self):
        return str(self.subsection.item if self.subsection else self.section.item)

    class Meta:
        verbose_name = ("PNL data")
        verbose_name_plural = ("PNL data")
        ordering = ('id',)