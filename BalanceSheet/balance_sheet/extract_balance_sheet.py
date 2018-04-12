import re
from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from collections import OrderedDict
import copy
import itertools


def ExtractBalnceSheet(**kwargs):
    last_notes_no=0
    data_dict = copy.deepcopy(kwargs['data_dict'])

    for l_num, line in enumerate(kwargs['data'][kwargs['date_line']:]):
        print (line)
        print ("********************************++++++++++++++++++++++++++************************")
        print (data_dict)
        if data_dict and data_dict[list(data_dict.keys())[-1]] == [] :
            data_dict[list(data_dict.keys())[-1]] =OrderedDict()
        l_check = line if line and line.strip()[-1].isalpha() else line and line.replace('-','').strip()
        if (len(re.split('  +',l_check)) < 2 and alpha_there(l_check)) or \
                (len(re.split('  +', l_check)) ==2 and num_there(line) and not alpha_there(line)):
            pass_list = ['LIABILITIES AND', ]

            # Add main key in data dict
            if any(i.lower() in line.lower() for i in pass_list) and not num_there(line):
                pass;

            elif any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k):
                if (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k)) in data_dict:
                    pass
                else:
                    data_dict[next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k)] = OrderedDict()

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
                    print ("ye karna hai")
                    new_key = get_alpha(line)
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

        elif len(re.split('  +', line)) > 2 and data_dict:

            values = re.split('  +', line)
            pattern = re.compile('[(|)-]')
            key_name = get_alpha(values[0])
            if key_name in ['assets','liabilities']:
                line = kwargs['data'][l_num-1]+' '+line
                values = re.split('  +', line)

            # this loop executes when 'total' exist in key then we add a new key in data dict
            # mentioned in mapping dict for that `total ` key
            # todo ignore_index concept

            elif pattern.split(key_name)[0] in [i for i in
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
            else:
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

                    data_dict[list(data_dict.keys())[-1]][get_alpha(new_key)] = \
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


    return data_dict


def remove_ignore_index(values,last_notes_no,**kwargs):
    ignore_index = list(kwargs['ignore_index'].values())
    ignore_index.sort()
    if 'notes' in kwargs['ignore_index']:
        current_notes = values[kwargs['ignore_index']['notes']]
        if last_notes_no and not (len(last_notes_no) == len(current_notes)):
            ignore_index.remove(kwargs['ignore_index']['notes'])

        elif len(values) == len(kwargs['date_obj'])+len(kwargs['ignore_index'])+1:
            last_notes_no = current_notes if current_notes else last_notes_no

    for i in ignore_index:
        del values[i]
    return values,last_notes_no
