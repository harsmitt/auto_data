from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
from .add_blank_in_data import *
import copy
from collections import OrderedDict
from PNL.extract_pnl import ExtractPNL
from PNL.get_notes_data import *
from BalanceSheet.balance_sheet.extract_balance_sheet import ExtractBalnceSheet

from BalanceSheet.balance_sheet.save_data import *
from PNL.save_pnl import *



def get_ignore_index(**kwargs):
    g_index = None
    c_index = None
    n_index = None
    ignore_index={}
    date_obj= kwargs['date_obj']
    date_line=0
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
                # date_obj,date_line = get_date(word_list =line.split(),pdf_type = kwargs['pdf_type'],
                #                     date_obj=kwargs['date_obj'],year_end=kwargs['year_end'])
                next_line = kwargs['data'][l_num + 1] if len(kwargs['data']) > l_num + 1 else ''

                date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                               year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
                               date_line=date_line, data=kwargs['data'],
                               next_line=next_line, l_num=l_num)

        if n_index and g_index and c_index and not kwargs['date_obj']:
            next_line = kwargs['data'][l_num + 1] if len(kwargs['data']) > l_num + 1 else ''

            date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                 year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
                                                 date_line=date_line, data=kwargs['data'],
                                                 next_line=next_line, l_num=l_num)


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

    return ignore_index,date_obj,date_line




def scrap_pdf_page(**kwargs):
    date_obj=[]
    date_line=0
    ignore_index ={}
    data_dict = OrderedDict()
    p_num = kwargs['p_num'].split('-')
    pdf_page = copy.deepcopy(p_num[0])
    loop = 1 if 'data' in kwargs else 10
    pdf_page_next = int(int(p_num[-1])- int(p_num[0])) if len(p_num)==2  else 1
    for i in range(loop):
        data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
        print (data)

        if any(i in ' '.join(data[:10]).lower() for i in kwargs['pdf_page']):
            for l_num,line in enumerate(data[:20]):
                print (line)
                import itertools
                # if not ignore_index:
                #     for loop in range(len(['group','company','notes'])+1):
                #         for subset in itertools.combinations(['group','company','notes'],loop):
                #             if subset == line.lower() :
                #

                ## todo list should be rewrite

                if line and not ignore_index and any(re.search(r'\b' + word + r'\b',  line.lower()) for word in ['group','company','notes','note']) and len(line.split())<6:
                    ignore_index,date_obj,date_line = get_ignore_index(year_end=kwargs['year_end'],data=data,l_num=l_num,pdf_type=kwargs['pdf_type'],date_obj=date_obj)
                    if date_obj:break;
                elif line and not date_obj and not ignore_index:
                    next_line = data[l_num + 1] if len(data) > l_num + 1 else ''

                    date_obj,date_line = check_date_obj(pdf_type=kwargs['pdf_type'],line = line,
                                                        year_end=kwargs['year_end'],date_obj=date_obj,
                                                        date_line =date_line,data=data,
                                                        next_line= next_line,l_num=l_num)
                    if date_obj : break;



            if date_obj:
                # for pdf in range(pdf_page_next):
                if 'balance sheet' in kwargs['pdf_page']:
                    for pdf in range(pdf_page_next):
                        pdf_page = int(pdf_page)+pdf

                        data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
                        data_dict = ExtractBalnceSheet(date_line=date_line,data_dict=data_dict,data=data,ignore_index=ignore_index,date_obj=date_obj)

                    if data_dict:
                        img_path, c_name = Create_blank_sheet(year_end=kwargs['year_end'],c_name=kwargs['c_name'], path=kwargs['path'], page=pdf_page)
                        status = match_keyword(year_end=kwargs['year_end'],data=data_dict, img_path=img_path, page=i, c_name=c_name,new_dict=True,pdf_type = kwargs['pdf_type'])
                        return True

                elif any(i in kwargs['pdf_page'] for i in  ['income','operations']):
                    for pdf in range(pdf_page_next):
                        pdf_page = int(pdf_page) + pdf

                        data = get_page_content(seprator='@@', page=pdf_page, path=kwargs['path'],file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
                        data_dict = ExtractPNL(date_line=date_line,data_dict=data_dict, data=data, ignore_index=ignore_index,
                                                   date_obj=date_obj)


                    if data_dict and (len(data_dict) > 5 or any('revenue' in x.strip(' s') for x in list(data_dict.keys()))):

                        comp_data = get_notes_data(n_sec = 'pnl',date_obj=date_obj,year_end=kwargs['year_end'],pdf_type=kwargs['pdf_type'],notes_sec=kwargs['notes'],
                                                   path=kwargs['path'], file=kwargs['file'], page_data=data_dict)


                        img_path, c_name = Create_pnl(year_end=kwargs['year_end'], c_name=kwargs['c_name'],
                                                              path=kwargs['path'], page=pdf_page)
                        status = save_pnl(year_end=kwargs['year_end'], data=comp_data, img_path=img_path,
                                               page=i, c_name=c_name, new_dict=True, pdf_type=kwargs['pdf_type'])
                        return True

                        # pdf_page = str(int(pdf_page) + 1)
            else:
                print (data[-2].split()[-1])
                pdf_page = str(int(pdf_page) + 1)


        else:
            print (data[-2].split()[-1])
            pdf_page = str(int(pdf_page) + 1)

    return False