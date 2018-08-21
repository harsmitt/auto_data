from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
from .statements_page import *
from .utils import *

index_list =['balance sheets','operations','income','notes','balance sheet']
financial_statement =['financial statements and supplementary data',
                      'financial content']##'exhibits and financial statement',


def get_page_num(l_num,**kwargs):
    line = kwargs['data'][l_num]
    n_line = kwargs['data'][l_num+1] if (len(kwargs['data'])-1!=l_num+1) else ''
    if n_line:

        if line.split()[-1].split('-')[0].isdigit():
            c_num = line.split()[-1].split('-')[0]
            next_num =next_num_page(data=kwargs['data'],line_num=l_num,i=0,index = -1)

        elif line.split()[0].split('-')[0].isdigit():
            c_num=line.split()[0].split('-')[0]
            next_num = next_num_page(data=kwargs['data'],line_num=l_num,i=0,index = 0)

        if (int(next_num) - int(c_num)) > 1 :
            if kwargs['section_name'] in kwargs['page_detail']:
                kwargs['page_detail'][kwargs['section_name']].update({kwargs['key_name']: c_num + '-' + next_num})
            else:
                kwargs['page_detail'].update({kwargs['section_name']: {kwargs['key_name']: c_num + '-' + next_num}})

    else:
        c_num = line.split()[-1].split('-')[0] if line.split()[-1].split('-')[0].isdigit() else line.split()[0].split('-')[0]
        if kwargs['section_name'] in kwargs['page_detail']:
            kwargs['page_detail'][kwargs['section_name']].update({kwargs['key_name']: c_num})
        else:
            kwargs['page_detail'].update({kwargs['section_name']: {kwargs['key_name']: c_num }})
    return kwargs['page_detail']



def table_content(**kwargs):
    statement_find=False
    old_value={}
    try:
        if any(i in ' '.join(kwargs['data']) for i in ['table of contents','table of content','index','contents','page no'] ):
            for l_num, line in enumerate(kwargs['data']):
                print (line)
                if statement_find:break;

                if 'statement_section' in kwargs['page_detail']:
                    old_value = kwargs['page_detail']['statement_section']

                if not statement_find and  all(word in get_alpha(line) for word in ['management','discussion']):
                    kwargs['page_detail'] = get_page_num(l_num,section_name='notes_section',key_name='discussion',
                                                         data=kwargs['data'],
                                                         page_detail= kwargs['page_detail'])

                elif not statement_find and any(word in get_alpha(line) for word in financial_statement):
                    kwargs['page_detail'] = get_page_num(l_num, section_name='statement_section', key_name='statement',
                                                         data=kwargs['data'],page_detail=kwargs['page_detail'])
                    statement_page,n_dict = get_financial_statements(path=kwargs['path'],file=kwargs['file'],item_no=line,statement= kwargs['page_detail']['statement_section']['statement'])

                    if statement_page:
                        statement_find=True
                        kwargs['page_detail']['statement_section']=statement_page

                    else:
                        if old_value :
                            kwargs['page_detail']['statement_section']=old_value

                    if n_dict and old_value:
                        if len(n_dict['notes'].split('-')) == 1:
                            n_dict['notes'] = n_dict['notes'] + '-' + old_value['statement'].split('-')[1]

                    if n_dict and 'notes_section' in kwargs['page_detail']:
                        kwargs['page_detail']['notes_section'].update(n_dict)

                    elif n_dict and not 'notes_section' in kwargs['page_detail']:
                        kwargs['page_detail'].update({'notes_section':n_dict})

                elif not statement_find and any(index in get_alpha(line) for index in index_list):
                    statements_page, n_dict = financial_page(line=line, data=kwargs['data'], line_num=l_num, i=0, index=-1)
                    ##if page number at the starting of a line
                    if not statements_page and not n_dict:
                        statements_page, n_dict = financial_page(line=line, data=kwargs['data'], line_num=l_num, i=0, index=0)

                    if statements_page:

                        if 'statement_section' in kwargs['page_detail']:
                            key = list(statements_page.keys())[0]
                            if not key in kwargs['page_detail']['statement_section']:
                                kwargs['page_detail']['statement_section'].update(statements_page)
                        else:
                            kwargs['page_detail'].update({'statement_section': statements_page})

                    if n_dict:

                        if 'notes_section' in kwargs['page_detail']:
                            kwargs['page_detail']['notes_section'].update(n_dict)
                        else:
                            kwargs['page_detail'].update({'notes_section': n_dict})

    except:
        return kwargs['page_detail']
    return kwargs['page_detail']