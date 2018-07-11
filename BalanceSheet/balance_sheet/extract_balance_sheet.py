import re
from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from collections import OrderedDict
import copy
import itertools

from .without_sections import without_sections
from DataExtraction.common_files.utils import get_page_content,remove_extra_keys

pass_list = ['LIABILITIES AND', ]
def ExtractBalnceSheet(**kwargs):
    try:
        res = False
        last_notes_no=0
        data_dict = copy.deepcopy(kwargs['data_dict'])
        if not 'page_2' in kwargs:
            data_dict , res = check_pattern(data = kwargs['data'][kwargs['date_line']:],data_dict = data_dict,
                                        ignore_index=kwargs['ignore_index'],date_obj = kwargs['date_obj'])
        if not res:
            for l_num, line in enumerate(kwargs['data'][kwargs['date_line']:]):

                if l_num > 10 and len(data_dict) < 2 and data_dict :
                   d_keys =list(data_dict.keys())[-1]
                   if not any(key in d_keys for key in  ['current assets','current liabilities','stockholders equity']):
                    break;
                print (line)
                l_check = line if line and line.strip()[-1].isalpha() else line and line.replace('-', '').strip()

                if not kwargs['unit'] and line and any(word in line.lower() for word in ['millions', 'thousands']):
                    print (line)
                    x = [w1 for word in line.lower().split() for w1 in ['millions', 'thousands'] if w1 in word]
                    print (x)
                    kwargs['unit'] = x[0] if x else ''

                elif data_dict and data_dict[list(data_dict.keys())[-1]] == []:
                    data_dict[list(data_dict.keys())[-1]] = OrderedDict()

                elif all(word in line.lower() for word in ['total liabilities','and'] ):
                    d_keys = list(data_dict.keys())
                    if all(key in d_keys for key in ['current assets', 'current liabilities', 'stockholders equity']):
                        return data_dict,kwargs['unit']

                elif not 'page_2' in kwargs and (('continue' in line.lower() and len(kwargs['data'])-l_num<5 ) or (l_num+kwargs['date_line']+2 == len(kwargs['data'][kwargs['date_line']:]) and any(word in line for word in ['total assets' ,'total liabilities','continued','net current asset']))):
                    data = get_page_content(seprator='@@',page = kwargs['page'], path=kwargs['path'], file=kwargs['file'])
                    data_dict,kwargs['unit'] = ExtractBalnceSheet(unit=kwargs['unit'],page_2 = True,date_line =2,data_dict=data_dict,data=data,ignore_index=kwargs['ignore_index'],date_obj=kwargs['date_obj'])
                    return data_dict,kwargs['unit']

                elif not 'page_2' in kwargs and data_dict and not all(keys in list(data_dict.keys()) for keys in ['current assets','current liabilities','stockholders equity'])\
                    and l_num+kwargs['date_line']+1 == len(kwargs['data']):

                    data = get_page_content(seprator='@@', page=kwargs['page'], path=kwargs['path'],
                                            file=kwargs['file'])
                    data_dict,kwargs['unit'] = ExtractBalnceSheet(unit=kwargs['unit'],page_2 = True,date_line=0, data_dict=data_dict, data=data,
                                                   ignore_index=kwargs['ignore_index'], date_obj=kwargs['date_obj'])
                    return data_dict,kwargs['unit']

                elif not 'page_2' in kwargs and data_dict and l_num+kwargs['date_line']+1 == len(kwargs['data']):
                    d_keys= list(data_dict.keys())
                    if not any(key for key in list(data_dict[d_keys[-1]].keys()) if all(word in key for word in ['total','equity'])):

                        data = get_page_content(seprator='@@', page=kwargs['page'], path=kwargs['path'],
                                                file=kwargs['file'])
                        data_dict,kwargs['unit'] = ExtractBalnceSheet(unit=kwargs['unit'],page_2=True, date_line=0, data_dict=data_dict, data=data,
                                                   ignore_index=kwargs['ignore_index'], date_obj=kwargs['date_obj'])
                        return data_dict,kwargs['unit']
                    else:
                        pass


                elif (len(re.split('  +',l_check)) < 2 and alpha_there(l_check)) or \
                        (len(re.split('  +',l_check)) == 2 and not num_there((re.split('  +',l_check)[-1]))) or\
                        (len(re.split('  +', l_check)) ==2 and num_there(line) and not alpha_there(line))\
                        or any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +',line)[0]) in k):
                    # pass_list = ['LIABILITIES AND', ]

                    # Add main key in data dict
                    # if any(i.lower() in line.lower() for i in pass_list) and not num_there(line):
                    #     pass;

                    if any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +',line)[0]) in k):
                        key_name = (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +',line)[0]) in k))
                        if key_name in data_dict:
                            x = list(data_dict.keys())
                            if data_dict[key_name]:
                                if x[-1] == key_name:#data_dict[key_name]:
                                    pass
                                elif x[-1] != key_name and len(data_dict[key_name])==1:
                                    del data_dict[key_name]
                                    data_dict[key_name] = OrderedDict()
                            else :
                                del data_dict[key_name]
                                data_dict[key_name]=OrderedDict()
                        else:
                            data_dict[next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +',line)[0]) in k)] = OrderedDict()

                    elif len(kwargs['data']) > l_num + 1 and any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line+ ' '+str(kwargs['data'][l_num+1])) in k):

                        if (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line+ ' ' +str(kwargs['data'][l_num+1])) in k)) in data_dict:
                            pass
                        else:
                            data_dict[next(
                                v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line+' '+ str(kwargs['data'][l_num+1])) in k)] = OrderedDict()

                    # if main key already defined in data_dict
                    elif data_dict:
                        if len(kwargs['data']) > l_num + 1 and (':' in (kwargs['data'][l_num] + ' ' + kwargs['data'][l_num + 1])[-1])\
                                and data_dict[list(data_dict.keys())[-1]] in [[],{}]:
                            pass


                        elif num_there(line) and not alpha_there(line):
                            values = list(filter(lambda name: num_there(name), line.split()))
                            if kwargs['ignore_index']:
                                values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                            ignore_index=kwargs['ignore_index'],
                                                                            data=kwargs['data'],date_obj = kwargs['date_obj'])
                            val = list(map(lambda x: str(get_digit(x)), values))
                            dict1 = list(zip(kwargs['date_obj'], val))
                            for d1 in data_dict:
                                for key in data_dict[d1]:
                                    if data_dict[d1][key] in [[], {}] and key not in ['non current assets',
                                                                                      'non current liabilities']:
                                        data_dict[d1][key] = dict1

                        elif alpha_there(line) and line.split()[0].split('-')[0].istitle() and not check_datetime(line.split()[0]):
                            new_key = get_alpha(line,key=True)
                            old_dict = data_dict[list(data_dict.keys())[-1]]
                            if old_dict and old_dict[list(old_dict.keys())[-1]] in [[],{}]:
                                old_dict[new_key] = old_dict.pop(list(old_dict.keys())[-1])
                            else:
                                if data_dict[list(data_dict.keys())[-1]] in [[], {}]:
                                    data_dict[list(data_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})
                                else:
                                    for d1 in data_dict:
                                        for key in data_dict[d1]:
                                            if data_dict[d1][key] in [[], {}] and key not in list(
                                                    itertools.chain(*mapping_dict.key_mapping_dict.keys())):
                                                data_dict[d1][key] = OrderedDict()
                                            else:
                                                data_dict[list(data_dict.keys())[-1]][new_key] = OrderedDict()

                elif len(re.split('  +', line)) > 2 and kwargs['date_obj']:

                    values = re.split('  +', line)
                    pattern = re.compile('[(|)-]')
                    key_name = get_alpha(values[0],key=True)

                    if any('%' in i for i in values[1:]):
                        return False

                    if key_name in ['assets','liabilities']:
                        line = kwargs['data'][l_num-1]+' '+line
                        values = re.split('  +', line)


                    # this loop executes when 'total' exist in key then we add a new key in data dict
                    # mentioned in mapping dict for that `total ` key
                    # todo ignore_index concept
                    elif data_dict and not alpha_there(line) and data_dict[list(data_dict.keys())[-1]] in [[],{}]:
                        old_dict = list(data_dict.keys())[-1]
                        if (next(v for k, v in mapping_dict.key_mapping_dict.items() if old_dict in k)) in data_dict:
                            pass


                    elif data_dict and  pattern.split(key_name)[0] in [i for i in
                                                      list(itertools.chain(*mapping_dict.key_mapping_dict.keys())) if
                                                      'total' in i]:
                        new_key = key_name
                        if kwargs['ignore_index']:
                            values,last_notes_no = remove_ignore_index(values, last_notes_no, ignore_index=kwargs['ignore_index'],
                                                         data=kwargs['data'],date_obj = kwargs['date_obj'])
                        new_values = list(filter(lambda num: num_there(num), values[1:]))
                        val = list(map(lambda x: str(get_digit(x)), new_values))
                        data_dict[list(data_dict.keys())[-1]][new_key] = list(zip(kwargs['date_obj'], val))

                        data_dict[
                            next(v for k, v in mapping_dict.key_mapping_dict.items() if
                                 pattern.split(key_name)[0] in k)] = OrderedDict()

                    # zip these values[1:] with date and add new
                    # component in data_dict
                    elif data_dict:
                        # todo ignore_index concept
                        new_key = values[0]
                        if (new_key.split()[0].split('-')[0].istitle()or new_key.split()[0][0].split('-')[0].istitle()) and not check_datetime(new_key.split()[0]):

                            if kwargs['ignore_index']:
                                values,last_notes_no = remove_ignore_index(values,last_notes_no,date_obj = kwargs['date_obj'],ignore_index=kwargs['ignore_index'],data=kwargs['data'])
                            new_values = list(filter(lambda num: num_there(num), values[1:]))
                            val = list(map(lambda x: str(get_digit(x)), new_values))
                            if data_dict[list(data_dict.keys())[-1]]:
                                blank_check = data_dict[list(data_dict.keys())[-1]]
                                if not blank_check[list(blank_check.keys())[-1]]:
                                    blank_check.pop(list(blank_check.keys())[-1])

                            data_dict[list(data_dict.keys())[-1]][get_alpha(new_key,key=True)] = \
                            list(zip(kwargs['date_obj'], val))
                        else:
                            if kwargs['ignore_index']:
                                values,last_notes_no = remove_ignore_index(values, last_notes_no, ignore_index=kwargs['ignore_index'],
                                                             data=kwargs['data'],date_obj=kwargs['date_obj'])
                            new_values = list(filter(lambda num: num_there(num), values[1:]))
                            val = map(lambda x: str(get_digit(x)), new_values)
                            old_dict = data_dict[list(data_dict.keys())[-1]]
                            if old_dict and not old_dict[list(old_dict.keys())[-1]]:
                                old_dict[list(old_dict.keys())[-1]] =\
                                    list(zip(kwargs['date_obj'], val))
                            elif not data_dict[list(data_dict.keys())[-1]]:
                                data_dict[list(data_dict.keys())[-1]]= \
                                list(zip(kwargs['date_obj'], val))
                            # data_dict[key_name] = list(zip(kwargs['date_obj'], val))

                # elif data_dict:
                #     pass
            data_dict = remove_extra_keys(data_dict =data_dict)

            return data_dict,kwargs['unit']
        else:
            data_dict = remove_extra_keys(data_dict=data_dict)
            return data_dict,kwargs['unit']

    except Exception as e:
        return e


