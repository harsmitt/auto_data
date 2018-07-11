import re
import datetime
import tempfile, subprocess
from .basic_functions import *
from .mapping_data import k_list,stop_words
from collections import OrderedDict
# from BalanceSheet.models import *

index_list =['balance sheet','operations','income','cash flow','notes','balance sheets']
financial_statement =['financial statements and supplementary data','exhibits and financial statement']

def get_page_content(seprator=' ',**kwargs):

    try:
        pdfData = kwargs['file'].read()
        tf = tempfile.NamedTemporaryFile()
        tf.write(pdfData)
        tf.seek(0)
        outputTf = tempfile.NamedTemporaryFile()
        args = ['pdftotext', '-f', str(kwargs['page']), '-l', str(kwargs['page']), '-layout','-enc','UTF-8', '-q', kwargs['path'],
                outputTf.name]
        txt = subprocess.check_output(args)
        data = outputTf.readlines()

        data = [i.decode('utf-8').replace('\xa0',' ') for i in data]#[re.sub(r'[^\x00-\x7A]',  '' , i.decode('utf-8')) for i in data]
        data = [i.lower().strip() for i in data if i != '\n'] if seprator ==' ' else [i.strip() for i in data if i != '\n']
        # data= [re.sub('\s+', '     ', line) for line in data]
        data = [i.replace('\t','  ').replace('\n','') for i in data]
        data = [i for i in data if i != '']
        # data = [line.replace('  @@', ' - ').strip() for line in data]
        # data = [line.replace('@@', ' ').strip() for line in data]

        return data
    except Exception as e:
        return e

def check_content(**kwargs):
    k_words = [get_alpha(i.lower(),remove_space=True,remove_s=True) for i in k_list[kwargs['p_type']]]
    data =  kwargs['data'][:20] if type(kwargs['data'])==list else [kwargs['data']]
    for l_num,line in enumerate(data):
        if get_alpha(line.lower(),remove_s=True) in k_list[kwargs['p_type']] and not 'check_statement' in kwargs :
            return True
        elif get_alpha(line.lower(),remove_space=True,remove_s=True) in k_words and not 'check_statement' in kwargs :
            return True
        else:
            # ' '.join([word for word in i.lower().split() if word not in stop_words ])
            for i in k_list[kwargs['p_type']] :
                if (all((loop in get_alpha(line,remove_space=True,remove_s=True)) or (loop in get_alpha(line,remove_space=True))\
                       for loop in [word for word in i.lower().split() if word not in stop_words ])) or \
                   (all((loop in get_alpha(' '.join(data), remove_space=True, remove_s=True)) or (loop in get_alpha(' '.join(data), remove_space=True)) \
                         for loop in [word for word in i.lower().split() if word not in stop_words])):
                    return True
    return False

def match_re_list(**kwargs):
    try:
        from .all_regex import check_1,check_2
        data = get_page_content(seprator='@@', page=kwargs['page'], path=kwargs['path'], file=kwargs['f_obj'])
        keywords_list = k_list[kwargs['match_re']]
        for keys in keywords_list:
            re_1 = re.compile(check_1, re.I)
            r2 = check_2 %(keys)
            r3 = check_2 %(get_alpha(keys,remove_space=True))
            re_2 = re.compile(r2, re.I)
            re_3 = re.compile(r3, re.I)
            if (re_1.search(extract_s(' '.join(data[:20]))) and re_2.search(extract_s(' '.join(data[:20])))) or\
                re_2.search(extract_s(' '.join(data[:20]))):

                res = check_in_re(data=data,r_1=re_1,r_2 = re_2)
                return data, res

                # x = [i for i in data[:20] if get_digit(i.split()[-1],num=True) and  not check_datetime(i.split()[-1])]
                # if len(x)>5:
                #     return data,True
            elif re_1.search(get_alpha(' '.join(data[:20]),remove_space=True)) and re_3.search(get_alpha(' '.join(data[:20]),remove_space=True)):
                # res = check_in_re(data=data[:20])
                # return data, res
                # x = [i for i in data[:20] if get_digit(i) and check_datetime(i)]
                # if len(x) > 5:
                #     return data, True
                return data,True

        return data,False
    except Exception as e:
        return e

def check_in_re(**kwargs):

    if any(word in (' '.join(kwargs['data']).lower()) for word in ['supplementary financial data','summary of','summarized as','overview of','comparison between','financial summary','financial comparison']):
        return False

    x = [i for i in kwargs['data'] if num_there(i.split()[-1]) and not check_datetime(i.split()[-1],pdf_type = True)]
    if len(x) > 5:
        return True

import copy
def remove_extra_keys(**kwargs):
    data_dict = copy.deepcopy(kwargs['data_dict'])
    for i, j in data_dict.items():
        if type(j)==OrderedDict:
            for inn,inn_d in j.items():
                if not inn_d:
                    del data_dict[i][inn]
        elif not j:
            del data_dict[i]
    return data_dict

def valid_yq_name(date_obj,y_end,pdf_type=None,p_type=None,):
    try:
        val=''
        date_dict = year_date(year_end=y_end) if pdf_type =='year' else qtr_date_pnl()
        for key,val in date_dict.items():
            if pdf_type=='year':
                if int(date_obj) == int(val):
                    val = val
                    return val
            else:
                last_month, next_month = next_last_month(val)
                if date_obj.lower() == val.lower() or date_obj.lower() ==last_month.lower() or date_obj.lower()==next_month.lower():
                    val = val
                    return val

    except Exception as e:
        return e


