from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
from DataExtraction.common_files.add_blank_in_data import *
import copy
from collections import OrderedDict
from .extract_balance_sheet import ExtractBalnceSheet

from .save_data import *

def get_ignore_index(**kwargs):
    g_index = None
    c_index = None
    n_index = None
    ignore_index={}
    date_obj= kwargs['date_obj']
    for l_num in range(kwargs['l_num'],len(kwargs['data'])):
        line = kwargs['data'][l_num].lower()
        if all(word in line for word in ['group','company']):
            group = [word for word in line.split() if 'group' in word ]
            g_index = re.split('  +',line).index(group[0])+1 if group else None
            company = [word for word in line.split() if 'company' in word]
            c_index = re.split('  +',line).index(company[0])+1 if company else None
        if any( 'note' in word  for word in line.split()):
            notes = [word for word in line.split() if 'note' in word]
            if ('assets' in line or 'liabilities' in line) or ('note' not in  line.split()[0] and not any(check_datetime(obj) for obj in line.split()[0] )):
                n_index = re.split('  +',line).index(notes[0]) if notes and notes[0] in re.split('  +',line) else None
            else:
                n_index = re.split('  +',line).index(notes[0])+1 if notes and notes[0] in re.split('  +',line) else None

            if not any(i in line for i in ['group','company']):
                date_obj = get_date(word_list =line.split(),pdf_type = kwargs['pdf_type'],
                                    date_obj=kwargs['date_obj'])
        if n_index and g_index and c_index and not kwargs['date_obj']:
            date_obj = get_date(word_list =line.split(),pdf_type = kwargs['pdf_type'],date_obj=kwargs['date_obj'])

        if g_index and c_index  and kwargs['date_obj']:
            if g_index < c_index :
                for i in range(1,len(date_obj)+1):
                    key = 'c_y'+str(i)
                    c_in_dict ={key:-(int(i))}
                    ignore_index.update(**c_in_dict)
            else:
                for i in range(1,len(date_obj)+1):
                    key = 'c_y'+str(i)
                    c_in_dict ={key:n_index+(int(i))} if n_index else {key:(int(i))}
                    ignore_index.update(**c_in_dict)
            if n_index : ignore_index.update({'notes':n_index})

            break;

        elif n_index:
            ignore_index.update({'notes': n_index})
            break;

    return ignore_index,date_obj

def get_pdf_quarter(**kwargs):
    q_list, y_list = [], []
    qtr_list = qtr_date(year_end=kwargs['year_end']).values()
    for obj in kwargs['word_list']:
        if check_datetime(obj):
            print (obj)
            try:
                if type(datetime.strptime(obj, '%B')) == datetime:
                    q_list.append(obj)
            except:
                try:
                    if type(datetime.strptime(obj, '%Y')) == datetime:
                        y_list.append(obj)
                except:
                    pass

    if len(q_list)==2 and len(y_list)!=2 or len(q_list)!=2 and len(y_list)==2 :
        for obj in kwargs['next_line'].split():
            try:
                if type(datetime.strptime(obj, '%B')) == datetime:
                    q_list.append(obj)
            except:
                try:
                    if type(datetime.strptime(obj, '%Y')) == datetime:
                        y_list.append(obj)
                except:
                    pass

    if len(q_list)==2 and len(y_list)==2:
        for i in list(zip(q_list, y_list)):
            if ' '.join(i) in qtr_list:
                kwargs['date_obj'].append(' '.join(i))

    return kwargs['date_obj']



def get_date(**kwargs):
    for obj in kwargs['word_list']:
        if check_datetime(obj):
            if kwargs['pdf_type']=='year':
                year_list =year_date(year_end=kwargs['year_end']).values()
                if obj in year_list and obj not in kwargs['date_obj']:
                    kwargs['date_obj'].append(obj)
            else:
                print ('quarter')

    return kwargs['date_obj']


def scrap_pdf_page(**kwargs):
    date_obj=[]
    ignore_index ={}
    data_dict = OrderedDict()
    p_num = kwargs['p_num'].split('-')
    pdf_page = copy.deepcopy(p_num[0])
    loop = 1 if 'data' in kwargs else 10
    pdf_page_next = int(int(p_num[-1])- int(p_num[0])) if len(p_num)==2  else 1
    for i in range(loop):
        data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
        print (data)

        if all(i in ' '.join(data[:10]).lower() for i in kwargs['pdf_page'].split()):
            for l_num,line in enumerate(data[:20]):
                print (line)

                import itertools
                # if not ignore_index:
                #     for loop in range(len(['group','company','notes'])+1):
                #         for subset in itertools.combinations(['group','company','notes'],loop):
                #             if subset == line.lower() :
                #

                ## todo list should be rewrite


                if not ignore_index and any(re.search(r'\b' + word + r'\b',  line.lower()) for word in ['group','company','notes']) and len(line.split())<6:
                    ignore_index,date_obj = get_ignore_index(data=data,l_num=l_num,pdf_type=kwargs['pdf_type'],date_obj=date_obj)
                    break;
                elif not date_obj and not ignore_index:
                    if kwargs['pdf_type']=='year':
                        date_obj = get_date(year_end=kwargs['year_end'],word_list =line.split(),pdf_type = kwargs['pdf_type'],date_obj=date_obj)
                    else:
                        date_obj = get_pdf_quarter(year_end=kwargs['year_end'],word_list =line.split(),pdf_type = kwargs['pdf_type'],date_obj=date_obj,next_line = data[l_num+1])
                    if len(date_obj) <2:
                        date_obj=[]
            if date_obj:
                for pdf in range(pdf_page_next):
                    if kwargs['pdf_page']=='balance sheet':
                        data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
                        data_dict = ExtractBalnceSheet(data_dict=data_dict,data=data,ignore_index=ignore_index,date_obj=date_obj)
                        if data_dict:
                            img_path, c_name = Create_blank_sheet(year_end=kwargs['year_end'],c_name=kwargs['c_name'], path=kwargs['path'], page=pdf_page)
                            status = match_keyword(year_end=kwargs['year_end'],data=data_dict, img_path=img_path, page=i, c_name=c_name,new_dict=True,pdf_type = kwargs['pdf_type'])
                            return status
                            # pdf_page = str(int(pdf_page) + 1)
            else:
                print (data[-2].split()[-1])
                pdf_page = str(int(pdf_page) + 1)


        else:
            print (data[-2].split()[-1])
            pdf_page = str(int(pdf_page) + 1)

    return False