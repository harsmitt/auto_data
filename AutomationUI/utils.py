from DataExtraction.models import *
from BalanceSheet.models import *
from PNL.models import CompanyPNLData
from collections import OrderedDict
from DataExtraction.common_files.utils import *
from DataExtraction.common_files.basic_functions import *
from .tranform_data import get_data
from django.db.models import Q
from django.core.cache import cache


# import HTMLParser
# parser = HTMLParser.HTMLParser()
def sub_dict(s_dict):
    sub_d=OrderedDict()
    for i, j in s_dict.items():
        for j1, j2 in j.items():
            if not j2: j2=0
            if j2:
                val = int(j2) if not '.' in str(j2) else float(j2)
                if not val==0:
                    if not j1 in sub_d:
                        sub_d[j1] =[i + '(' + str(val) + ')',val]
                    else:
                        old_val  = int(sub_d[j1][1]) if not '.' in str(sub_d[j1][1]) else float(sub_d[j1][1])
                        sub_d[j1] = [sub_d[j1][0] + '##' + i + '(' + str(val) + ')',old_val+val]
    return sub_d

def del_old_data(sec_objs):
    for obj in sec_objs:
        obj.description =''
        obj.q1=0
        obj.save()


def update_qtr(data,c_id,req_type,action_type=None):
    c_obj = CompanyList.objects.filter(id =c_id).values_list('y_end',flat=True)
    all_objs = quarter_data.objects.filter(company_name_id=c_id,page_extraction=req_type)
    # sec_objs  = all_objs.filter(Q(section__item= list(data.keys())[0]),~Q(subsection=None))
    sec_objs  = all_objs.filter(section__item= list(data.keys())[0],subsection__item__in= list(data[list(data.keys())[0]]))
    if action_type:del_old_data(sec_objs)
    # del_old_data(sec_objs)
    date_objs = qtr_date_pnl()
    date_objs.update(year_date(c_obj[0]))

    for key,obj in data.items():
        for k1, k2 in obj.items():
            if type(k2) != list:
                for des1,des2 in k2.items():
                    q_date = des1
                    if des2:
                        des = str(des2[0])
                        q_sum =int(des2[1]) if not '.' in str(des2) else float(int(des2[1]))
                        sec_o = sec_objs.get(subsection__item=k1, quarter_date=date_objs[q_date])
                        sec_o.description=des
                        sec_o.q1 = q_sum
                        sec_o.save()
            else:
                for s2obj in k2:
                    for s2,s2_obj in s2obj.items():
                        for s2_key ,s2_val in s2_obj.items():
                            if s2_val:
                                q_date = s2_key
                                des = str(s2_val[0])
                                q_sum = int(s2_val[1]) if not '.' in str(s2_val[1]) else float(int(s2_val[1]))
                                sec_o = sec_objs.get(subsection__item=k1, quarter_date=date_objs[q_date],s2section__item =s2)
                                sec_o.description = des
                                sec_o.q1 = q_sum
                                sec_o.save()

        return True


def save_data(data,c_id,req_type,action_type=None,p_type=None,complete_sec=None):
    row_data=OrderedDict()
    for sec,sub_list in data.items():
        sub_data=OrderedDict()
        for subsec in sub_list:
            if "update" in subsec or complete_sec:
                if  "update" in subsec: subsec.pop('update')
                for sub, item in subsec.items():
                    if type(item) != list:
                        sub_data[sub]= sub_dict(item)
                        break;
                    else:
                        s2_data =OrderedDict()
                        s2_list=[]
                        for s2_obj in item:
                            for s2_key,s2_ob in s2_obj.items():
                                s2_data[s2_key] =sub_dict(s2_ob)
                        s2_list.append(s2_data)
                        sub_data[sub]=s2_list
                        break;
            else:
                pass

        row_data[sec]=sub_data
    res = update_qtr(row_data,c_id,req_type=p_type,action_type=action_type)
    # res = delete_qtr(row_data,c_id,req_type = req_type)

    data_list, date_list, loop_key = get_data(req_type=p_type,section_type=req_type, c_id=c_id,o_sec =list(row_data.keys())[0])
    return data_list, date_list, loop_key

