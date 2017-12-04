from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from .common_functions import *
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin import AdminSite
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse

qtr_dict=qtr_date()
year_dict = year_date()


# class MyAdminSite(AdminSite):

def custom_view(request):
    import pdb;pdb.set_trace()
    sec_obj = Section.objects.filter(id=1)
    sub_obj = SubSection.objects.filter(section=sec_obj)
    s2_obj = S2Section.objects.filter(subsection__in=sub_obj)
    s1 = list(sec_obj) + list(sub_obj) + list(s2_obj)
    print ("mahima")

    return render(request, 'admin/review.html',{'sec_obj':s1})

#     def get_urls(self):
#         from django.conf.urls import url
#         urls = super(MyAdminSite, self).get_urls()
#         urls += [
#             url(r'^admin/custom_view/$', self.admin_view(self.custom_view))
#         ]
#         return urls
#
# admin_site = MyAdminSite()


class SectionForm( forms.ModelForm ):
    i_synonyms = forms.CharField( widget=forms.Textarea )

    class Meta:
        model = Section
        fields = '__all__'

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
    list_display=['subsection','item']

    # def get_queryset(self, obj):
    #     import pdb;
    #     pdb.set_trace()
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

def show_image(request):
    from django.shortcuts import render

    import pdb;pdb.set_trace()
    sec_obj = Section.objects.filter(id=1)
    sub_obj = SubSection.objects.filter(section=sec_obj)
    s2_obj = S2Section.objects.filter(subsection__in=sub_obj)
    s1 = list(sec_obj) + list(sub_obj) + list(s2_obj)
    return render(request, 'admin/review.html',{'obj':s1})

    # pdf_path= request.GET['pdf_path']
    # path = 'http://10.10.0.84/media/'+ pdf_path.split('/')[-3]+'/'+pdf_path.split('/')[-2]+'/'+pdf_path.split('/')[-1]
    # return render(request, 'image.html',{'path':path})

def submit(request):
    obj = GbcData.objects.filter(id=request.GET['obj_id'])
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

    return HttpResponseRedirect('/admin/DataExtraction/gbcdata/')
#
# def reject(request):
#     import pdb;pdb.set_trace()
#     print ("mahima")
#     obj = GbcData.objects.filter(id=request.GET['obj_id'])
#     q1_id = obj[0].q1.id
#     q2_id =obj[0].q2.id
#
#     obj[0].delete()
#     q1_obj = quarter_data.objects.filter(id= q1_id)
#     q1_obj[0].delete()
#     q2_obj = quarter_data.objects.filter(id=q2_id)
#     q2_obj[0].delete()

class QuarterAdmin(admin.ModelAdmin):
    list_display = ["quarter_date",'q1']
    exclude =['pdf_page']

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            """
            Return empty perms dict thus hiding the model from admin index.
            """
            return {}
        else:
            return {'change': True, 'add': True}

    class Meta:
        models =quarter_data

class YearAdmin(admin.ModelAdmin):
    list_display = ["year_date",'y1','description']

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            """
            Return empty perms dict thus hiding the model from admin index.
            """
            return {}
        else:
            return {'change': True, 'add': True}

    class Meta:
        models =quarter_data

def presentation(obj):
    section_obj = S2Section.objects.filter(
        subsection__in=SubSection.objects.filter(section__in=Section.objects.filter(id__in=[1, 2, 3, 4, 5]))).order_by(
        'subsection')




class GBCADMIN(admin.ModelAdmin):
    from django.db.models import Q
    list_display = [ 'gbc_name',"section", "subsection", "s2section",
                    'q1_url','q2_url','q3_url','q4_url','lrq_url','y1_url','y2_url','y3_url','y4_url','button']
    # list_display=['gbc_name',"section"]


    def button(self, obj):

        x = GbcData.objects.filter(gbc_name=obj.gbc_name, section=obj.section, subsection=obj.subsection,
                                     s2section=obj.s2section).order_by('subsection_id')
        if x :
            return mark_safe('<input type="button" value="Verified"/>')
        else:
            return mark_safe('<a href="/submit?obj_id=%s"><input type="button" value="Verify"/></a>') % (obj.id)
    button.short_description = 'Action'
    button.allow_tags = True

    # def button1(self, obj):
    #     return mark_safe('<a href="/reject?obj_id=%s"><input type="button" value="Reject"/></a>') %(obj.id)
    # button.short_description = 'Action2'
    # button.allow_tags = True

    def y1_url(self, obj):
        if obj.y1:
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y1.pdf_image_path,obj.gbc_name.id,obj.y1.y1) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y1.id)

    y1_url.allow_tags = True
    y1_url.short_description = year_dict['y1']

    def y2_url(self, obj):
        if obj.y2:
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y2.pdf_image_path,obj.gbc_name.id,obj.y2.y1) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y2.id)

    y2_url.allow_tags = True
    y2_url.short_description = year_dict['y2']


    def y3_url(self, obj):
        if obj.y3:
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y3.pdf_image_path,obj.gbc_name.id,obj.y3.y1) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y3.id)

    y3_url.allow_tags = True
    y3_url.short_description = year_dict['y3']

    def y4_url(self, obj):
        if obj.y4:
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y4.pdf_image_path,obj.gbc_name.id,obj.y4.y1) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y4.id)

    y4_url.allow_tags = True
    y4_url.short_description = year_dict['y4']


    def q1_url(self, obj):
        if obj.q1:
            # import pdb;pdb.set_trace()
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q1.pdf_image_path,obj.gbc_name.id,obj.q1.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q1.id)

    q1_url.allow_tags = True
    q1_url.short_description = qtr_dict['q1']

    def q2_url(self, obj):
        if obj.q2:
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q2.pdf_image_path,obj.gbc_name.id,obj.q2.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q2.id)
    q2_url.allow_tags = True
    q2_url.short_description = qtr_dict['q2']

    def q3_url(self, obj):
        if obj.q3:
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q3.pdf_image_path,obj.gbc_name.id,obj.q3.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q3.id)
    q3_url.allow_tags = True
    q3_url.short_description = qtr_dict['q3']

    def q4_url(self, obj):
        if obj.q4:
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q4.pdf_image_path,obj.gbc_name.id,obj.q4.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q4.id)
    q4_url.allow_tags = True
    q4_url.short_description = qtr_dict['q4']

    def lrq_url(self, obj):
        if obj.lrq:
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.lrq.pdf_image_path,obj.gbc_name.id,obj.lrq.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.lrq.id)
    lrq_url.allow_tags = True
    lrq_url.short_description = qtr_dict['lrq']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company']

    def company(self, obj):
        if obj:
            # import pdb;pdb.set_trace()
            return('<a href="/admin/DataExtraction/gbcdata/?gbc_name=%s">%s</a>' % (obj.id,obj.company_name) )

    company.allow_tags = True

admin.site.register(Section,SectionAdmin)
admin.site.register(SubSection,SubSectionAdmin)
admin.site.register(S2Section,S2SectionAdmin)
admin.site.register(GbcData,GBCADMIN)
admin.site.register(quarter_data,QuarterAdmin)
admin.site.register(year_data,YearAdmin)
admin.site.register(CompanyList,CompanyAdmin)