def remove_ignore_index(values,last_notes_no,**kwargs):
    try:
        values = [i for i in values if i != '$']
        ignore_index = list(kwargs['ignore_index'].values())
        ignore_index.sort()
        if 'notes' in kwargs['ignore_index']:
            current_notes = values[kwargs['ignore_index']['notes']] if kwargs['ignore_index']['notes'] < len(values) else ''
            if not get_digit(current_notes,num=True) :# (last_notes_no and not (len(last_notes_no) == len(current_notes))) or
                ignore_index.remove(kwargs['ignore_index']['notes'])
            elif len(values) == len(kwargs['date_obj']) + len(kwargs['ignore_index']) + 1:
                last_notes_no = current_notes if current_notes else last_notes_no

            elif len(values) != len(kwargs['date_obj']) + len(kwargs['ignore_index']) + 1:
                return values, last_notes_no
        for i in ignore_index:
            del values[i]
        return values,last_notes_no
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return e


def check_pattern(**kwargs):
    line0 = kwargs['data'][0]
    next_line1 = kwargs['data'][1]
    next_line2 = kwargs['data'][2]
    next_line3 = kwargs['data'][3]
    next_line4 = kwargs['data'][4]
    for line in [line0,next_line1,next_line2,next_line3,next_line4]:
        if any(i.lower() in line.lower() for i in pass_list) and not num_there(line):
            pass;
        elif any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +', line)[0]) in k):
            return kwargs['data_dict'] , False
    # else:
    data_dict = without_sections(data = kwargs['data'],data_dict = kwargs['data_dict']
                                 ,ignore_index=kwargs['ignore_index'],date_obj = kwargs['date_obj'])
    return data_dict,True