from django.shortcuts import render

def update_comp(request):
    add_in_item = False
    g_data = dict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'][0] == 'pnl' else 'Balance Sheet'
    section = Section.objects.filter(i_related=r_type)
    subsection = SubSection.objects.filter(section__in=section)
    s2sec = S2Section.objects.filter(subsection__in=subsection)
    req_type = 'pnl' if g_data['type'][0] == 'pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if  req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    sub_list =list(subsection.filter(s2section=None).values_list('item',flat=True))
    s2_list = list(s2sec.values_list('item', flat=True))
    data=data_list
    remove_item =''
    if not remove_item:
        for data in data_list:
            if g_data['section'][0] in list(data.keys()):
                for i in data[g_data['section'][0]]:
                    for key, val in i.items():
                        if type(val) != list and key == g_data['subsection'][0]:
                            for d_key, d_val in val.items():
                                if d_key == g_data['existing_sec'][0]:
                                    remove_item=i[key].pop(g_data['existing_sec'][0])
                                    i['update']=True
                                    break;
                        elif key == g_data['subsection'][0] and 's2sec' in g_data:
                            for s2sec in val:
                                for s2, s2_o in s2sec.items():
                                    if s2 == g_data['s2sec'][0]:
                                        for s2_key, s2_val in s2_o.items():
                                            if s2_key == g_data['existing_sec'][0]:
                                                remove_item =s2sec[s2].pop(g_data['existing_sec'][0])
                                                i['update']=True
                                                break;
                                if remove_item:break;
                    if remove_item:break;
                data_list, date_list, loop_key = save_data(data, request.GET['c_id'], req_type=r_type,
                                                           action_type='update', p_type=req_type)
                if remove_item: break;
    if remove_item and not add_in_item:
        for data in data_list:
            if g_data['item'][0] in sub_list:
                sub_obj = SubSection.objects.filter(item=g_data['item'][0]).values('section__item', 'item')[0]
                sec_name= sub_obj['section__item']
            else:
                sub_obj = S2Section.objects.filter(item=g_data['item'][0]).values('subsection__section__item', 'item')[0]
                sec_name = sub_obj['subsection__section__item']
            if sec_name in list(data.keys()):
                for i in data[sec_name]:
                    for key, val in i.items():
                        if type(val) != list and key == g_data['item'][0]:
                            val.update({g_data['existing_sec'][0]: remove_item})
                            i['update']=True
                            add_in_item =True
                            break;
                        elif type(val) == list  and 's2sec' in g_data:
                            for s2sec in val:
                                for s2, s2_o in s2sec.items():
                                    if s2 == g_data['item'][0]:
                                        s2_o.update({g_data['existing_sec'][0]: remove_item})
                                        i['update']=True
                                        add_in_item = True
                                        # remove_item =s2sec[s2].pop(g_data['existing_sec'][0])
                                        break;
                                if add_in_item: break;
                    if add_in_item :break;
                data_list, date_list, loop_key = save_data(data, request.GET['c_id'], req_type=r_type,
                                                       action_type='update', p_type=req_type)
                if add_in_item: break;

    comp = list(sub_list) + list(s2_list)
    if g_data['type']== 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())
#
# def remake_dict(section,key,data):
#     print (data)
#     new_data=OrderedDict()
#     inner_dict =OrderedDict()
#     keys_list = ['q1','q2','q3','q4','lrq','y1','y2','y3','y4']
#     sec_part = [i for i in data.keys() if key in i]
#     # sub_part =
#     for i in sec_part:
#         inner_dict[i.split('_')[1]]=data[i][0]
#     new_data[data['section'][0]]=inner_dict
#
#
#
