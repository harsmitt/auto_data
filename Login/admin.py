from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class TeamListAdmin(admin.ModelAdmin):
    list_display = ['t_user','u_role']
    list_filter =['t_user','u_role']
    search_fields = ('t_user',)
    def get_queryset(self, request):
        qs = super(TeamListAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            from Login.models import TeamName
            x = TeamName.objects.filter(team_lead__username=request.user)
            if x:
                return  qs.filter(team_name__in=x)
            else:
                return qs


class TeamSectorAdmin(admin.ModelAdmin):
    list_display = ['sector_code','sector_description']
    list_filter =['sector_code','sector_description']
    def get_queryset(self, request):
        qs = super(TeamSectorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            from Login.models import TeamName
            x = TeamName.objects.filter(team_lead__username=request.user)
            if x:
                return  qs.filter(team__in=x)
            else:
                return qs


##login module
admin.site.register(TeamName),
admin.site.register(TeamList,TeamListAdmin),
admin.site.register(Team_Sector,TeamSectorAdmin),


