from __future__ import unicode_literals

from django.db import models

Comp_type=(('Balance Sheet','Balance Sheet'),
           ('Profit and Loss','Profit and Loss'),
           )

class Section(models.Model):
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=400, blank=True,null=True)
    i_related = models.CharField(max_length=200,choices=Comp_type)
    added_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.item



class SubSection(models.Model):
    section = models.ForeignKey(Section)
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=2000, blank=True,null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True,null=True)
    i_keyword = models.CharField(max_length =1000,blank=True,null=True)
    i_deduction = models.CharField(max_length=2000, blank=True,null=True)
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item


class S2Section(models.Model):
    subsection = models.ForeignKey(SubSection)
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=2000, blank=True,null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True,null=True)
    i_keyword = models.CharField(max_length=1000, blank=True,null=True)
    i_deduction = models.CharField(max_length=2000, blank=True, null=True)

    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item


class quarter_data(models.Model):
    quarter_date = models.CharField(max_length=200, blank=True, null=True)
    q1 = models.CharField(max_length=200, blank=True, null=True)
    description =models.CharField(max_length=1000, blank=True, null=True)
    pdf_image_path = models.CharField(max_length=1000,blank=True,null=True)
    pdf_page = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.q1

class year_data(models.Model):
    year_date = models.CharField(max_length=200, blank=True, null=True)
    y1 = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    pdf_image_path = models.CharField(max_length=1000, blank=True, null=True)
    pdf_page = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.year_date

class CompanyList(models.Model):
    company_name= models.CharField(max_length=200)
    ditcode = models.CharField(max_length = 200,blank=True,null=True)

    def __str__(self):
        return self.company_name

class GbcData(models.Model):
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
        return self.subsection.item

    class Meta:
        verbose_name = ("Raw data")
        verbose_name_plural = ("Raw data")
        ordering = ('subsection', 's2section')

