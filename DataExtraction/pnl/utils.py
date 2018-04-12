import re
import datetime
import tempfile, subprocess
from DataExtraction.common_functions import *
from collections import OrderedDict

pass_list = ['total','gross margin','diluted','basic','per share']
index_list =['consolidated','balance sheets','operations','income','cash flow']
spl_char=['\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x94']
exceptional = ['current','deferred']

# total_comp = list(mapping_dict.keys()) + list(mapping_dict.values())
def get_date_obj(date_obj, str1, date_val, qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    get_month = [i for i in str1.split() if not num_there(i)]

    try:
        if len(get_month) in [2, 0]:
            if not date_obj and not date_val == True and not get_year:
                date_obj = get_month
            else:
                month_year = list(zip(date_obj, get_year) if date_obj else zip(get_month, get_year))
                date_obj = []
                for r1 in month_year:
                    obj = r1[0] + ' ' + r1[1]
                    d_obj = datetime.strptime(obj, '%B %Y')
                    if type(d_obj) == datetime:
                        date_obj.append(obj)
                qtr_list = qtr_date().values()
                for i in date_obj:
                    last_month, next_month = next_last_month(i)
                    if i in qtr_list or last_month in qtr_list or next_month in qtr_list:
                        date_val = True
                        qtr_exists = True
                        break;
                    else:
                        date_val, qtr_exists = False, False
    except:
        date_val, qtr_exists = False, False

    return date_obj, qtr_exists, date_val


def get_year(date_obj, str1, date_val, qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    if not len(get_year) == 3 and not date_obj and date_val == False:
        for i in str1.split():
            try:
                if not num_there(i):
                    d_obj = datetime.strptime(i, '%B')
                    if d_obj and type(d_obj) == datetime:
                        date_obj.append(i)
                else:
                    break;
            except:
                return date_obj, False, date_val
    else:
        if len(get_year) == 3:
            date_obj = get_year
            date_val = True
            qtr_exists = True
    return date_obj, qtr_exists, date_val

def get_page_content(**kwargs):
    # print (kwargs)
    pdfData = kwargs['file'].read()
    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)
    outputTf = tempfile.NamedTemporaryFile()
    args = ['pdftotext', '-f', str(kwargs['page']), '-l', str(kwargs['page']), '-layout', '-q', kwargs['path'],
            outputTf.name]
    txt = subprocess.check_output(args, universal_newlines=True)
    data = outputTf.readlines()
    return data


def table_content(**kwargs):
    # print (kwargs)
    r1 = re.compile('[ (A-Za-z0-9. - )]Table of Contents*[ (A-Za-z0-9. - )$]', re.IGNORECASE)
    if [i for i in kwargs['data'] if r1.search(i.decode('utf-8'))]:
        for num, str1 in enumerate(kwargs['data']):
            if 'Financial Statements and Supplementary Data' in str1.decode('utf-8'):

                page_num = str1.decode('utf-8').split()[-1]
                next_num = kwargs['data'][num + 1].decode('utf-8').split()[-1]
                if (int(next_num) - int(page_num)) > 5:
                    for i in range(10):
                        data = get_page_content(page=page_num,path=kwargs['path'],file=kwargs['file'])
                        if any(('Financial Statements and Supplementary Data').lower() in i.decode('utf-8').lower() for i in data):
                            statements_page = {' '.join(i.decode('utf-8').split()[0:6]) : i.decode('utf-8').split()[-1]
                                                                  for i in data if any(index in i.decode('utf-8').lower() for index in index_list)
                                                                  and i.decode('utf-8').split()[-1].isdigit()==True}
                            # print (kwargs['page_detail'])
                            kwargs['page_detail']['page_list'].update(statements_page)
                            break;
                        else:
                            page_num= int(page_num)+ 1

            elif "Management's Discussion and Analysis of" in str1.decode('utf-8'):
                page_num = str1.decode('utf-8').split()[-1]
                next_num = kwargs['data'][num + 1].decode('utf-8').split()[-1]
                key =get_aplha( str1.decode('utf-8').split('.')[-1].strip())
                if (int(next_num) - int(page_num)) > 1:
                    if 'page_list' in kwargs['page_detail']:
                        kwargs['page_detail']['page_list']['start-end'] ={key: page_num+'-'+ next_num}
                    else:
                        kwargs['page_detail']['page_list'] ={'start-end':{key:page_num+'-'+ next_num}}


            elif any(i in str1.decode('utf-8').lower() for i in index_list) and str1.decode('utf-8').split()[-1].isdigit()==True:
                page_num = str1.decode('utf-8').split()[-1]
                if 'page_list' in kwargs['page_detail']:
                    kwargs['page_detail']['page_list'][' '.join(str1.decode('utf-8').split()[0:6])] =page_num
                else:
                    kwargs['page_detail']['page_list'] ={' '.join(str1.decode('utf-8').split()[0:6]):page_num}


            elif 'Financial Statement' in str1.decode('utf-8') and not kwargs['page_detail']:
                page_num = str1.decode('utf-8').split()[-1]
                for i in range(10):
                    data = get_page_content(page=page_num, path=kwargs['path'], file=kwargs['file'])
                    if any('Financial Statement' in i.decode('utf-8') for i in data):
                        kwargs['page_detail']['page_list'] = {' '.join(i.decode('utf-8').split()[0:6]) : i.decode('utf-8').split()[-1]
                                                              for i in data if 'consolidated' in i.decode('utf-8').lower()
                                                              if i.decode('utf-8').split()[-1].isdigit()==True}
                        # print (kwargs['page_detail'])
                        break;
                    else:
                        page_num = int(page_num) + 1

    return kwargs['page_detail']



def get_operations_data(**kwargs):
    qtr_exists = ''
    date_val = False
    date_obj = []
    data_dict = OrderedDict()
    for loop1 in range(10):
        data = get_page_content(page=kwargs['num'], path=kwargs['path'], file=kwargs['file'])
        r1 = re.compile('[ (A-Za-z0-9. - )]STATEMENTS OF *[ (A-Za-z0-9. - )$]', re.IGNORECASE)
        r2 = re.compile('[ (A-Za-z0-9. - )]income|operation*[ (A-Za-z0-9. - )$]', re.IGNORECASE)
        if ([i for i in data if r1.search(i.decode('utf-8')) and r2.search(i.decode('utf-8'))]) and not data_dict:
            for i in data:
                i = i.decode('utf8')
                if i and num_there(i) and not date_val:
                    date_obj, qtr_exists, date_val = get_year(date_obj, i, date_val, qtr_exists)
                    if qtr_exists == False and len(date_obj) > 1:
                        qtr_exists = False
                        break;
                elif date_val == True:
                    word = i.strip().replace(':', '')
                    if 'per share' in word:
                        break;
                    elif any(ex.lower() in word.lower() for ex in exceptional):
                        values = re.split('  +', word)
                        if data_dict[list(data_dict.keys())[-1]]=={}:
                            new = list(
                                map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), values[1:]))))
                            data_dict[list(data_dict.keys())[-1]]=list(zip(date_obj,new))
                        else:
                            old_values = data_dict[list(data_dict.keys())[-1]]
                            cal_values = calculations(old_values,values[1:])
                            data_dict[list(data_dict.keys())[-1]] = list(zip(date_obj,cal_values))

                    elif any(val in word.lower() for val in pass_list):
                        pass
                    elif word and word.split()[0].istitle() and len(word) < 100 and any(
                            check_datetime(str1) for str1 in word.split()) == False:

                        if word.lower() in data_dict:
                                pass

                        elif alpha_there(word) and not num_there(word):
                            # new_key = get_aplha(word)
                            data_dict[word.strip().lower()] = {}

                        elif data_dict and num_there(word) and not alpha_there(word):
                            values = list(filter(lambda name: num_there(name), word.split()))
                            # new = [int(i.replace(',', '').replace('(', '-').replace(')', '').replace('$','')) for i in values]
                            new =list(map(lambda num : get_digit(num),list(filter(lambda x: num_there(x),values))))

                            dict1 = list(zip(date_obj,new))
                            for d1 in data_dict:
                                for key in data_dict[d1]:
                                    if data_dict[d1][key] in [[], {}]:
                                        data_dict[d1][key] = dict1

                    elif len(word) > 100:
                        values = re.split('  +', word)
                        new_key = values[0] if len(values[0]) < 60 else values[0].split(',')[0]
                        new_key =  new_key.strip().lower()
                        val = values[1].split() if len(values) == 2  else values[1:]#get_aplha(new_key)
                        # new_values = list(map(lambda x: x.replace(x, '-') if x in spl_char else x, values[1:]))
                        new = list(map(lambda num : get_digit(num),list(filter(lambda x: num_there(x),val))))
                        data_dict[new_key] = list(zip(date_obj,new))

                    elif len(word) > 100 and ('                       ') not in word:
                        word = word.split(',')[0]
                        new_key = [word.replace(i, '-') for i in spl_char if i in word]
                        new_key = "".join(new_key[0].split()) if new_key else word

                        data_dict[list(data_dict.keys())[-1]] = {new_key: {}}

        elif data_dict:
            break;
        else:
            kwargs['num']=int(kwargs['num'])+1

    return data_dict,kwargs['num']


