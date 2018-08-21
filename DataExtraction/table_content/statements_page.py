
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
from .utils import *
import re



def notes_section(**kwargs):
    try:
        next_index = -2 if int(kwargs['index']) == -1 else 1
        if len(kwargs['data']) - 1 > kwargs['line_num'] + 1:
            ending_notes = next_num_page(data=kwargs['data'], line_num=kwargs['line_num'], i=kwargs['i'], index=int(kwargs['index']))
        if kwargs['line'].split()[next_index] == '-':
            n_dict = {'notes': kwargs['line'].split()[-3] + '-' + kwargs['num']} if int(kwargs['index'])== -1 \
                else {'notes': kwargs['num'] + '-' + kwargs['line'].split()[2]}

        else:
            n_dict = {'notes': kwargs['num'] + '-' + ending_notes} if ending_notes else {'notes': kwargs['num']}

        return n_dict
    except Exception as e:
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in notes section notes section %s " % str(e))
        pass

def financial_page(**kwargs):
<<<<<<< HEAD
    temp_dict , n_dict={},{}
    if any(i in kwargs['line'].split()[int(kwargs['index'])] for i in ['and',',']) or check_datetime(kwargs['line'].split()[int(kwargs['index'])]):
        line = kwargs['line'] + '' + kwargs['data'][kwargs['line_num'] + 1]
    else:line=kwargs['line']
    if line.split()[int(kwargs['index'])].split('-')[0].isdigit() and not check_datetime(line.split()[0]):
        num = str(int(line.split()[int(kwargs['index'])].split('-')[0]) + kwargs['i'])
        index = [index for index in index_list if index in get_alpha(line)][0]
        if index == 'notes' and 'notes' in line:
            n_dict = notes_section(data=kwargs['data'], line_num=kwargs['line_num'], line=line, num=num, i=kwargs['i'], index=kwargs['index'])
        else:
            if len(kwargs['data']) - 1 > kwargs['line_num'] + 1:
                check_next_num = next_num_page(data=kwargs['data'], line_num=kwargs['line_num'], i=kwargs['i'], index=kwargs['index'])
=======
    try:
        temp_dict , n_dict={},{}
        if any(i in kwargs['line'].split()[int(kwargs['index'])] for i in ['and',',']) or check_datetime(kwargs['line'].split()[int(kwargs['index'])]):
            line = kwargs['line'] + '' + kwargs['data'][kwargs['line_num'] + 1]
        else:line=kwargs['line']
        if line.split()[int(kwargs['index'])].split('-')[0].isdigit() and not check_datetime(line.split()[0]):
            num = str(int(line.split()[int(kwargs['index'])].split('-')[0]) + kwargs['i'])
            # index = [index for index in index_list if index in get_alpha(line)][0]
            if kwargs['key'] == 'notes' and 'notes' in line:
                n_dict = notes_section(data=kwargs['data'], line_num=kwargs['line_num'], line=line, num=num, i=kwargs['i'], index=kwargs['index'])
            else:
                if len(kwargs['data']) - 1 > kwargs['line_num'] + 1:
                    check_next_num = next_num_page(data=kwargs['data'], line_num=kwargs['line_num'], i=kwargs['i'], index=kwargs['index'])
>>>>>>> feature-automationv2

                temp_dict = {kwargs['key']: num + '-' + check_next_num} if check_next_num and int(
                    check_next_num) - int(num) > 1 else {kwargs['key']: num}
        return temp_dict,n_dict
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in table content financial page %s " % str(e))
        return e


def get_financial_statements(**kwargs):
<<<<<<< HEAD

    statements_page, n_dict = {}, {}

    next_num = ''
    page_num = kwargs['statement'].split('-')[0]
    if len(kwargs['statement'].split('-'))>1:next_num=kwargs['statement'].split('-')[1]
    for i in range(10):
        if not next_num or (int(next_num) - int(page_num)) > 1:
            data = get_page_content(page=page_num, path=kwargs['path'], file=kwargs['file'])
            item = get_alpha(kwargs['item_no'].split('.')[1].strip()) if len(kwargs['item_no'].split('.'))>1\
                        else get_alpha(kwargs['item_no'].split('.')[0].strip())

            if (item in get_alpha(' '.join(data))):
                for line_num,line in enumerate(data):
                    print(line)
                    if line and any(index in get_alpha(line) for index in index_list):


                        ##if page number at the end of line
                        t_dict,notes = financial_page(line=line,data=data,line_num=line_num,i=i,index=-1)

                        ##if page number at the starting of a line
                        if not t_dict and not  notes :
                            t_dict, notes = financial_page(line=line, data=data, line_num=line_num, i=i, index=0)

                        if statements_page:
                            if t_dict:
                                key = list(t_dict.keys())[0]
                            elif notes :
                                key = list(notes.keys())[0]
                            if not key in statements_page:
                                statements_page.update(t_dict)
                        else:
                            statements_page.update(t_dict)

                        n_dict.update(notes)

                return statements_page,n_dict
                break;
            else:
                page_num = int(page_num) + 1
                next_num  = int(next_num)+1 if next_num else ''
    return statements_page
=======
    try:

        statements_page, n_dict = {}, {}

        next_num = ''
        page_num = kwargs['statement'].split('-')[0]
        if len(kwargs['statement'].split('-'))>1:next_num=kwargs['statement'].split('-')[1]
        for i in range(10):
            if not next_num or (int(next_num) - int(page_num)) > 1:
                data = get_page_content(page=page_num, path=kwargs['path'], file=kwargs['file'])
                item = get_alpha(kwargs['item_no'].split('.')[1].strip()) if len(kwargs['item_no'].split('.'))>1\
                            else get_alpha(kwargs['item_no'].split('.')[0].strip())

                if (item in get_alpha(' '.join(data))):
                    for line_num,line in enumerate(data):
                        key = ''
                        if line :#and any(index in get_alpha(line) for index in index_list):
                            if check_content(data=line, p_type='bsheet'):
                                key = 'bsheet'
                            elif check_content(data=line,p_type='pnl'):
                                key = 'pnl'
                            elif 'note' in get_alpha(line.lower(),remove_s=True):
                                key = 'notes'
                            if key:
                                ##if page number at the end of line
                                t_dict,notes = financial_page(line=line,data=data,key=key,line_num=line_num,i=i,index=-1)

                                ##if page number at the starting of a line
                                if not t_dict and not  notes :
                                    t_dict, notes = financial_page(line=line, data=data,key=key, line_num=line_num, i=i, index=0)

                                if statements_page:
                                    if t_dict:
                                        key_1 = list(t_dict.keys())[0]
                                    elif notes :
                                        key_1 = list(notes.keys())[0]
                                    if not key_1 in statements_page:
                                        statements_page.update(t_dict)
                                else:
                                    statements_page.update(t_dict)

                                n_dict.update(notes)

                    return statements_page,n_dict
                    break;
                else:
                    page_num = int(page_num) + 1
                    next_num  = int(next_num)+1 if next_num else ''
        return statements_page
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in table content get_financial_statements %s " % str(e))
>>>>>>> feature-automationv2



