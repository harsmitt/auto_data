# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Section(models.Model):
    sec = models.CharField(max_length=2000)
    equivalent = models.CharField(max_length=2000, blank=True)
    added_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.sec

class SubSection(models.Model):
    ssection = models.CharField(max_length=2000)
    equivalent = models.CharField(max_length=2000,blank=True)
    added_date = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section)

    def __unicode__(self):
        return self.ssection

class SubSubSection(models.Model):
    sssection = models.CharField(max_length=2000)
    equivalent = models.CharField(max_length=2000,blank=True)
    added_date = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(SubSection)

    def __unicode__(self):
        return self.sssection

class SubSubSubsection(models.Model):
    ssssection = models.CharField(max_length=2000)
    equivalent = models.CharField(max_length=2000,blank=True)
    added_date = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(SubSubSection)

    def __unicode__(self):
        return self.ssssection
