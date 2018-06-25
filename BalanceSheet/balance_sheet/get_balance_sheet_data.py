import re
from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from collections import OrderedDict
import copy
import itertools


def ExtractBalnceSheet(**kwargs):
    key_value = ''
    data_dict = copy.deepcopy(kwargs['data_dict'])
    for l_num, line in enumerate(kwargs['data']):
        if len(re.split('  +', line)) < 2:
            if any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k):
                if (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k)) in data_dict:
                    pass
                else:
                    data_dict[next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(line) in k)] = OrderedDict()
            elif data_dict:
                if len(kwargs['data']) > l_num + 1 and (':' in kwargs['data'][l_num] + ' ' + kwargs['data'][l_num + 1])\
                        and data_dict[list(data_dict.keys())[-1]] in [[],{}]:
                    pass

                elif num_there(line) and not alpha_there(line):
                    values = list(filter(lambda name: num_there(name), line.split()))
                    val = list(map(lambda x: str(get_digit(x)), values))
                    dict1 = list(zip(kwargs['date_obj'], val))
                    for d1 in data_dict:
                        for key in data_dict[d1]:
                            if data_dict[d1][key] in [[], {}] and key not in list(itertools.chain(*mapping_dict.key_mapping_dict.keys())):
                                data_dict[d1][key] = dict1
                                key_value = False
                elif not num_there(line) and alpha_there(line):

                    if key_value == 1 :
                        if len(kwargs['data']) > l_num+1  and len(kwargs['data'][l_num+1])>100:
                            new_key = get_alpha(line)
                            data_dict[list(data_dict.keys())[-1]] = OrderedDict({new_key:OrderedDict()})
                        elif len(kwargs['data']) > l_num+1:
                            old_dict= data_dict[list(data_dict.keys())[-1]]
                            if not old_dict[list(old_dict().keys())[-1]]:
                                new_key = list(old_dict.keys())[-1] +' '+ get_alpha(line)
                                old_dict[new_key] = old_dict.pop(list(old_dict.keys())[-1])
                            else:
                                new_key = get_alpha(line)
                                old_dict[list(old_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})

                    elif key_value==2:
                        if len(kwargs['data']) > l_num+2  and not alpha_there(kwargs['data'][l_num+2]) and  not check_datetime(line.split()[0]):
                            new_key = get_alpha(line)
                            data_dict[list(data_dict.keys())[-1]] = OrderedDict({new_key:OrderedDict()})
                        elif len(kwargs['data']) > l_num+2 and not check_datetime(line.split()[0]):
                            old_dict= data_dict[list(data_dict.keys())[-1]]
                            if not old_dict[list(old_dict().keys())[-1]]:
                                new_key = list(old_dict.keys())[-1] +' '+ get_alpha(line)
                                old_dict[new_key] = old_dict.pop(list(old_dict.keys())[-1])
                            else:
                                new_key = get_alpha(line)
                                old_dict[list(old_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})
                    elif line.split()[0].istitle() and not check_datetime(line.split()[0]) and not alpha_there(kwargs['data'][l_num+2]):
                        new_key = get_alpha(line.split(',')[0])
                        if data_dict[list(data_dict.keys())[-1]] in [[], {}]:
                            data_dict[list(data_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})
                        else:
                            data_dict[list(data_dict.keys())[-1]][new_key] = OrderedDict()





        elif len(re.split('  +', line)) > 2 and data_dict:

            key_value = True

            values = re.split('  +', line)

            pattern = re.compile('[(|),-]')

            key_name = get_alpha(values[0])

            # this loop executes when 'total' exist in key then we add a new ley in data dict

            # mentioned in mapping dict for that `total ` key


            # todo ignore_index concept

            if pattern.split(key_name)[0] in [i for i in
                                              list(itertools.chain(*mapping_dict.key_mapping_dict.keys())) if

                                              'total' in i]:

                new_key = key_name if len(key_name) < 60 else key_name.split(',')[0]

                if kwargs['ignore_index']:

                    ignore_index = list(kwargs['ignore_index'].values())

                    ignore_index.sort()

                    for i in ignore_index: del values[i]

                new_values = list(filter(lambda num: num_there(num), values[1:]))

                val = map(lambda x: str(get_digit(x)), new_values)

                data_dict[list(data_dict.keys())[-1]][new_key] = list(zip(kwargs['date_obj'], val))

                data_dict[

                    next(v for k, v in mapping_dict.key_mapping_dict.items() if
                         pattern.split(key_name)[0] in k)] = OrderedDict()


            # zip these values[1:] with date and add new

            # component in data_dict

            else:

                # todo ignore_index concept

                new_key = key_name.split(',')[0]

                if kwargs['ignore_index']:

                    ignore_index = list(kwargs['ignore_index'].values())

                    ignore_index.sort()

                    for i in ignore_index: del values[i]

                new_values = list(filter(lambda num: num_there(num), values[1:]))

                val = map(lambda x: str(get_digit(x)), new_values)

                data_dict[list(data_dict.keys())[-1]][new_key] = \
\
                    list(zip(kwargs['date_obj'], val))

    return data_dict