def y_sorting(year_list):
    try:
        list1= [int(i.split('.')[0]) for i in year_list]
        for loop1 in range(0,len(list1)):
            for i,j in enumerate(list1):
                if len(list1)>1 and len(list1)!=(i+1):
                    if list1[i]<list1[i+1]:
                        temp = list1[i]
                        list1[i]=list1[i+1]
                        list1[i+1]=temp
        return list1
    except Exception as e:
        return e

def q_sorting(q_list):
    try:
        name_list = [i.split('.pdf')[0].replace('_',' ') for i in q_list]
        for loop in range(0,len(name_list)):
            for i,j in enumerate(name_list):
                if len(name_list)>1 and len(name_list)!=(i+1):
                    if datetime.strptime(name_list[i], '%B %Y') < datetime.strptime(name_list[i+1], '%B %Y'):
                        temp= name_list[i]
                        name_list[i] =name_list[i+1]
                        name_list[i+1]=temp
        return name_list
    except Exception as e:
        return e


def get_pdf_quarter(**kwargs):
    try:
        q_list, y_list = [], []
        qtr_list = qtr_date_pnl().values()
        for obj in kwargs['word_list']:
            if check_datetime(obj):
                try:
                    if type(datetime.strptime(obj, '%B')) == datetime:
                        q_list.append(obj.lower())
                except:
                    try:
                        if type(datetime.strptime(obj, '%Y')) == datetime:
                            y_list.append(obj)
                    except:
                        pass
        if (q_list and not y_list) or (y_list and not q_list) or (len(q_list)==1 and len(y_list)==1):#>=1 and len(y_list)!=2 or len(q_list)!=2 and len(y_list)==2 :
            num =kwargs['l_num'] +1
            while num <= kwargs['l_num']+3:
                if num_there(kwargs['data'][num]):
                    for obj in kwargs['data'][num].split():
                        try:
                            if type(datetime.strptime(obj, '%B')) == datetime:
                                q_list.append(obj.lower())
                        except:
                            try:
                                if type(datetime.strptime(obj, '%Y')) == datetime:
                                    y_list.append(obj)
                            except:
                                pass
                    if q_list and y_list :break;
                    else:num+=1
                else:
                    num+=1
        if len(q_list)*2 == len(y_list):
            q_list = q_list*2
        elif len(y_list)*2 == len(q_list):
            y_list = y_list*2


        if len(q_list)==len(y_list):#(len(q_list)>=1 and len(q_list)<=2 and len(y_list)==2) or (len(y_list)>=1 and len(y_list)<=2 and len(q_list)==2) :

            # if len(q_list)==1 and len(y_list)==2:
            #     q_list=q_list*2
            # elif len(y_list)==1 and len(q_list)==2:
            #     y_list=y_list*2
            for i in list(zip(q_list, y_list)):
                q_date =' '.join(i)
                last_month, next_month = next_last_month(q_date)
                # if q_date.lower() in qtr_list or last_month.lower() in qtr_list or next_month.lower() in qtr_list:
                kwargs['date_obj'].append(q_date)

        return kwargs['date_obj']

    except Exception as e:
        return e

def calculations(old,new):
    try:
        year, values = map(list, zip(*old))
        # old_values = list(map(lambda num : get_digit(num),list(filter(lambda x: num_there(x),values))))
        new = list(map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), new))))
        new_values = [a + b for a, b in zip(values, new)]
        return new_values
    except Exception as e:
        return e


def get_date(**kwargs):
    try:
        for d_obj in kwargs['word_list']:
            d_obj = d_obj.replace(',','').split('/')
            for obj in d_obj:
                if check_datetime(obj,pdf_type = 'year'):
                    if kwargs['pdf_type']=='year':
                        year_list =year_date(year_end=kwargs['year_end']).values()
                        if obj not in kwargs['date_obj']:
                            kwargs['date_obj'].append(obj)
                    else:
                        pass


        return kwargs['date_obj']
    except Exception as e:
        return e

def check_date_obj(**kwargs):
    try:
        if kwargs['pdf_type'] == 'year':
            kwargs['date_obj'] = get_date(year_end=kwargs['year_end'], word_list=kwargs['line'].split(),
                                pdf_type=kwargs['pdf_type'],
                                date_obj=kwargs['date_obj'])
            if len(kwargs['date_obj']) < 2:
                kwargs['date_obj'] = []
            else:
                kwargs['date_line'] = kwargs['l_num'] + 1
        else:
            # get_quarter_date(data=kwargs['data'],l_num=kwargs['l_num'],line = kwargs['line'],year_end=kwargs['year_end'],date_obj=kwargs['date_obj'] )
            kwargs['date_obj'] = get_pdf_quarter(year_end=kwargs['year_end'], word_list=kwargs['line'].split(), pdf_type=kwargs['pdf_type'],
                                       date_obj=kwargs['date_obj'],
                                                 data=kwargs['data'],l_num=kwargs['l_num'])
            if len(kwargs['date_obj']) < 1:
                kwargs['date_obj'] = []

            else:
                kwargs['date_obj']= [i for num, i in enumerate(kwargs['date_obj']) if i not in kwargs['date_obj'][num + 1:]]
                kwargs['date_line'] = kwargs['l_num'] + 1
        return  kwargs['date_obj'],kwargs['date_line']
    except Exception as e:
        return e
