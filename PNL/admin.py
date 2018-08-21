from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from DataExtraction.models import *
from DataExtraction.common_files.basic_functions import *
from .keywords_handling import *

qtr_dict=qtr_date(year_end='December')
year_dict = year_date(year_end='December')

from django import forms

class SectorSubSectionForm(forms.ModelForm):
    i_synonyms = forms.CharField(widget=forms.Textarea)
    i_breakdown =forms.CharField(widget=forms.Textarea)

    class Meta:
        model = SectorSubSection
        fields = '__all__'
from django.utils.safestring import mark_safe


class SectorSubAdmin(admin.TabularInline):
    model = SectorSubSection
    exclude =('section','item','neg_ro','is_expense','is_income','i_synonyms','i_breakdown','i_keyword','i_deduction','added_date','added_by','modified_by')
    readonly_fields = ['link']

    def link(self, obj):
        # url = reverse(...)
        return mark_safe("<a href='/admin/PNL/sectorsubsection/%s'>%s</a>" % (obj.id,obj.item.split('##')[-1]))

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True


class SectorSectionAdmin(admin.TabularInline):
    inlines =[SectorSubAdmin]
    model = SectorSection

class SectorSubSectionAdmin(admin.ModelAdmin):
    form = SectorSubSectionForm

    # def save_model(self, request, obj, form, change):
    #     obj.i_synonyms = '##'.join(obj.i_synonyms.split('\r\n'))
    #     obj.save()

class DITSectorSectionAdmin(admin.TabularInline):
    inlines = [SectorSubAdmin]
    model=DITSectorSection

class SectorAdmin(admin.ModelAdmin):
    readonly_fields = ('sector_name',)
    inlines = [SectorSubAdmin]
    search_fields = ('sector_name',)

    def get_queryset(self, request):
        qs = super(SectorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            from Login.models import TeamName
            x = TeamName.objects.filter(team_lead__username=request.user)
            sectors = SectorDit.objects.filter(team_sector__team__in=x).values_list('sector_id',flat=True).distinct()
            if x:
                return  qs.filter(id__in=sectors)
            else:
                return qs

    def save_model(self, request, obj, form, change):
        if obj.copy_main:
            msg = remove_main_sub(obj)
        else:
            msg = copy_main_subsection(obj)

        obj.save()

    class Meta:
        models =Sector



class SectorDitAdmin(admin.ModelAdmin):
    list_display = ['sector','dit_name','dit_code']

    search_fields = ('dit_name', 'dit_code',)
    # exclude =['copy_Sector']

    def get_queryset(self, request):
        qs = super(SectorDitAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            from Login.models import TeamName
            x = TeamName.objects.filter(team_lead__username=request.user)
            if x:
                return  qs.filter(team_sector__team__in=x)
            else:
                return qs

    def save_model(self, request, obj, form, change):
        if obj.copy_Sector:
            msg = remove_main_sub(obj)
        else:
            msg = copy_main_subsection(obj)

        obj.save()

    class Meta:
        models = SectorDit



admin.site.register(Sector,SectorAdmin)
admin.site.register(SectorDit,SectorDitAdmin)

# admin.site.register(SubSection)
# admin.site.register(Section)

admin.site.register(DITSectorSection)

admin.site.register(DITSectorSubSection)
admin.site.register(SectorSection)
admin.site.register(SectorSubSection,SectorSubSectionAdmin)
# admin.site.register(CompanyPNLData,GBCADMIN)