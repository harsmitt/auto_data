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

    # def get_queryset(self, obj):
    #
    #     print ("reset")
    #     sec_obj = Section.objects.filter(id=1)
    #     sub_obj = SubSection.objects.filter(section=sec_obj)
    #     s2_obj = S2Section.objects.filter(subsection__in=sub_obj)
    #     s1 = list(sec_obj) + list(sub_obj) + list(s2_obj)
    #
    #     return s1

    def save_model(self, request, obj, form, change):
        obj.i_synonyms = '##'.join(obj.i_synonyms.split('\r\n'))
        obj.save()

    #
class QuarterAdmin(admin.ModelAdmin):
    list_display = ["quarter_date", 'q1']
    exclude = ['pdf_page']

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

class YearAdmin(admin.ModelAdmin):
    list_display = ["year_date", 'y1', 'description']

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



def show_image(request):
    from django.shortcuts import render

    pdf_path= request.GET['pdf_path']
    path = 'http://10.10.0.84/media/'+ pdf_path.split('/')[-3]+'/'+pdf_path.split('/')[-2]+'/'+pdf_path.split('/')[-1]
    return render(request, 'image.html',{'path':path})

# def submit(request):
#     obj = GbcData.objects.filter(id=request.GET['obj_id'])
#     x = obj[0].__dict__
#     x.pop('_state')
#     q1_obj =obj[0].q1.__dict__
#     q1_obj.pop('_state')
#     # q1_new = quarter_data_R(**q1_obj)
#     q1_new.save()
#     q2_obj = obj[0].q2.__dict__
#     q2_obj.pop('_state')
#     q2_new = quarter_data_R(**q2_obj)
#     q2_new.save()
#     new_obj = GbcData_R(**x)
#     new_obj.save()

    # return HttpResponseRedirect('/admin/DataExtraction/gbcdata/')
#
# # def reject(request):
# #     print ("mahima")
# #     obj = GbcData.objects.filter(id=request.GET['obj_id'])
# #     q1_id = obj[0].q1.id
# #     q2_id =obj[0].q2.id
# #
# #     obj[0].delete()
# #     q1_obj = quarter_data.objects.filter(id= q1_id)
# #     q1_obj[0].delete()
# #     q2_obj = quarter_data.objects.filter(id=q2_id)
# #     q2_obj[0].delete()
#

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name','c_ticker','y_end','PNL','BalanceSheet']


    def PNL(self, obj):
        if obj:
            return('<a href="/admin/PNL/companypnldata/?gbc_name=%s">%s</a>' % (obj.id,"Company PNL") )

    PNL.allow_tags = True
    PNL.short_description = "PNL Data"

    def BalanceSheet(self, obj):
        if obj:
           return('<a href="/admin/BalanceSheet/companybalancesheetdata/?gbc_name=%s">%s</a>' % (obj.id,"Company Balance Sheet") )

    BalanceSheet.allow_tags = True

class SectorDitAdmin(admin.ModelAdmin):
    list_display = ['sector','dit_name','dit_code']



#

admin.site.register(CompanyList,CompanyAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(SubSection,SubSectionAdmin)
admin.site.register(S2Section,S2SectionAdmin)
admin.site.register(quarter_data,QuarterAdmin)
admin.site.register(year_data,YearAdmin)
# admin.site.register(Sector)
# admin.site.register(SubSection)
# admin.site.register(Section)
# admin.site.register(SectorDit,SectorDitAdmin)