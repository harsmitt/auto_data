import json
from django.core.cache import cache
from collections import OrderedDict
from .tranform_data import *
from .utils import *
from django.shortcuts import render

def delete_multiple(request):
    g_data = OrderedDict(request.GET)
    d_data = json.loads(request.GET['delete_data'])
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'
    req_type = 'pnl' if g_data['type'] == 'pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])

    for item in d_data:
        deleted_row = False
        for data in data_list:
            if g_data['section'] in list(data.keys()) and not deleted_row:
                for i in data[g_data['section']]:
                    if not deleted_row:
                        for key, val in i.items():
                            if type(val) != list and key == g_data['subsection']:
                                for d_key, d_val in val.items():
                                    if d_key == item:
                                        i[key].pop(item)
                                        i['update'] = True
                                        deleted_row = True
                                        break;
                            elif key == g_data['subsection'] and g_data['s2section']:
                                for s2sec in val:
                                    for s2, s2_o in s2sec.items():
                                        if s2 == g_data['s2section']:
                                            s2sec[s2].pop(item)
                                            i['update'] = True
                                            deleted_row = True
                                            break;
                    elif deleted_row:
                        break;

            elif deleted_row:
                break;
    data = [i for i in data_list if g_data['section'] in list(i.keys())]
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'], req_type=r_type, action_type='delete',
                                                   p_type=req_type)
    else:
        pass
    if g_data['type'] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())



def save_multiple(request):
    n_data = json.loads(request.GET['new_data'])
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'

    req_type = 'pnl' if g_data['type'] == 'pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    data = data_list
    for row in n_data:
        added_row = False
        new_row = OrderedDict()
        new_row[row[0]] = OrderedDict(zip(list(loop_key.keys()), row[1:]))
        for data in data_list:
            if g_data['section'] in list(data.keys()) and not added_row:
                for i in data[g_data['section']]:
                    if not added_row:
                        for key, val in i.items():
                            if type(val) == OrderedDict and key == g_data['subsection']:
                                i[key].update(new_row)
                                i['update'] = True
                                added_row = True
                                break;
                            elif key == g_data['subsection'] and g_data['s2section']:
                                for s2sec in val:
                                    for s2, s2_o in s2sec.items():
                                        if s2 == g_data['s2section']:
                                            s2sec[s2].update(new_row)
                                            i['update'] = True
                                            added_row = True
                                            break;
                    elif added_row:
                        break;
            elif added_row:
                break;
    data = [i for i in data_list if g_data['section'] in list(i.keys())]
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'], req_type=r_type, p_type=req_type)
    else:
        pass
    # data = save_data(data, request.GET['c_id'],g_data['type'][0])
    if g_data['type'][0] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())



