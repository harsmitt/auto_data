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

# @cache_page(60 * 15, key_prefix="site1")
def get_data(req_type=None,c_id=None,section_type=None):
    c_obj = CompanyList.objects.filter(id = c_id)
    data_objs = quarter_data.objects.filter(page_extraction = req_type,company_name=c_id)
    data_list =[]
    qtr_dict = qtr_date_pnl()
    year_dict = year_date(str(c_obj[0].y_end))
    date_list = list(qtr_dict.values())+list(year_dict.values())
    loop_key = qtr_dict
    loop_key.update(year_dict)

    section = Section.objects.filter(i_related=section_type)
    subsection = SubSection.objects.filter(section__in=section)
    s2section = S2Section.objects.filter(subsection__in=subsection)
    #
    # sec_objs = data_objs.filter(subsection=None,s2section=None)
    sec_list =[]
    for sec in section:
        print ("hello"+str(sec))
        sec_d = OrderedDict()
        if sec.item =='Current Liabilities' :
            sec_d['Total Asessts']=[]
            sec_list.append(sec_d)
            sec_d = OrderedDict()
        sub_list=[]
        s2_list=[]
        sub_objs = data_objs.filter(Q(section=sec),~Q(subsection=None),Q(s2section=None))
        s1_sec = subsection.filter(section=sec)
        for sub in s1_sec:
            sub_d = OrderedDict()
            s1_obj = sub_objs.filter(subsection=sub)
            sub_d[sub.item]=get_des(loop_key,s1_obj)
            s2objs = data_objs.filter(Q(section=sec), Q(subsection=sub), ~Q(s2section=None))
            if s2objs:
                s2_sec = s2section.filter(subsection=sub)
                for s2 in s2_sec:
                    s2_d=OrderedDict()
                    s2_obj= s2objs.filter(s2section=s2)
                    s2_d[s2.item] = get_des(loop_key,s2_obj)
                    s2_list.append(s2_d)
                sub_d[sub.item]=s2_list
            sub_list.append(sub_d)
        sec_d[sec.item]=sub_list
        sec_list.append(sec_d)
    if req_type=='bsheet':
        sec_d=OrderedDict()
        sec_d['Total Liablities and equity'] = []
        sec_d['CrosscCheck'] = []
        sec_list.append(sec_d)
    # import pdb;pdb.set_trace()
    data_list.append(sec_list)
    cache_data={req_type:data_list[0],'date_list':date_list,'loop_key':loop_key}
    cache.set(c_id,cache_data,20*20)
    # cache.set(req_type,data_list[0],60*60)
    # cache.set('date_list', date_list,60*60)

    # cache.set('loop_key', loop_key,60*60)
    return data_list[0],date_list,loop_key










