from DataExtraction.models import *
from BalanceSheet.models import *
from PNL.models import CompanyPNLData
from collections import OrderedDict
from DataExtraction.common_files.utils import *
from DataExtraction.common_files.basic_functions import *
from django.db.models import Q
from django.core.cache import cache

# from django.views.decorators.cache import cache_page

def get_des(loop_key,objs):
    des_d =OrderedDict()
    for q_key, q_date in loop_key.items():
        obj_data = objs.filter(quarter_date=q_date)
        des = obj_data[0].description.split('##') if obj_data else []
        for d_obj in des:
            if d_obj:
                if not get_alpha(d_obj) or not get_alpha(d_obj).split(',')[0] in des_d:
                    des_d[get_alpha(d_obj).split(',')[0]] = OrderedDict({q_key: get_digit(d_obj, ui_num=True)})
                else:
                    des_d[get_alpha(d_obj).split(',')[0]][q_key] = get_digit(d_obj, ui_num=True)
            else:
                pass
    return des_d

def get_date_list(c_id):
    if cache.has_key(c_id):
        cache_dict = cache.get(c_id)
        date_list = cache_dict['date_list']
        loop_key = cache_dict['loop_key']
    else:
        c_obj = CompanyList.objects.filter(id=c_id)
        qtr_dict = qtr_date_pnl()
        year_dict = year_date(str(c_obj[0].y_end))
        date_list = list(qtr_dict.values()) + list(year_dict.values())
        loop_key = qtr_dict
        loop_key.update(year_dict)
    return loop_key,date_list


def get_delete_data(c_id=None):
    loop_key, date_list = get_date_list(c_id)
    sec_list = []
    data_objs = DeleteRow.objects.filter(company_name=c_id)
    sec = data_objs.values_list('section__item',flat=True).distinct()
    for sec_obj in sec:
        print ("delete row " + str(sec))
        sec_d = OrderedDict()
        subsec = data_objs.filter(section__item= sec_obj).values_list('subsection__item',flat=True).distinct()
        sub_list = []
        s2_list = []
        for sub in subsec:
            sub_d = OrderedDict()
            s1_obj = data_objs.filter(section__item=sec_obj,subsection__item=sub)
            s2objs = data_objs.filter(Q(section__item=sec_obj), Q(subsection__item=sub), ~Q(s2section=None))
            if s2objs:
                s2_sec = s2objs.filter(subsection__item=sub).values_list('s2section__item',flat=True).distinct()
                for s2 in s2_sec:
                    s2_d = OrderedDict()
                    s2_obj = s2objs.filter(s2section__item=s2)
                    s2_d[s2] = get_des(loop_key, s2_obj)
                    s2_list.append(s2_d)
                sub_d[sub] = s2_list
            else:
                sub_d[sub] = get_des(loop_key, s1_obj)
            sub_list.append(sub_d)
        print (sub_list)
        sec_d[sec_obj] = sub_list
        sec_list.append(sec_d)

    print(sec_list)
    return  sec_list,date_list,loop_key

# @cache_page(60 * 15, key_prefix="site1")
def get_data(req_type=None,c_id=None,section_type=None,o_sec = None):
    loop_key, date_list = get_date_list(c_id)
    data_list = []
    data_objs = quarter_data.objects.filter(page_extraction=req_type, company_name=c_id)
    if cache.has_key(c_id) and o_sec:
        section = Section.objects.filter(i_related=section_type,item=o_sec)
    else:
        section = Section.objects.filter(i_related=section_type)

    sec_list =[]
    for sec in section:
        print ("hello"+str(sec))
        sec_d = OrderedDict()
        sub_list =get_subsec_data(sec,data_objs,loop_key)
        sec_d[sec.item]=sub_list
        sec_list.append(sec_d)
        if sec.item == 'Non-Current Assets' :
            sec_d = OrderedDict()
            sec_d['Total Asessts']=[]
            sec_list.append(sec_d)

        elif sec.item == 'Non-Current Liabilities' :
            sec_d = OrderedDict()
            sec_d['Total Liabilities']=[]
            sec_list.append(sec_d)

        elif sec.item == 'Shareholder Equity' :
            sec_d=OrderedDict()
            sec_d['Total Liablities and equity'] = []
            sec_d['CrosscCheck'] = []
            sec_list.append(sec_d)
        data_list.append(sec_list)
    if cache.has_key(c_id) and o_sec:
        cache_dict = cache.get(c_id)
        x = [ind for ind, i in enumerate(cache_dict[req_type]) if list(i.keys())[0] ==o_sec]
        cache_dict[req_type][x[0]] = data_list[0][0]
        cache_data = {req_type: cache_dict[req_type], 'date_list': date_list, 'loop_key': loop_key}
        data_list = [cache_dict[req_type]]
    else:
        cache_data={req_type:data_list[0],'date_list':date_list,'loop_key':loop_key}

    cache.set(c_id,cache_data,20*20)
    return data_list[0],date_list,loop_key


def get_subsec_data(sec,data_objs,loop_key):
    subsection = SubSection.objects.filter(section=sec)
    s2section = S2Section.objects.filter(subsection__in=subsection)
    sub_list = []
    s2_list = []
    sub_objs = data_objs.filter(Q(section=sec), ~Q(subsection=None), Q(s2section=None))
    s1_sec =subsection
    for sub in s1_sec:
        sub_d = OrderedDict()
        s1_obj = sub_objs.filter(subsection=sub)
        sub_d[sub.item] = get_des(loop_key, s1_obj)
        s2objs = data_objs.filter(Q(section=sec), Q(subsection=sub), ~Q(s2section=None))
        if s2objs:
            s2_sec = s2section.filter(subsection=sub)
            for s2 in s2_sec:
                s2_d = OrderedDict()
                s2_obj = s2objs.filter(s2section=s2)
                s2_d[s2.item] = get_des(loop_key, s2_obj)
                s2_list.append(s2_d)
            sub_d[sub.item] = s2_list
        sub_list.append(sub_d)
    return sub_list








