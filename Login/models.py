from __future__ import unicode_literals

from django.db import models

from DataExtraction.choices import year_end,Comp_type,CountryList,pdf_extraction_page,User_role
from django.contrib.auth.models import User


class TeamName(models.Model):
    team_name = models.CharField(max_length=100)
    team_lead = models.ForeignKey(User, blank=True,null=True,related_name='TeamLead')

    def __str__(self):
        return str(self.team_name)


class TeamList(models.Model):
    team_name = models.ForeignKey(TeamName,blank=True,null=True)
    t_user    = models.ForeignKey(User,blank=True,null=True,related_name='TeamUser')
    tele_id   = models.CharField(max_length=100,blank=True,null=True)
    u_role    = models.CharField(max_length=200, choices=User_role, blank=True)

    def __str__(self):
        return str(self.t_user.username +' '+self.team_name.team_name +' '+ self.u_role)

class Team_Sector(models.Model):
    sector_code = models.CharField(max_length =100)
    sector_description = models.CharField(max_length =200)
    team = models.ForeignKey(TeamName,blank=True,null=True)

    def __str__(self):
        return str(self.sector_description)