def calculations(old,new):
    year, values = map(list, zip(*old))
    # old_values = list(map(lambda num : get_digit(num),list(filter(lambda x: num_there(x),values))))
    new = list(map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), new))))
    new_values = [a + b for a, b in zip(values, new)]
    return new_values


def get_notes_data(**kwargs):
    import copy
    old_data_dict = copy.deepcopy(kwargs['page_data'])
    notes_sec_start=False
    notes_key =['net sales', 'cost of sales','selling, general and administrative expenses','interest expense', 'other (income) expense, net']
    sec_name = list(kwargs['notes_sec'].keys())[0]

    start= list(kwargs['notes_sec'].values())[0].split('-')[0]
    end = list(kwargs['notes_sec'].values())[0].split('-')[-1]
    total_notes = int(end) - int(start)
    for notes in range(int(start)-1,int(end)+5):
        data = get_page_content(page=notes, path=kwargs['path'], file=kwargs['file'])
        if any(sec_name in get_aplha(i.decode('utf-8')) for i in data ) and not notes_sec_start:
            notes_sec_start = True
            keys = list(kwargs['page_data'].keys())
            for key in keys:
                r1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$' %(key)
                r2 = '%s[ ,A-Za-z0-9.-]*$' %(key)
                re_obj = re.compile(r1, re.I)
                re_obj2 = re.compile(r2, re.I)
                for line in data:
                    if re_obj.match(line.decode('utf-8')) or re_obj2.match(line.decode('utf-8')):
                        print ("match kr gya")

        elif notes_sec_start:
            qtr_exists = ''
            date_val = False
            date_obj = []
            new_key_dict = OrderedDict()

            keys = list(kwargs['page_data'].keys())
            for key in keys:
                if key in notes_key:
                    r1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$' % (key)
                    r2 = '%s[ ,A-Za-z0-9.-]*$' % (key)
                    re_obj = re.compile(r1, re.I)
                    re_obj2 = re.compile(r2, re.I)
                    if any(re_obj2.match(line.decode('utf-8')) for line_num,line in enumerate(data) ) :
                        key_line_num =[line_num for line_num,line in enumerate(data) if re_obj2.match(line.decode('utf-8'))]

                        for num,line in enumerate(data[key_line_num[0]:]):
                            line = line.decode('utf8').strip()
                            if line and num_there(line) and not date_val:
                                date_obj, qtr_exists, date_val = get_year(date_obj, line, date_val, qtr_exists)
                                if qtr_exists == False and len(date_obj) > 1:
                                    qtr_exists = False
                                    break;
                            elif date_val == True:
                                if line.replace('-',' ').split()[0].istitle() and not num_there(line):
                                    if line.lower() in kwargs['page_data']:
                                        pass

                                    elif alpha_there(line) and not num_there(line):
                                        # new_key = get_aplha(word)
                                        new_key_dict[line.strip().lower()] = {}

                                    elif new_key_dict and num_there(line) and not alpha_there(line):
                                        values = list(filter(lambda name: num_there(name), line.split()))
                                        new = list(
                                            map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), values))))

                                        dict1 = list(zip(date_obj, new))
                                        for d1 in new_key_dict:
                                            for key in new_key_dict[d1]:
                                                if new_key_dict[d1][key] in [[], {}]:
                                                    new_key_dict[d1][key] = dict1

                                elif line.replace('-',' ').split()[0].istitle() and len(re.split('   +',line))>1:
                                    values = re.split('  +', line)
                                    new_key = values[0] if len(values[0]) < 60 else values[0].split(',')[0]
                                    val = values[1].split() if len(values)==2  else values[1:]
                                    new_key = new_key.strip().lower()
                                    if new_key not in keys:
                                        if 'total' not in new_key:
                                            new = list(
                                                map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), val))))
                                            if kwargs['page_data'][key]!= list(zip(date_obj, new)):
                                                new_key_dict[new_key] = list(zip(date_obj, new))
                                            else:
                                                old_data_dict.update(new_key_dict)
                                                break;

                                        if new_key.split()[0].lower()=='total' :
                                            new = list(
                                                map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), val))))
                                            new_key_dict[new_key] = list(zip(date_obj, new))
                                            old_data_dict.update(new_key_dict)
                                            break;
                                    elif (new_key == key) :
                                        old_data_dict.update(new_key_dict)
                                        break;

                    # print (kwargs['page_data'][key])




        else:
            print ("different page")
    return old_data_dict
