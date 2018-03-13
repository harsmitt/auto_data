from DataExtraction.models import *
from BalanceSheet.models import *
from collections import OrderedDict
from DataExtraction.common_files.utils import *
from DataExtraction.common_files.basic_functions import *

def get_company_data(gbc_data):
    data=OrderedDict()
    section = Section.objects.filter(i_related='Balance Sheet')
    subsection = SubSection.objects.filter(section__in=section)
    s2sec = S2Section.objects.filter(subsection__in=subsection)

    for sec in section:
        loop_list = ['q1', 'q2', 'q3', 'q4', 'y1', 'y2', 'y3', 'y4']
        gbc_objs = gbc_data.filter(section=sec)
        obj_d = OrderedDict()
        for obj in gbc_objs:
            inner_d = OrderedDict()
            inn2 = OrderedDict()
            for loop in loop_list:
                if not obj.subsection:
                    if getattr(obj, loop):
                        if not inner_d:
                            inner_d= OrderedDict({loop: getattr(obj, loop).q1} if 'q' in loop else {
                                loop: getattr(obj, loop).y1})
                        else:
                            inner_d[loop] = getattr(obj, loop).q1 if 'q' in loop else getattr(obj, loop).y1

                #
                elif obj.subsection and not obj.s2section:
                    if getattr(obj, loop):
                        des = getattr(obj, loop).description.split('##')
                        des = list(filter(None, des))
                        for d_obj in des:
                            if not get_alpha(d_obj) in inner_d:
                                inner_d[get_alpha(d_obj)] = OrderedDict({loop: get_number(d_obj)} )
                            else:
                                inner_d[get_alpha(d_obj)][loop] = get_number(d_obj)

                else:
                    if getattr(obj, loop):
                        des = getattr(obj, loop).description.split('##')
                        des = list(filter(None, des))
                        for d_obj in des:
                            if not get_alpha(d_obj) in inn2:
                                inn2[get_alpha(d_obj)] = OrderedDict({loop: get_number(d_obj)} )
                            else:
                                inn2[get_alpha(d_obj)][loop] =  get_number(d_obj)


                    # print(inn2)
                    if obj.s2section.item not in inner_d:
                        inner_d[obj.s2section.item] = inn2

                        inner_d['s2sec'] = 1
                    else:
                        inner_d[obj.s2section.item].update(inn2)

            if obj.subsection :
                if obj.subsection.item not in obj_d:
                    obj_d[obj.subsection.item] = inner_d
                else:
                    obj_d[obj.subsection.item].update(inner_d)
            else:
                data[sec.item]=inner_d

        if sec.item not in data:
            data[sec.item] = obj_d
        else:
            data[sec.item].update(obj_d)
    return data


def sub_dict(s_dict):
    sub_d=OrderedDict()
    for i, j in s_dict.items():
        for j1, j2 in j.items():
            if not int(j2)==0:
                if not j1 in sub_d:
                    sub_d[j1] =[i + '(' + str(j2) + ')',j2]
                else:
                    sub_d[j1] = [sub_d[j1][0] + '##' + i + '(' + str(j2) + ')',int(sub_d[j1][1])+int(j2)]
    return sub_d

def s2sec_dict(s2_dict):
    com_dict = OrderedDict()
    for i,j in s2_dict.items():
        s2_d =OrderedDict()
        if i!='s2sec':
            s2_d[i]=sub_dict(j)
        if com_dict:
            com_dict.update(s2_d)
        else:
            com_dict=s2_d
    return com_dict

def delete_old_data(gbc_obj):
    for obj in gbc_obj:
        obj.q1.description=''
        obj.q1.save()
        obj.q2.description = ''
        obj.q2.save()
        obj.q3.description = ''
        obj.q3.save()
        obj.q4.description = ''
        obj.q4.save()
        obj.y1.description = ''
        obj.y1.save()
        obj.y2.description = ''
        obj.y2.save()
        obj.y3.description = ''
        obj.y3.save()
        obj.y4.description = ''
        obj.y4.save()
def update_sub(key,val,obj):
        if 'q' in key:
            new_data = {'description': val[0], 'q1': val[1]}
            o_obj = quarter_data.objects.filter(id=obj.values_list(key, flat=True))
        else:
            new_data = {'description': val[0], 'y1': val[1]}
            o_obj = year_data.objects.filter(id=obj.values_list(key, flat=True))
        o_obj.update(**new_data)

