from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from DataExtraction.models import *
from DataExtraction.common_files.basic_functions import *
# from django.utils.safestring import mark_safe
# from django import forms
# from django.contrib.admin import AdminSite
# from django.shortcuts import render
#
# from django.http import HttpResponseRedirect, HttpResponse
qtr_dict=qtr_date(year_end='December')
year_dict = year_date(year_end='December')


def copy_main_subsection(obj):
    sec_obj = Section.objects.filter(i_related='Profit and Loss')
    for s_obj in sec_obj:
        new_obj  = {'sector':obj,'item':obj.sector_name+'##'+s_obj.item,'i_synonyms':s_obj.i_synonyms,'added_date':datetime.now()}
        sector_sec = SectorSection(**new_obj)
        sector_sec.save()

        sub_objs = SubSection.objects.filter(section=s_obj)
        print (len(sub_objs))

        for so in sub_objs:
            new_obj = {'sector': obj,'section':sector_sec, 'item': obj.sector_name + '##' + so.item,
                       'i_synonyms': so.i_synonyms,'i_breakdown':so.i_breakdown,'i_keyword':so.i_keyword,
                       'i_deduction':so.i_deduction,'added_date': datetime.now()}
            sector_subsec = SectorSubSection(**new_obj)
            sector_subsec.save()
    return True

def remove_main_sub(obj):
    sec = SectorSection.objects.filter(sector=obj)
    for i in sec:
        subsec = SectorSubSection.objects.filter(sector=obj,section=i)

        for ob in subsec:
            ob.delete()
        i.delete()
    return True

class SectorSubAdmin(admin.TabularInline):
    model = SectorSubSection
    exclude = ['section','i_deduction','neg_ro']
    readonly_fields = ['item']


class SectorSectionAdmin(admin.TabularInline):
    inlines =[SectorSubAdmin]
    model = SectorSection



class SectorAdmin(admin.ModelAdmin):
    inlines = [SectorSubAdmin]
    def save_model(self, request, obj, form, change):
        if obj.copy_main:
            msg = remove_main_sub(obj)
        else:
            print ("ab function call kro")
            msg = copy_main_subsection(obj)

        obj.save()

    class Meta:
        models =Sector

from django.utils.safestring import mark_safe
class GBCADMIN(admin.ModelAdmin):
    from django.db.models import Q
    list_display = [ 'gbc_name','section','subsection',
                    'q1_url','q2_url','q3_url','q4_url','lrq_url','y1_url','y2_url','y3_url','y4_url']



    def button(self, obj):

        x = CompanyPNLData.objects.filter(gbc_name=obj.gbc_name, section=obj.section, subsection=obj.subsection,
                                     s2section=obj.s2section).order_by('subsection_id')
        if x :
            return mark_safe('<input type="button" value="Verified"/>')
        else:
            return mark_safe('<a href="/submit?obj_id=%s"><input type="button" value="Verify"/></a>') % (obj.id)

    button.short_description = 'Action'
    button.allow_tags = True


    def y1_url(self, obj):
        if obj.y1:
            val = obj.y1.y1 #'(' + str(obj.y1.y1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.y1.y1
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y1.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y1.id)

    y1_url.allow_tags = True
    y1_url.short_description = year_dict['y1']

    def y2_url(self, obj):
        if obj.y2:
            val = obj.y2.y1#'(' + str(obj.y2.y1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.y2.y1
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y2.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y2.id)

    y2_url.allow_tags = True
    y2_url.short_description = year_dict['y2']


    def y3_url(self, obj):
        if obj.y3:
            val = obj.y3.y1#'(' + str(obj.y3.y1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.y3.y1
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y3.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y3.id)

    y3_url.allow_tags = True
    y3_url.short_description = year_dict['y3']

    def y4_url(self, obj):
        if obj.y4:
            val = obj.y4.y1#'(' + str(obj.y4.y1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.y4.y1
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.y4.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/year_data/%d/'>Change</a>" % obj.y4.id)

    y4_url.allow_tags = True
    y4_url.short_description = year_dict['y4']


    def q1_url(self, obj):
        if obj.q1:
            # import pdb;pdb.set_trace()
            val = obj.q1.q1#'('+str(obj.q1.q1)+')' if obj.subsection and obj.subsection.neg_ro else obj.q1.q1
            return ('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q1.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q1.id)

    q1_url.allow_tags = True
    q1_url.short_description = qtr_dict['q1']

    def q2_url(self, obj):
        if obj.q2:
            val = obj.q2.q1#'(' + str(obj.q2.q1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.q2.q1
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q2.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q2.id)
    q2_url.allow_tags = True
    q2_url.short_description = qtr_dict['q2']

    def q3_url(self, obj):
        if obj.q3:
            val = obj.q3.q1#'(' + str(obj.q3.q1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.q3.q1
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q3.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q3.id)
    q3_url.allow_tags = True
    q3_url.short_description = qtr_dict['q3']

    def q4_url(self, obj):
        if obj.q4:
            val = obj.q4.q1#'(' + str(obj.q4.q1) + ')' if obj.subsection and obj.subsection.neg_ro else obj.q4.q1
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.q4.pdf_image_path,obj.gbc_name.id,val) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.q4.id)
    q4_url.allow_tags = True
    q4_url.short_description = qtr_dict['q4']

    def lrq_url(self, obj):
        if obj.lrq:
            return('<a href="/show_image?pdf_path=%s&gbc_name=%s">%s</a>' % (obj.lrq.pdf_image_path,obj.gbc_name.id,obj.lrq.q1) ,
                    "<a target='_blank' href='/admin/DataExtraction/quarter_data/%d/'>Change</a>" % obj.lrq.id)
    lrq_url.allow_tags = True
    lrq_url.short_description = qtr_dict['lrq']


admin.site.register(Sector,SectorAdmin)
# admin.site.register(SubSection)
# admin.site.register(Section)
admin.site.register(SectorDit)
admin.site.register(DITSectorSection)
admin.site.register(DITSectorSubSection)
admin.site.register(SectorSection)
admin.site.register(SectorSubSection)
admin.site.register(CompanyPNLData,GBCADMIN)