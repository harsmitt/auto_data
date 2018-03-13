import re
import datetime
import tempfile, subprocess
from .basic_functions import *
from collections import OrderedDict
# from BalanceSheet.models import *

index_list =['balance sheet','operations','income','cash flow','notes','balance sheets']
financial_statement =['financial statements and supplementary data','exhibits and financial statement']

def get_page_content(seprator=' ',**kwargs):
    pdfData = kwargs['file'].read()
    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)
    outputTf = tempfile.NamedTemporaryFile()
    args = ['pdftotext', '-f', str(kwargs['page']), '-l', str(kwargs['page']), '-layout', '-q', kwargs['path'],
            outputTf.name]
    txt = subprocess.check_output(args)
    data = outputTf.readlines()
    data = [re.sub(r'[^\x00-\x7F]+', seprator, i.decode('utf-8')) for i in data]
    data = [i.lower().strip() for i in data if i != '\n'] if seprator ==' ' else [i.strip() for i in data if i != '\n']
    data = [line.replace(' @@', ' - ').strip() for line in data]
    data = [line.replace('@@', ' ').strip() for line in data]

    return data

def match_regex(**kwargs):
    data = get_page_content(seprator='@@', page=kwargs['page'], path=kwargs['path'], file=kwargs['f_obj'])
    print (data)
    if len(kwargs['match_re'])==1:
        r1 = re.compile(kwargs['match_re'][0],re.IGNORECASE)
        if ([i for i in data if r1.search(i.lower())]):
            return data,True
        else:
            return data,False
    elif len(kwargs['match_re'])==2:
        r1 = re.compile(kwargs['match_re'][0], re.IGNORECASE)
        r2 = re.compile(kwargs['match_re'][1], re.IGNORECASE)
        if ([i for i in data if r1.search(i.lower()) and r2.search(i.lower()) ]):
            return data, True
        else:
            return data, False

# def get_date_obj(date_obj, str1, date_val,qtr_exists):
#     get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
#     get_month = [i for i in str1.split() if not num_there(i) and i.lower().strip() not in ['current assets','assets']]
#
#     if len(get_month) ==3:
#         try:
#             if  list(filter(lambda x:  datetime.strptime(x, '%B') ,date_obj) ):
#                 get_month=get_month[1:]
#         except:
#             pass
#
#     try:
#         if len(get_month) in[2,0] :
#             if not date_obj and not date_val==True and not get_year:
#                 date_obj=get_month
#             else:
#                 month_year = list(zip(date_obj, get_year) if date_obj else zip(get_month,get_year))
#                 date_obj=[]
#                 for r1 in month_year:
#                     obj = r1[0]+' '+r1[1]
#                     d_obj = datetime.strptime(obj, '%B %Y')
#                     if type(d_obj) == datetime:
#                         date_obj.append(obj)
#                 qtr_list = qtr_date().values()
#                 for i in date_obj:
#                     last_month,next_month = next_last_month(i)
#                     if i in qtr_list or last_month in qtr_list or next_month in qtr_list:
#                         date_val=True
#                         qtr_exists=True
#                         break;
#                     else:
#                         date_val,qtr_exists = False,False
#     except:
#         date_val, qtr_exists = False, False
#
#     return date_obj,qtr_exists,date_val

def get_quarter_name(date_obj,y_end):
    quarter_val=''
    qtr_dict = qtr_date(year_end=y_end)
    for key,val in qtr_dict.items():
        last_month ,next_month = next_last_month(val)
        if date_obj == val or date_obj ==last_month or date_obj==next_month:
            quarter_val = key
            break;
    return quarter_val


def get_year_name(date_obj,y_end):
    year_val=''
    year_dict = year_date(year_end=y_end)
    for key,val in year_dict.items():
        if int(date_obj) == int(val):
            year_val = key
            break;
    return year_val


