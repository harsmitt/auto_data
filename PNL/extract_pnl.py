import re
from DataExtraction.common_files.mapping_data import mapping_dict
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import calculations,remove_extra_keys
from DataExtraction.common_files.ignore_index import remove_ignore_index
from collections import OrderedDict
import copy
import itertools
from DataExtraction.logger_config import logger


pass_list = ['diluted','basic','per share','statement of']
index_list =['consolidated','balance sheets','operations','income','cash flow','comprehensive loss']
spl_char=['\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x94']
exceptional = ['current\n','deferred\n']
except_words =['per share','comprehensive','per common share']



def ExtractPNL(**kwargs):
    try:
        last_notes_no=0
        sub_dict = False
        data_dict = copy.deepcopy(kwargs['data_dict'])
        data = kwargs['data'][kwargs['date_line']:]
        for l_num, line in enumerate(data):
            line = line.replace('$', '').strip()
            if l_num>15 and len(data_dict)<2 and data_dict:
                d_keys =list(data_dict.keys())[-1]
                if not data_dict[d_keys]:
                    break;
            if data_dict and any(word in line.lower() for word in except_words) and not any(word in line.lower() for word in ['except per share']):
                break;

            elif not kwargs['unit'] and line and any(word in line.lower() for word in ['millions', 'thousands']):
                x = [w1 for word in line.lower().split() for w1 in ['millions', 'thousands'] if w1 in word]
                kwargs['unit'] = x[0] if x else ''

            elif any((re.split('  +',ex.lower())[0]) ==  line.lower() for ex in exceptional):
                values = re.split('  +', line)
                if data_dict[list(data_dict.keys())[-1]] == {}:
                    new = list(
                        map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), values[1:]))))

                    data_dict[list(data_dict.keys())[-1]] = get_modigy_values(date_obj =kwargs['date_obj'],val=new)

                else:
                    old_values = data_dict[list(data_dict.keys())[-1]]
                    cal_values = calculations(old_values, values[1:])
                    data_dict[list(data_dict.keys())[-1]] = get_modigy_values(date_obj =kwargs['date_obj'],val=cal_values)#list(zip(kwargs['date_obj'][:-1], cal_values[:-1]))

            elif data_dict and any(val in line.lower() for val in pass_list):
                pass

            elif len(re.split('  +',line)) >2 and not data_dict and not num_there(line):
                pass

            elif  (len(re.split('  +', line.replace('-','').strip()))) < 2 or\
                           (len(re.split('  +', line.replace('-','').strip())) ==2 and \
                                num_there(line) and not alpha_there(line)):
                if num_there(line) and not alpha_there(line):
                    values = list(filter(lambda name: num_there(name), line.split()))
                    if len(values) < (len(kwargs['date_obj'])+len(kwargs['ignore_index'])):
                        new_line = line
                        for n_line in range(1,(len(kwargs['date_obj'])+len(kwargs['ignore_index']))-len(values)+1):
                            new_line = line + data[l_num+n_line]
                        values = list(filter(lambda name: num_there(name), new_line.split()))
                    if kwargs['ignore_index']:
                        values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                    ignore_index=kwargs['ignore_index'],
                                                                    data=kwargs['data'],date_obj = kwargs['date_obj'])
                    val = list(map(lambda x: str(get_digit(x)), values))
                    dict1 = get_modigy_values(date_obj =kwargs['date_obj'],val=val)#list(zip(kwargs['date_obj'], val))
                    for d1 in data_dict:
                        if data_dict[d1] in [[], {}] :
                            data_dict[d1] = dict1

                elif alpha_there(line) and line.split()[0][0].split('-')[0].istitle() and not check_datetime(line.split()[0]):
                    if data_dict and not data_dict[list(data_dict.keys())[-1]]:
                        pass
                    else:
                        new_key = get_alpha(line,key=True,pnl=True)
                        data_dict[new_key] = OrderedDict()


            elif len(re.split('  +', line)) >= 2 :

                values = re.split('  +', line)
                key_name = get_alpha(values[0],key=True,pnl=True)
                new_key = values[0]
                if not new_key.split()[0].split('-')[0].istitle() and data_dict and not data_dict[list(data_dict.keys())[-1]] :
                    line = list(data_dict.keys())[-1].title() + ' ' + line
                    values = re.split('  +', line)
                    key_name = get_alpha(values[0], key=True, pnl=True)
                    new_key = values[0]
                    del data_dict[list(data_dict.keys())[-1]]

                if kwargs['ignore_index']:
                    values, last_notes_no = remove_ignore_index(values, last_notes_no, ignore_index=kwargs['ignore_index'],
                                                                data=kwargs['data'],date_obj = kwargs['date_obj'])
                new_values = list(filter(lambda num: num_there(num), values[1:]))
                val = list(map(lambda x: str(get_digit(x)), new_values))
                if any('%' in i for i in new_values):
                    return False


                if new_key and (new_key.split()[0].split('-')[0].istitle()or new_key.split()[0][0].split('-')[0].istitle() ) and not check_datetime(new_key.split()[0]):
                    if data_dict and not data_dict[list(data_dict.keys())[-1]] or sub_dict:
                        last_key = list(data_dict.keys())[-1]
                        sub_dict = False if any(word in key_name.lower() for word in ['total','net']) and all(word in key_name.split() for word in last_key.split())\
                                else True
                        if not 'total' in key_name.lower() or sub_dict:
                            data_dict[list(data_dict.keys())[-1]][key_name] = get_modigy_values(date_obj =kwargs['date_obj'],val=val)# list(zip(kwargs['date_obj'], val))
                        else:
                            data_dict[key_name] = get_modigy_values(date_obj =kwargs['date_obj'],val=val)#list(zip(kwargs['date_obj'], val))

                    else:
                        data_dict[key_name] = get_modigy_values(date_obj =kwargs['date_obj'],val=val)#list(zip(kwargs['date_obj'], val))


                elif data_dict:
                    if kwargs['ignore_index']:
                        values, last_notes_no = remove_ignore_index(values, last_notes_no,
                                                                    ignore_index=kwargs['ignore_index'],

                                                                    data=kwargs['data'], date_obj=kwargs['date_obj'])

                    new_values = list(filter(lambda num: num_there(num), values[1:]))

                    val = map(lambda x: str(get_digit(x)), new_values)

                    old_dict = data_dict[list(data_dict.keys())[-1]]
                    if not data_dict[list(data_dict.keys())[-1]]:
                        data_dict[list(data_dict.keys())[-1]] = list(zip(kwargs['date_obj'], val))
                    else:pass

        data_dict= remove_extra_keys(data_dict =data_dict)
        return data_dict,kwargs['unit']


    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in pnl extraction for data:%s " % str(kwargs))
        return data_dict,kwargs['unit']

def get_modigy_values(**kwargs):
    try:
        if len(kwargs['date_obj']) == 3:
            if all(kwargs['date_obj'][i] >= kwargs['date_obj'][i + 1] for i in range(len(kwargs['date_obj']) - 1)):

                modify_val = list(zip(kwargs['date_obj'][:-1], kwargs['val'][:-1]))
            else:
                modify_val= list(zip(kwargs['date_obj'][1:], kwargs['val'][1:]))
        else:
            modify_val = list(zip(kwargs['date_obj'], kwargs['val']))

        return modify_val
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for :%s " % str(kwargs))
        return e