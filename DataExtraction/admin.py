from __future__ import unicode_literals

from django.contrib import admin
from BalanceSheet.models import *
from DataExtraction.common_files.basic_functions import *
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin import AdminSite
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
#
class SectionForm( forms.ModelForm ):
    i_synonyms = forms.CharField( widget=forms.Textarea )

    class Meta:
        model = Section
        fields = '__all__'
#
class SectionAdmin( admin.ModelAdmin ):
    form = SectionForm

    def save_model(self, request, obj, form, change):
        obj.i_synonyms = '##'.join(obj.i_synonyms.split('\r\n'))
        obj.save()


class SubSectionForm(forms.ModelForm):
    i_synonyms = forms.CharField(widget=forms.Textarea)
    i_breakdown =forms.CharField(widget=forms.Textarea)

    class Meta:
        model = SubSection
        fields = '__all__'


class SubSectionAdmin(admin.ModelAdmin):
    form = SubSectionForm

    def save_model(self, request, obj, form, change):
        obj.i_synonyms = '##'.join(obj.i_synonyms.split('\r\n'))
        obj.save()

class S2SectionForm(forms.ModelForm):
    i_synonyms = forms.CharField(widget=forms.Textarea)
    i_breakdown = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = S2Section
        fields = '__all__'

class S2SectionAdmin(admin.ModelAdmin):
    form = S2SectionForm
    list_display = ['subsection', 'item']

    def save_model(self, request, obj, form, change):
        obj.i_synonyms = '##'.join(obj.i_synonyms.split('\r\n'))
        obj.save()

    #
class QuarterAdmin(admin.ModelAdmin):
    list_display = ['company_name','page_extraction','section','subsection','s2section','q_obj']
    exclude = ['pdf_page']

    def q_obj(self,obj):
        return ("<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" %obj.id)

    q_obj.allow_tags = True

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            """
            Return empty perms dict thus hiding the model from admin index.
            """
            return {}
        else:
            return {'change': True, 'add': True}

    class Meta:
        models = quarter_data

# def show_image(request):
#     from django.shortcuts import render
#
#     pdf_path= request.GET['pdf_path']
#     path = 'http://10.10.0.84/media/'+ pdf_path.split('/')[-3]+'/'+pdf_path.split('/')[-2]+'/'+pdf_path.split('/')[-1]
#     return render(request, 'image.html',{'path':path})

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name','c_ticker','y_end','PNL','BalanceSheet']


    def PNL(self, obj):
        if obj:
            return('<a href="/admin/DataExtraction/quarter_data/?company_name=%s&&page_extraction=pnl">%s</a>' % (obj.id,"Company PNL") )

    PNL.allow_tags = True
    PNL.short_description = "PNL Data"

    def BalanceSheet(self, obj):
        if obj:
           return('<a href="/admin/DataExtraction/quarter_data/?company_name=%s&&page_extraction=bsheet">%s</a>' % (obj.id,"Company Balance Sheet") )

    BalanceSheet.allow_tags = True
    BalanceSheet.short_description = "BalanceSheet Data"

class SectorDitAdmin(admin.ModelAdmin):
    list_display = ['sector','dit_name','dit_code']


admin.site.register(CompanyList,CompanyAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(SubSection,SubSectionAdmin)
admin.site.register(S2Section,S2SectionAdmin)
admin.site.register(quarter_data,QuarterAdmin)