def y_sorting(year_list):
    list1= [int(i.split('.')[0]) for i in year_list]
    for loop1 in range(0,len(list1)):
        for i,j in enumerate(list1):
            if len(list1)>1 and len(list1)!=(i+1):
                if list1[i]<list1[i+1]:
                    temp = list1[i]
                    list1[i]=list1[i+1]
                    list1[i+1]=temp
    return list1

def q_sorting(q_list):
    name_list = [i.split('.pdf')[0].replace('_',' ') for i in q_list]
    for loop in range(0,len(name_list)):
        for i,j in enumerate(name_list):
            if len(name_list)>1 and len(name_list)!=(i+1):
                if datetime.strptime(name_list[i], '%B %Y') < datetime.strptime(name_list[i+1], '%B %Y'):
                    temp= name_list[i]
                    name_list[i] =name_list[i+1]
                    name_list[i+1]=temp
    return name_list



def get_pdf_quarter(**kwargs):
    q_list, y_list = [], []
    qtr_list = qtr_date(year_end=kwargs['year_end']).values()
    for obj in kwargs['word_list']:
        if check_datetime(obj):
            print (obj)
            try:
                if type(datetime.strptime(obj, '%B')) == datetime:
                    if obj not in q_list :q_list.append(obj.lower())
            except:
                try:
                    if type(datetime.strptime(obj, '%Y')) == datetime:
                        if obj not in q_list:y_list.append(obj)
                except:
                    pass

    if len(q_list)>=1 and len(y_list)!=2 or len(q_list)!=2 and len(y_list)==2 :
        # import pdb;pdb.set_trace()
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
                break;
            else:
                num+=1

    if (len(q_list)>=1 and len(q_list)<=2 and len(y_list)==2) or (len(y_list)>=1 and len(y_list)<=2 and len(q_list)==2) :

        if len(q_list)==1 and len(y_list)==2:
            q_list=q_list*2
        elif len(y_list)==1 and len(q_list)==2:
            y_list=y_list*2
        for i in list(zip(q_list, y_list)):
            q_date =' '.join(i)
            last_month, next_month = next_last_month(q_date)
            if q_date.lower() in qtr_list or last_month.lower() in qtr_list or next_month.lower() in qtr_list:
                kwargs['date_obj'].append(q_date)

    return kwargs['date_obj']

def calculations(old,new):
    year, values = map(list, zip(*old))
    # old_values = list(map(lambda num : get_digit(num),list(filter(lambda x: num_there(x),values))))
    new = list(map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), new))))
    new_values = [a + b for a, b in zip(values, new)]
    return new_values


def get_date(**kwargs):
    for obj in kwargs['word_list']:
        obj = obj.replace(',','')
        if check_datetime(obj):
            if kwargs['pdf_type']=='year':
                year_list =year_date(year_end=kwargs['year_end']).values()
                if obj in year_list and obj not in kwargs['date_obj']:
                    kwargs['date_obj'].append(obj)
            else:
                print ('quarter')

    return kwargs['date_obj']

def check_date_obj(**kwargs):
    if kwargs['pdf_type'] == 'year':
        kwargs['date_obj'] = get_date(year_end=kwargs['year_end'], word_list=kwargs['line'].split(),
                            pdf_type=kwargs['pdf_type'],
                            date_obj=kwargs['date_obj'])
        if len(kwargs['date_obj']) < 2:
            kwargs['date_obj'] = []
        else:
            # import pdb;pdb.set_trace()
            kwargs['date_line'] = kwargs['l_num'] + 1
    else:
        kwargs['date_obj'] = get_pdf_quarter(year_end=kwargs['year_end'], word_list=kwargs['line'].split(), pdf_type=kwargs['pdf_type'],
                                   date_obj=kwargs['date_obj'],
                                             data=kwargs['data'],l_num=kwargs['l_num'])
        if len(kwargs['date_obj']) < 1:
            kwargs['date_obj'] = []

        else:
            # import pdb;pdb.set_trace()
            kwargs['date_line'] = kwargs['l_num'] + 1
    return  kwargs['date_obj'],kwargs['date_line']