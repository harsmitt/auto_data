from DataExtraction.common_files.utils import *
from DataExtraction.common_files.basic_functions import *
import copy

def make_str(**kwargs):
    val_list = []
    for val in kwargs['val']:
        new_str = ''
        str1 = copy.deepcopy(val)
        for i in range(int((len(val)-1)/3)):
            new_str = ',' + str(str1[-3:]) + new_str
            str1 = str1[:-3]
        new_str = str1+new_str
        val_list.append(new_str)
    return val_list
#
# def keys_find_breakup(**kwargs):
#     key_list =[]
#     pdf_page_keys = list(kwargs['data_dict'].keys())
#     for key in pdf_page_keys:
#         if not type(kwargs['data_dict'][key]) == OrderedDict:
#             key_list.append(key)
#     return key_list


    # else:
    #     for key in pdf_page_keys:
    #         key_list.append(key)
    #     return key_list

def match_key(**kwargs):
    try:
        for key in kwargs['pdf_page_keys']:
            key = key.replace('net','').replace('total','')
            r1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-:]*$' % (key)
            r2 = '%s[ ,A-Za-z0-9.-:]*$' % (key)
            re_obj = re.compile(r1, re.I)
            re_obj2 = re.compile(r2, re.I)
            if re_obj.match(get_alpha(kwargs['line'],key=True)) or re_obj2.match(get_alpha(kwargs['line'],key=True)):
                return True
            else:
                r1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-:]*$' % (key.replace('net','').replace('total','').split(',')[0])
                r2 = '%s[ ,A-Za-z0-9.-:]*$' % (key.replace('net','').replace('total','').split(',')[0])
                re_obj = re.compile(r1, re.I)
                re_obj2 = re.compile(r2, re.I)
                if re_obj.match(get_alpha(kwargs['line'],key=True)) or re_obj2.match(get_alpha(kwargs['line'],key=True)):
                    return True
        return False
    except:
        import pdb;pdb.set_trace()
        print (key)

def get_values(**kwargs):
    keys = list(kwargs['data_dict'].keys())
    if kwargs['exist_key'] in kwargs['data_dict']:
        date_obj, values = map(list, zip(*kwargs['data_dict'][kwargs['exist_key']]))
        return date_obj,values
    else:
        for i in keys:
            if type(kwargs['data_dict'][i])==OrderedDict and kwargs['exist_key'] in kwargs['data_dict'][i]:
                date_obj, values =map(list,zip(*kwargs['data_dict'][i][kwargs['exist_key']]))
                return date_obj,values
    # else:
    #     date_obj, values = map(list, zip(*kwargs['data_dict'][kwargs['exist_key']]))
    #     return date_obj, values

import copy

def extract_notes(**kwargs):
    start = kwargs['key']['f_num']
    end = kwargs['key']['l_num']
    notes_sec_start = False
    pdf_page_keys = copy.deepcopy(kwargs['pdf_page_keys'])
    if pdf_page_keys:
        for notes in range(int(start), int(end)):
            if notes ==83: import pdb;pdb.set_trace()
            date_obj = []
            data = get_page_content(seprator='@@', page=notes, path=kwargs['path'], file=kwargs['file'])
            notes_sec_start = True
            if notes_sec_start:
                try:
                    for l_num, line in enumerate(data):
                        line = line.lower().replace('net','').replace('total','')
                        if match_key(pdf_page_keys=pdf_page_keys,line=line.lower()):
                            exist_key = [key for key in pdf_page_keys if key.replace('net','').replace('total','') in get_alpha(line,key=True)]
                            if exist_key:
                                year,values = get_values(exist_key = exist_key[0],data_dict = kwargs['data_dict'])#map(list,zip(**kwargs['data_dict'][exist_key[0]]))
                                new_values = make_str(val = values)
                                start = l_num-2 if l_num > 2 else l_num
                                end = l_num+10 if len(data)> l_num+11 else len(data)-l_num
                                if not date_obj:
                                    for num, line in enumerate(data[start:end]):

                                        if kwargs['pdf_type'] == 'year':
                                            date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                                                 year_end=kwargs['year_end'], data=data,
                                                                                     date_obj=date_obj,
                                                                                     date_line=0,
                                                                                     l_num=num)
                                            if all(y1 in date_obj for y1 in year):
                                                date_obj=year
                                                break;
                                            else:date_obj=[]
                                        else:
                                            next_line = data[start:end][num + 1] if len(data[start:end]) > num + 1 else ''
                                            date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                                                     year_end=kwargs['year_end'], data=data[start:end],
                                                                                     date_obj=date_obj,next_line=next_line,
                                                                                     date_line=0, l_num=num)
                                            if date_obj ==year: break;
                                            else:date_obj=[]
                                if date_obj==year:
                                    if (all(val in line.lower() for val in new_values) for line in data[l_num+date_line-1:l_num+date_line+10]):
                                        s_line = l_num
                                        start_l = s_line+date_line if date_line > s_line else s_line
                                        new_dict = get_data_dict(date_obj=date_obj,data = data[start_l:start_l+15],key= exist_key,values = new_values)
                                        if new_dict:
                                            for keys in list(kwargs['data_dict'].keys()):
                                                if type(kwargs['data_dict'][keys])==OrderedDict and exist_key[0] in kwargs['data_dict'][keys]:
                                                        del kwargs['data_dict'][keys][exist_key[0]]
                                                        kwargs['data_dict'][keys][exist_key[0]] = new_dict
                                                        pdf_page_keys.pop(pdf_page_keys.index(exist_key[0]))
                                                        break;
                                                elif exist_key[0] in list(kwargs['data_dict'].keys()):
                                                    del kwargs['data_dict'][exist_key[0]]
                                                    kwargs['data_dict'][exist_key[0]] = new_dict
                                                    pdf_page_keys.pop(pdf_page_keys.index(exist_key[0]))
                                                    break;
                except Exception as e:
                    import traceback
                    print (traceback.format_exc())
                    pass

        return kwargs['data_dict'],pdf_page_keys


    else:
        print ("no key for breakup")