def swap_multiple(request):
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'
    section = Section.objects.filter(i_related=r_type)
    subsection = SubSection.objects.filter(section__in=section)
    s2sec = S2Section.objects.filter(subsection__in=subsection)
    req_type = 'pnl' if g_data['type'] == 'pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    sub_list = list(subsection.filter(s2section=None).values_list('item', flat=True))
    s2_list = list(s2sec.values_list('item', flat=True))
    data = data_list
    s_data = json.loads(request.GET['s_data'])

    for item in s_data:
        remove_item = ''
        add_in_item = False
        if not remove_item:
            for data in data_list:
                if g_data['section'] in list(data.keys()):
                    for i in data[g_data['section']]:
                        for key, val in i.items():
                            if type(val) != list and key == g_data['subsection']:
                                for d_key, d_val in val.items():
                                    if d_key == item:
                                        remove_item = i[key].pop(item)
                                        i['update'] = True
                                        break;
                            elif key == g_data['subsection'] and g_data['s2section']:
                                for s2sec in val:
                                    for s2, s2_o in s2sec.items():
                                        if s2 == g_data['s2section']:
                                            for s2_key, s2_val in s2_o.items():
                                                if s2_key == item:
                                                    remove_item = s2sec[s2].pop(item)
                                                    i['update'] = True
                                                    break;
                                    if remove_item: break;
                        if remove_item: break;
                    data_list, date_list, loop_key = save_data(data, request.GET['c_id'], req_type=r_type,
                                                               action_type='update', p_type=req_type)
                    if remove_item: break;
        if remove_item and not add_in_item:
            for data in data_list:
                if g_data['item'] in sub_list:
                    sub_obj = SubSection.objects.filter(item=g_data['item']).values('section__item', 'item')[0]
                    sec_name = sub_obj['section__item']
                    s2section=''
                else:
                    sub_obj = \
                    S2Section.objects.filter(item=g_data['item']).values('subsection__section__item', 'item')[0]
                    sec_name = sub_obj['subsection__section__item']
                    s2section = sub_obj['item']
                if sec_name in list(data.keys()):
                    for i in data[sec_name]:
                        for key, val in i.items():
                            if type(val) != list and key == g_data['item']:
                                val.update({item: remove_item})
                                i['update'] = True
                                add_in_item = True
                                break;
                            elif type(val) == list and s2section:
                                for s2sec in val:
                                    for s2, s2_o in s2sec.items():
                                        if s2 == g_data['item']:
                                            s2_o.update({item: remove_item})
                                            i['update'] = True
                                            add_in_item = True
                                            # remove_item =s2sec[s2].pop(g_data['existing_sec'][0])
                                            break;
                                    if add_in_item: break;
                        if add_in_item: break;
                    data_list, date_list, loop_key = save_data(data, request.GET['c_id'], req_type=r_type,
                                                               action_type='update', p_type=req_type)
                    if add_in_item: break;

    comp = list(sub_list) + list(s2_list)
    if g_data['type'] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())


def update_dict(data_list, new_row, section, subsec, added_row,s2section=None):
    for data in data_list:
        if section in list(data.keys()) and not added_row:
            for i in data[section]:
                if not added_row:
                    for key, val in i.items():
                        if type(val) == OrderedDict and key == subsec:
                            i[key].update(new_row)
                            i['update'] = True
                            added_row = True
                            break;
                        elif key == subsec and s2section:
                            for s2sec in val:
                                for s2, s2_o in s2sec.items():
                                    if s2 == s2section:
                                        s2sec[s2].update(new_row)
                                        i['update'] = True
                                        added_row = True
                                        break;
                elif added_row:
                    break;
        elif added_row:
            break;

def update_section(request):
    n_data = json.loads(request.GET['new_data'])
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'

    req_type = 'pnl' if g_data['type'] == 'pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    data = data_list
    for subsec , row_data in n_data.items():
        row_data = json.loads(row_data[0]) if row_data else []

        if row_data and type(row_data)==dict:
            for s2sec,r1_data in row_data.items():
                r_data =json.loads(r1_data[0])
                added_row = False
                for row in r_data:
                    row = json.loads(row)
                    new_row = OrderedDict()
                    new_row[row[0]]=OrderedDict(zip(list(loop_key.keys()), row[1:]))
                    update_dict(data_list, new_row, g_data['section'], subsec,added_row,s2sec)
        elif type(row_data)!=dict:
            for row in row_data:
                row = json.loads(row)
                added_row = False
                new_row = OrderedDict()
                new_row[row[0]] = OrderedDict(zip(list(loop_key.keys()), row[1:]))
                # s2section = subsec if  S2Section.objects.filter(subsection__item=subsec) else ''
                update_dict(data_list, new_row, g_data['section'], subsec,added_row)

    data = [i for i in data_list if g_data['section'] in list(i.keys())]
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'], req_type=r_type, p_type=req_type,complete_sec = True,action_type="update")
    else:
        pass
    # data = save_data(data, request.GET['c_id'],g_data['type'][0])
    if g_data['type'][0] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())
