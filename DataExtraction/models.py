from __future__ import unicode_literals

from django.db import models

from .choices import year_end,Comp_type,CountryList,pdf_extraction_page,User_role
from django.contrib.auth.models import User
from Login.models import Team_Sector

class Sector(models.Model):
    sector_name = models.CharField(max_length =1000)
    copy_main = models.BooleanField(default=True)

    def __str__(self):
        return str(self.sector_name)

class SectorDit(models.Model):
    sector =models.ForeignKey(Sector)
    copy_Sector = models.BooleanField(default=True)
    dit_name = models.CharField(max_length =1000)
    dit_code = models.CharField(max_length =200)
    team_sector = models.ForeignKey(Team_Sector, blank=True,null=True)

    def __str__(self):
        return str(self.dit_name)

class Section(models.Model):
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=400, blank=True,null=True)
    i_related = models.CharField(max_length=200,choices=Comp_type)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User,related_name = 'createdby',blank=True,null=True)
    modified_by = models.ForeignKey(User,related_name = 'modifiedby',blank=True,null=True)

    def __str__(self):
        return str(self.item)

class SubSection(models.Model):
    section = models.ForeignKey(Section)
    item = models.CharField(max_length=2000)
    neg_ro = models.BooleanField(default=False)
    is_expense = models.BooleanField(default=False)
    is_income = models.BooleanField(default=False)
    i_synonyms = models.CharField(max_length=2000, blank=True,null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True,null=True)
    i_keyword = models.CharField(max_length =1000,blank=True,null=True)
    i_deduction = models.CharField(max_length=2000, blank=True,null=True)
    added_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, blank=True, null=True, related_name='subsec_Addition')
    modified_by = models.ForeignKey(User, blank=True, null=True, related_name='subsec_Modification')

    def __str__(self):
        return str(self.item)

class S2Section(models.Model):
    subsection = models.ForeignKey(SubSection)
    item = models.CharField(max_length=2000)
    i_synonyms = models.CharField(max_length=2000, blank=True,null=True)
    i_breakdown = models.CharField(max_length=5000, blank=True,null=True)
    i_keyword = models.CharField(max_length=1000, blank=True,null=True)
    i_deduction = models.CharField(max_length=2000, blank=True, null=True)

    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)

class CompanyList(models.Model):
    company_name= models.CharField(max_length=200)
    ditname = models.ForeignKey(SectorDit)
    y_end = models.CharField(max_length=200, choices=year_end, blank=True)
    c_ticker = models.CharField(max_length = 200,blank=True,null=True)
    country = models.CharField(max_length=50,choices = CountryList)
    c_y_unit = models.CharField(max_length = 200,blank=True,null=True)
    c_q_unit=models.CharField(max_length = 200,blank=True,null=True)

    def __str__(self):
        return str(self.company_name)


class DeleteRow(models.Model):
    company_name = models.ForeignKey(CompanyList)
    page_extraction = models.CharField(max_length=200, choices=pdf_extraction_page, blank=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    subsection = models.ForeignKey(SubSection, blank=True, null=True)
    s2section = models.ForeignKey(S2Section, blank=True, null=True)
    quarter_date = models.CharField(max_length=200, blank=True, null=True)
    q1 = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.q1)

class quarter_data(models.Model):
    company_name = models.ForeignKey(CompanyList)
    page_extraction = models.CharField(max_length=200, choices=pdf_extraction_page, blank=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    subsection = models.ForeignKey(SubSection, blank=True, null=True)
    s2section = models.ForeignKey(S2Section, blank=True, null=True)
    quarter_date = models.CharField(max_length=200, blank=True, null=True)
    q1 = models.CharField(max_length=200, blank=True, null=True)
    description =models.CharField(max_length=1000, blank=True, null=True)
    pdf_image_path = models.CharField(max_length=1000,blank=True,null=True)
    pdf_page = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.q1)