def update_data(data,c_id):
    gbc_obj  =CompanyBalanceSheetData.objects.filter(gbc_name_id=c_id)
    delete_old_data(gbc_obj)
    gbc_obj = CompanyBalanceSheetData.objects.filter(gbc_name_id=c_id)
    for sec, sub in data.items():
        for i,j in sub.items():
            if type(j) != OrderedDict:
                sec_obj = gbc_obj.filter(section__item = sec,subsection=None)
                update_sub(i,j,sec_obj)
            else:
               for j1,j2 in j.items():
                   if type(j2)!=OrderedDict:
                       sub_obj = gbc_obj.filter(section__item = sec,subsection__item=i,s2section=None)
                       update_sub(j1, j2, sub_obj)

                   else:
                       for s1,s2 in j2.items():
                           s2_obj = gbc_obj.filter(section__item=sec, subsection__item=i, s2section__item=j1)
                           update_sub(s1, s2, s2_obj)
    return True

def save_data(data,c_id):
    row_data=OrderedDict()
    for sec,subsec in data.items():
        sub_data=OrderedDict()
        for sub, item in subsec.items():
            if type(item) == OrderedDict and not 's2sec' in item:
                sub_data[sub]= sub_dict(item)
            elif type(item) == OrderedDict and  's2sec' in item:
                sub_data[sub]=s2sec_dict(item)
            else:
                if not sec in row_data:
                    row_data[sec]= OrderedDict({sub:['',item]})
                else:
                    row_data[sec].update(OrderedDict({sub:['',item]}))
        row_data[sec].update(sub_data)
    res = update_data(row_data,c_id)
    gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=c_id)
    data = get_company_data(gbc_data)
    return data

import html
from django.shortcuts import render

def update_comp(request):
    section = Section.objects.filter(i_related='Balance Sheet')
    subsection = SubSection.objects.filter(section__in=section)
    s2sec = S2Section.objects.filter(subsection__in=subsection)

    gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=request.GET['c_id'])

    item = html.unescape(request.GET['item'])
    sub_list = list(SubSection.objects.filter(s2section=None).values_list('item', flat=True))
    s2_list = list(S2Section.objects.values_list('item', flat=True))

    sec = html.unescape(request.GET['section'])
    subsec = html.unescape(request.GET['subsection'])
    exist_sec = html.unescape(request.GET['existing_sec'])
    s2section = html.unescape(request.GET['s2sec']) if 's2sec' in request.GET else ''

    data = get_company_data(gbc_data)

    if not 's2sec' in request.GET:
        remove_item = data[sec][subsec].pop(exist_sec)
        if not len(data[sec][subsec])>=1:
            data[sec].pop(subsec)
    else:
        remove_item = data[sec][subsec][s2section].pop(exist_sec)
        if not len(data[sec][subsec][s2section])>=1:
            data[sec][subsec].pop(s2section)


    if item in sub_list:
        sub_obj = SubSection.objects.filter(item=item).values('section__item', 'item')[0]
        if sub_obj['item'] in data[sub_obj['section__item']]:
            data[sub_obj['section__item']][sub_obj['item']].update(OrderedDict([(exist_sec, remove_item)]))
        else:
            data[sub_obj['section__item']][sub_obj['item']] = OrderedDict([(exist_sec, remove_item)])

    else:

        s2_obj = S2Section.objects.filter(item=item).values('subsection__section__item','subsection__item', 'item')[0]
        if s2_obj['item'] in data[s2_obj['subsection__section__item']][s2_obj['subsection__item']]:
            data[s2_obj['subsection__section__item']][s2_obj['subsection__item']][s2_obj['item']].update(OrderedDict([(exist_sec, remove_item)]))
        else:
            data[s2_obj['subsection__section__item']][s2_obj['subsection__item']][s2_obj['item']] = OrderedDict([(exist_sec, remove_item)])

    comp = list(sub_list) + list(s2_list)
    new_data =save_data(data,request.GET['c_id'])
    return render(request, 'AutomationUI/table_body.html', {'data': new_data, 'comp': comp})

def remake_dict(section,key,data):
    print (data)
    new_data=OrderedDict()
    inner_dict =OrderedDict()
    keys_list = ['q1','q2','q3','q4','y1','y2','y3','y4']
    sec_part = [i for i in data.keys() if key in i]
    # sub_part =
    for i in sec_part:
        inner_dict[i.split('_')[1]]=data[i][0]
    new_data[data['section'][0]]=inner_dict



