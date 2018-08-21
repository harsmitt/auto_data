import copy
import re
# from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from DataExtraction.logger_config import logger

from DataExtraction.common_files.ignore_index import remove_ignore_index
from collections import OrderedDict
import itertools


pass_list = ['commitments and contingencies']
#

#todo merge both balance sheet extraction
def without_sections(**kwargs):
    try:
        last_notes_no = 0
        mapping_dict = kwargs['mapping_dict']
        data_dict = copy.deepcopy(kwargs['data_dict'])

        for l_num, line in enumerate(kwargs['data']):
            if l_num > 20 and len(data_dict) < 2:
                break;
            elif any(val in line.lower() for val in pass_list):
                pass



            elif (len(re.split('  +', line.replace('-', '').strip())) < 2 and alpha_there(line.replace('-', '').strip())) or (
                        len(re.split('  +', line.replace('-', '').strip())) == 2 and num_there(line) and not alpha_there(
                    line)):

                if any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +', line)[0]) in k):
                    key_name = (
                        next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(re.split('  +', line)[0]) in k))
                    if key_name in data_dict:
                        x = list(data_dict.keys())
                        if data_dict[key_name]:
                            if x[-1] == key_name:  # data_dict[key_name]:
                                pass
                            elif x[-1] != key_name and len(data_dict[key_name]) == 1:
                                del data_dict[key_name]
                                data_dict[key_name] = OrderedDict()
                        else:
                            del data_dict[key_name]
                            data_dict[key_name] = OrderedDict()
                    else:
                        data_dict[next(v for k, v in mapping_dict.key_mapping_dict.items() if
                                       get_alpha(re.split('  +', line)[0]) in k)] = OrderedDict()

                elif num_there(line) and not alpha_there(line):
                    values = list(filter(lambda name: num_there(name), line.split()))
                    if kwargs['ignore_index']:
                        values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                    ignore_index=kwargs['ignore_index'],
                                                                    data=kwargs['data'], date_obj=kwargs['date_obj'])
                    val = list(map(lambda x: str(get_digit(x)), values))
                    dict1 = list(zip(kwargs['date_obj'], val))
                    for d1 in data_dict:
                        for key in data_dict[d1]:
                            if type(data_dict[d1])==OrderedDict and data_dict[d1][key] in [[], {}] and key not in ['non current assets',
                                                                              'non current liabilities']:
                                data_dict[d1][key] = dict1
                            else:
                                data_dict[d1] = dict1

                elif alpha_there(line) and line.split()[0][0].split('-')[0].istitle() and not check_datetime(
                        line.split()[0]):
                    new_key = get_alpha(line, key=True)
                    if data_dict:
                        old_dict = data_dict[list(data_dict.keys())[-1]]
                        if old_dict and type(old_dict)==OrderedDict and old_dict[list(old_dict.keys())[-1]] in [[], {}]:
                            old_dict[new_key] = old_dict.pop(list(old_dict.keys())[-1])
                        else:
                            if data_dict[list(data_dict.keys())[-1]] in [[], {}]:
                                data_dict[list(data_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})
                            elif new_key.isalnum() or new_key.isalpha():
                                for d1 in data_dict:
                                    if type(data_dict[d1])==OrderedDict:
                                        for key in data_dict[d1]:
                                            if data_dict[d1][key] in [[], {}] and key not in list(
                                                    itertools.chain(*mapping_dict.key_mapping_dict.keys())):
                                                data_dict[d1][key] = OrderedDict()
                                            else:
                                                data_dict[list(data_dict.keys())[-1]][new_key] = OrderedDict()
                    else:
                        new_key = get_alpha(line, key=True)
                        data_dict[new_key] = OrderedDict()

            elif len(re.split('  +', line)) > 2:

                values = re.split('  +', line)
                pattern = re.compile('[(|)-]')
                key_name = get_alpha(values[0], key=True)

                # this loop executes when 'total' exist in key then we add a new key in data dict
                # mentioned in mapping dict for that `total ` key
                from DataExtraction.common_files.mapping_data import mapping_dict,balance_sheet_keys
                if 'total' in key_name :
                    if not any(key in list(data_dict.keys()) for key in balance_sheet_keys):
                        x = OrderedDict()
                        for i in data_dict: x[i] = data_dict.pop(i)
                        if any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(key_name.strip('total')) in k):
                            old_key = (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(key_name.strip('total')) in k))
                            new_key = (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(key_name) in k))
                            data_dict[old_key] = x
                            data_dict[new_key] = OrderedDict()
                    else:
                        if any(k for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(key_name) in k):
                            new_key = (next(v for k, v in mapping_dict.key_mapping_dict.items() if get_alpha(key_name,key=True) in k))
                            data_dict[new_key] = OrderedDict()
                        else:
                            pass
                        # data_dict[old_key] = x


                elif data_dict and any(key == list(data_dict.keys())[-1] for key in balance_sheet_keys):
                    if kwargs['ignore_index']:
                        values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                    ignore_index=kwargs['ignore_index'],
                                                                    data=kwargs['data'], date_obj=kwargs['date_obj'])
                    new_values = list(filter(lambda num: num_there(num), values[1:]))
                    val = list(map(lambda x: str(get_digit(x)), new_values))
                    data_dict[list(data_dict.keys())[-1]][get_alpha(key_name,key=True)] = list(zip(kwargs['date_obj'], val))
                else:
                    new_key = values[0]
                    if kwargs['ignore_index']:
                        values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                    ignore_index=kwargs['ignore_index'],
                                                                    data=kwargs['data'], date_obj=kwargs['date_obj'])
                    new_values = list(filter(lambda num: num_there(num), values[1:]))
                    val = map(lambda x: str(get_digit(x)), new_values)

                    if data_dict and not data_dict[list(data_dict.keys())[-1]]:
                        data_dict[list(data_dict.keys())[-1]] = list(zip(kwargs['date_obj'], val))

                    elif (new_key.split()[0].split('-')[0].istitle() or new_key.split()[0][0].split('-')[
                        0].istitle()) and not check_datetime(new_key.split()[0]):
                        data_dict[key_name] = list(zip(kwargs['date_obj'], val))
                    else:
                        pass



        return data_dict
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in extraction of balance sheet without section %s " % str(e))
        pass




