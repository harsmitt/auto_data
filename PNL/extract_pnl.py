import re
from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import calculations
from collections import OrderedDict
import copy
import itertools

pass_list = ['diluted','basic','per share']
index_list =['consolidated','balance sheets','operations','income','cash flow']
spl_char=['\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x94']
exceptional = ['current','deferred']

def ExtractPNL(**kwargs):
    last_notes_no=0
    sub_dict = False
    data_dict = copy.deepcopy(kwargs['data_dict'])

    for l_num, line in enumerate(kwargs['data'][kwargs['date_line']:]):
        print (line)
        print ("********************************++++++++++++++++++++++++++************************")
        print (data_dict)

        if data_dict and any(word in line.lower() for word in ['per share','comprehensive','per common share']):
            break;

        elif any(ex.lower() in line.lower() for ex in exceptional):
            values = re.split('  +', line)
            if data_dict[list(data_dict.keys())[-1]] == {}:
                new = list(
                    map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), values[1:]))))
                data_dict[list(data_dict.keys())[-1]] = list(zip(kwargs['date_obj'], new))
            else:
                old_values = data_dict[list(data_dict.keys())[-1]]
                cal_values = calculations(old_values, values[1:])
                data_dict[list(data_dict.keys())[-1]] = list(zip(kwargs['date_obj'], cal_values))

        elif any(val in line.lower() for val in pass_list):
            pass

        elif  (len(re.split('  +', line.replace('-','').strip())) < 2 and alpha_there(line.replace('-','').strip())) or (len(re.split('  +', line.replace('-','').strip())) ==2 and num_there(line) and not alpha_there(line)):

            if num_there(line) and not alpha_there(line):
                values = list(filter(lambda name: num_there(name), line.split()))
                if kwargs['ignore_index']:
                    values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                ignore_index=kwargs['ignore_index'],
                                                                data=kwargs['data'],date_obj = kwargs['date_obj'])
                val = list(map(lambda x: str(get_digit(x)), values))
                dict1 = list(zip(kwargs['date_obj'], val))
                for d1 in data_dict:
                    if data_dict[d1] in [[], {}] :
                        data_dict[d1] = dict1
                            
            elif alpha_there(line) and line.split()[0][0].split('-')[0].istitle() and not check_datetime(line.split()[0]):
                print ("ye karna hai")
                new_key = get_alpha(line,pnl=True)
                data_dict[new_key] = OrderedDict()


        elif len(re.split('  +', line)) > 2 :

            values = re.split('  +', line)
            pattern = re.compile('[(|)-]')
            key_name = get_alpha(values[0],pnl=True)

            # this loop executes when 'total' exist in key then we add a new key in data dict
            # mentioned in mapping dict for that `total ` key
            # todo ignore_index concept
            #
            #
            # # # todo ignore_index concept
            new_key = values[0]
            if kwargs['ignore_index']:
                values, last_notes_no = remove_ignore_index(values, last_notes_no, ignore_index=kwargs['ignore_index'],
                                                            data=kwargs['data'],date_obj = kwargs['date_obj'])
            new_values = list(filter(lambda num: num_there(num), values[1:]))
            val = map(lambda x: str(get_digit(x)), new_values)

            if (new_key.split()[0].split('-')[0].istitle()or new_key.split()[0][0].split('-')[0].istitle() ) and not check_datetime(new_key.split()[0]):
                # import pdb;pdb.set_trace()
                if data_dict and not data_dict[list(data_dict.keys())[-1]] or sub_dict:
                    last_key = list(data_dict.keys())[-1]
                    sub_dict = False if last_key in key_name else True
                    if not 'total' in key_name.lower():
                        data_dict[list(data_dict.keys())[-1]][key_name] = list(zip(kwargs['date_obj'], val))
                    else:
                        data_dict[key_name] = list(zip(kwargs['date_obj'], val))

                else:
                    data_dict[key_name] = list(zip(kwargs['date_obj'], val))

            else:
                print (line)


    return data_dict


def remove_ignore_index(values,last_notes_no,**kwargs):
    ignore_index = list(kwargs['ignore_index'].values())
    ignore_index.sort()
    if 'notes' in kwargs['ignore_index']:
        # import pdb;pdb.set_trace()
        current_notes = values[kwargs['ignore_index']['notes']]
        if last_notes_no and not (len(last_notes_no) == len(current_notes)):
            ignore_index.remove(kwargs['ignore_index']['notes'])
        elif len(values) == len(kwargs['date_obj']) + len(kwargs['ignore_index']) + 1:
            last_notes_no = current_notes if current_notes else last_notes_no
    for i in ignore_index:
        del values[i]
    return values,last_notes_no
