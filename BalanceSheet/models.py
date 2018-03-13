from __future__ import unicode_literals
from DataExtraction.models import *
from django.contrib.auth.models import User
from django.db import models
from DataExtraction.choices import *


class CompanyBalanceSheetData(models.Model):
    gbc_name = models.ForeignKey(CompanyList)
    section =models.ForeignKey(Section,blank=True,null=True)
    subsection = models.ForeignKey(SubSection,blank=True,null=True)
    s2section =models.ForeignKey(S2Section,blank=True,null=True)
    # s3section =models.ForeignKey(SubSubSubsection,blank=True,null=True)
    q1 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'Quarter_1')
    q2 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'Quarter_2')
    q3 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'Quarter_3')
    q4 = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'Quarter_4')
    lrq = models.ForeignKey(quarter_data,blank=True,null=True, related_name = 'Latest_Reporting_Quarter')
    y1 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'Previous_Year_1')
    y2 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'Previous_Year_2')
    y3 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'Previous_Year_3')
    y4 = models.ForeignKey(year_data,blank=True,null=True, related_name = 'Previous_Year_4')
    tlm = models.ForeignKey(year_data,blank=True,null=True, related_name = 'Previous_Year_5')


    def __str__(self):
        return str(self.subsection.item if self.subsection else self.section.item)

    class Meta:
        verbose_name = ("Balance Sheet data")
        verbose_name_plural = ("Balance Sheet data")
        ordering = ('id',)