def get_data_dict(**kwargs):
    sub_dict=False
    new_key_dict=OrderedDict()
    for line in kwargs['data']:
        word = list(line.split()[0].split('-')[0])
        if len(re.split('  +',line.replace('$',''))) == len(kwargs['date_obj'])+1:
            if all(val in line for val in kwargs['values']):
                for i in new_key_dict:
                    if not new_key_dict[i]:
                        del new_key_dict[i]
                return new_key_dict
            elif word[0].istitle() and not num_there(line) and not check_datetime(line.split()[0]):
                if alpha_there(line) and not num_there(line):
                    new_key_dict[line] = OrderedDict()

                elif new_key_dict and num_there(line) and not alpha_there(line) and not check_datetime(line.split()[0]):
                    values = list(filter(lambda name: num_there(name), line.split()))
                    new = list(
                        map(lambda num: get_digit(num),list(filter(lambda x: num_there(x), values))))

                    dict1 = list(zip(kwargs['date_obj'], new))
                    for d1 in new_key_dict:
                        for key in new_key_dict[d1]:
                            if new_key_dict[d1][key] in [[], {}]:
                                new_key_dict[d1][key] = dict1
                elif new_key_dict and alpha_there(line) and not check_datetime(line.split()[0]):
                    new_key = get_alpha(line,pnl=True)
                    # old_dict = new_key_dict[list(new_key_dict.keys())[-1]]
                    if new_key_dict[list(new_key_dict.keys())[-1]] in [[], {}]:
                            new_key_dict[list(new_key_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})
                            sub_dict=True
            elif line.split()[0].split('-')[0].istitle() and len(re.split('  +', line)) > 1 and not check_datetime(line.split()[0]):
                values = re.split('  +', line)
                new_key = get_alpha(values[0])
                val = values[1].split() if len(values) == 2  else values[1:]
                # new_key = new_key.strip().lower()
                # if new_key not in keys:
                if 'total' not in new_key:
                    new = list(
                        map(lambda num: str(get_digit(num)),list((filter(lambda x: num_there(x), val)))))
                    if new_key_dict and new_key_dict[list(new_key_dict.keys())[-1]] in [[], {}] :
                            new_key_dict[list(new_key_dict.keys())[-1]] = OrderedDict({new_key: list(zip(kwargs['date_obj'], new))})
                            sub_dict=True
                    elif sub_dict:
                        new_key_dict[list(new_key_dict.keys())[-1]][new_key] = list(zip(kwargs['date_obj'], new))

                    else:
                        new_key_dict[new_key] = list(zip(kwargs['date_obj'], new))
                elif 'total' in new_key and sub_dict:
                    if new_key_dict:
                        last_key = list(new_key_dict.keys())[-1]
                        sub_dict = False if new_key.split('total')[-1] in last_key else True

    new_key_dict = OrderedDict()

    if new_key_dict:
        for key,val in new_key_dict.items():
            if not new_key_dict[key]:
                del new_key_dict[key]
    return new_key_dict

