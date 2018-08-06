from .utils import *
from .mapping_data import qtr_combinations
#
# def ignore_qtr_index(**kwargs):
#     try:
#         q1_index = None
#         q2_index = None
#         ignore_index={}
#         date_obj= kwargs['date_obj']
#         date_line=0
#         for l_num in range(kwargs['l_num'],len(kwargs['data'])):
#             line = kwargs['data'][l_num].lower()
#             if [i for i in qtr_combinations if all(word in line for word in i)]:#[i for i in qtr_combinations if all(k1.lower() in i for k1 in re.split('  +',line))]:
#                 qtr1 = [word for word in re.split('  +',line) if kwargs['combination'][0][0] in word ]
#                 q1_index = re.split('  +',line).index(qtr1[0])+1 if qtr1 else None
#                 qtr2 = [word for word in re.split('  +',line) if kwargs['combination'][0][1] in word]
#                 q2_index = re.split('  +',line).index(qtr2[0])+1 if qtr2 else None
#
#             elif not date_obj and not [i for i in qtr_combinations if all(k1.lower() in i for k1 in re.split('  +',line))]:
#                 next_line = kwargs['data'][l_num + 1] if len(kwargs['data']) > l_num + 1 else ''
#                 date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
#                                year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
#                                date_line=date_line, data=kwargs['data'],
#                                next_line=next_line, l_num=l_num)
#
#             elif q1_index and q2_index and not kwargs['date_obj']:
#                 next_line = kwargs['data'][l_num + 1] if len(kwargs['data']) > l_num + 1 else ''
#                 date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
#                                                      year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
#                                                      date_line=date_line, data=kwargs['data'],
#                                                      next_line=next_line, l_num=l_num)
#
#
#
#             elif q1_index and q2_index  and kwargs['date_obj']:
#                 if q1_index < q2_index :
#                     for i in range(1,len(date_obj)+1):
#                         key = 'c_y'+str(i)
#                         c_in_dict ={key:-(int(i))}
#                         ignore_index.update(**c_in_dict)
#                 else:
#                     for i in range(1,len(date_obj)+1):
#                         key = 'c_y'+str(i)
#                         c_in_dict ={key:(int(i))}
#                         ignore_index.update(**c_in_dict)
#                 break;
#
#         return ignore_index,date_obj,date_line
#
#     except Exception as e:
#         return e
#

from .mapping_data import ignore_index_list
from .basic_functions import *
def i_notes_index(**kwargs):#[(notes,group,company),(group,notes),(company,notes),(notes)]
    g_index = None
    c_index = None
    n_index = None
    if all(word in extract_s(kwargs['line']) for word in ['group', 'company','note']):
        group = [word for word in kwargs['line'].split() if word == 'group']
        g_index = re.split('  +', kwargs['line']).index(group[0]) + 1
        company = [word for word in kwargs['line'].split() if word == 'company']
        c_index = re.split('  +',kwargs['line']).index(company[0]) + 1

    elif [i for i in qtr_combinations if all(word in kwargs['line'] for word in i)]:#[i for i in qtr_combinations if all(k1.lower() in i for k1 in re.split('  +',line))]:
        qtr1 = [word for word in re.split('  +',kwargs['line']) if kwargs['combination'][0][0] in word ]
        g_index = re.split('  +',kwargs['line']).index(qtr1[0])+1 if qtr1 else None
        qtr2 = [word for word in re.split('  +',kwargs['line']) if kwargs['combination'][0][1] in word]
        c_index = re.split('  +',kwargs['line']).index(qtr2[0])+1 if qtr2 else None

    notes = [word for word in kwargs['line'].split() if 'note' in word ]
    num_list = [i for i in re.split('  +',kwargs['line']) if num_there(i)]
    if notes and \
            len(list(filter(lambda x: str(get_digit(x)), num_list))) == len(kwargs['date_obj']) \
            and not any(get_alpha(x) for x in  re.split('  +',kwargs['line'])[1:]) \
            and (not all(check_datetime(obj) for obj in list(filter(lambda x: str(get_digit(x)), re.split('  +',kwargs['line'])))))\
            :


        return kwargs['ignore_index']
    elif notes and any( word in kwargs['line']for word in ['statement','receivable']):
        return kwargs['ignore_index']


    elif not any(word in extract_s(kwargs['line']).split()[0] for word in ['notes','note']) and \
            (any(check_datetime(obj) for obj in extract_s(kwargs['line']).split()) or 'except share data' in kwargs['line'].lower()):
        n_index = re.split('  +',kwargs['line']).index(notes[0]) if len(re.split('  +',kwargs['line']))>1 \
                else -1
    elif any(word in extract_s(kwargs['line']).split()[-1] for word in ['notes','note']) and len(extract_s(kwargs['line']).split())>1:
        n_index= -1
    else:
        if any(word in re.split('  +',kwargs['line']) for word in ['notes','note']) :
            n_index = re.split('  +',kwargs['line']).index(notes[0])+1
        else: kwargs['ignore_index']

#need to add keys

    if g_index and c_index and n_index:
        # notes will be the last column
        if g_index < c_index and c_index < n_index :
            for i in range(2, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict ={key:-(int(i))}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':-1})
        # notes will be in between group and company
        elif g_index < c_index and c_index> n_index:
            for i in range(1, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict ={key:1(int(i))}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':-int(len(kwargs['date_obj']+1))})

        # notes is first column and company is last
        elif n_index <g_index and g_index <c_index:

            for i in range(1, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict ={key:-(int(i))}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':1})

        # company is the first column and notes is last
        elif c_index < g_index and g_index < n_index:
            for i in range(1, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict = {key: int(i)}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':-1})

        # company is first column and notes is second
        elif c_index < g_index and n_index <g_index :
            for i in range(1, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict = {key: int(i)}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':int(len(kwargs['date_obj']+1))})

       # company is second and notes is first
        elif n_index < g_index and g_index > c_index:
            for i in range(2, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict = {key: int(i)}
                kwargs['ignore_index'].update(**c_in_dict)
            kwargs['ignore_index'].update(**{'notes':int(1)})
    else:
        if n_index is not None:
            kwargs['ignore_index'].update(**{'notes':n_index})

    return kwargs['ignore_index']


def i_company_index(**kwargs):#[group,company]
    if len(re.split('  +',kwargs['line']))>2:
        g_index = re.split('  +',kwargs['line']).index('group')+1 if 'group' in re.split('  +',kwargs['line']) else ''
        c_index = re.split('  +',kwargs['line']).index('company')+1 if 'company' in re.split('  +',kwargs['line']) else''
        if g_index and c_index and kwargs['date_obj']:
            if g_index < c_index:
                for i in range(1,len(kwargs['date_obj'])+1):
                    key = 'c_y' + str(i)
                    c_in_dict ={key:-(int(i))}
                    kwargs['ignore_index'].update(**c_in_dict)
                    # kwargs['ignore_index'].append(-(int(i)))
            else:
                for i in range(1,len(kwargs['date_obj'])+1):
                    key = 'c_y' + str(i)
                    c_in_dict ={key:int(i)}
                    kwargs['ignore_index'].update(**c_in_dict)

    return kwargs['ignore_index']


def i_qtr_index(**kwargs):
    g_index =None
    c_index=None
    n_index= None
    if len(re.split('  +', kwargs['line']))>1:
        qtr1 = [word for word in re.split('  +',kwargs['line']) if kwargs['combination'][0] in word ]
        g_index = re.split('  +',kwargs['line']).index(qtr1[0])+1 if qtr1 else None
        qtr2 = [word for word in re.split('  +',kwargs['line']) if kwargs['combination'][1] in word]
        c_index = re.split('  +',kwargs['line']).index(qtr2[0])+1 if qtr2 else None
    else:
        qtr1 = '##'.join(kwargs['line'].split(kwargs['combination'][0]))
        g_index = qtr1.index('##') + 1 if qtr1 else None
        qtr2 = '@@'.join(kwargs['line'].split(kwargs['combination'][1]))
        c_index = qtr2.index('@@')+1 if qtr2 else None

    for l_num in range(kwargs['l_num'], kwargs['l_num'] + 5):
        if len(kwargs['data']) > l_num:
            line = kwargs['data'][l_num].lower();
            if "note" in line.lower():
                if 'note' in extract_s(line).split()[0]:
                    n_index= 1
                elif 'note' in extract_s(line).split()[-1]:
                    n_index=-1
        else:
            break;

    if g_index and c_index and kwargs['date_obj']:
        start=1
        if g_index < c_index:
            if n_index == g_index :
                kwargs['ignore_index']['notes']=1
                start =1
            elif n_index==-1:
                kwargs['ignore_index']['notes'] = -1
                start=2
            for i in range(start, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict = {key: -(int(i))}
                kwargs['ignore_index'].update(**c_in_dict)
                # kwargs['ignore_index'].append(-(int(i)))
        else:
            if n_index == c_index :
                kwargs['ignore_index']['notes'] = 1
                start = 2
            elif n_index==-1:
                kwargs['ignore_index']['notes'] = -1
                start = 1
            for i in range(start, len(kwargs['date_obj']) + 1):
                key = 'c_y' + str(i)
                c_in_dict ={key:int(i)}
                kwargs['ignore_index'].update(**c_in_dict)

    return kwargs['ignore_index']

#code tested for [group,company,notes] combinations
def i_index(**kwargs):
    import copy
    ignore_index_line = copy.deepcopy(kwargs['l_num'])
    for l_num in range(0, ignore_index_line+ 5):
        if len(kwargs['data']) > l_num:
            line = kwargs['data'][l_num].lower()
        else:
            break;
        if not kwargs['date_obj']:
            next_line = kwargs['data'][l_num + 1] if len(kwargs['data']) > l_num + 1 else ''

            kwargs['date_obj'], kwargs['date_line'] = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                             year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
                                             date_line=kwargs['date_line'], data=kwargs['data'],
                                             next_line=next_line, l_num=l_num)
            if kwargs['date_obj'] and kwargs['date_line']:break;

    for l_num in range(kwargs['l_num'], kwargs['l_num'] + 5):
        if len(kwargs['data']) > l_num:
            line = kwargs['data'][l_num].lower();
            if kwargs['pdf_page']=='pnl' and kwargs['pdf_type']=='quarter':
                index_comb=[i for i in qtr_combinations if all(word in line.lower() for word in i)]
            else:
                index_comb = [x for x in ignore_index_list if all(word in extract_s(line) for word in x)]
        else:
            break;

        if index_comb and kwargs['date_obj'] and len(kwargs['date_obj'])<4:
            index_comb =index_comb[0]
            if 'note' in index_comb:
                kwargs['ignore_index'] = i_notes_index(pdf_type=kwargs['pdf_type'],pdf_page=kwargs['pdf_page'],
                                                       date_obj =kwargs['date_obj'],line=line,
                                                       ignore_index =kwargs['ignore_index'])
                if kwargs['date_obj']: break;
            elif len(index_comb)==2 and 'note' not in index_comb:
                if kwargs['pdf_page']=='pnl' and kwargs['pdf_type']=='quarter':
                    kwargs['ignore_index'] = i_qtr_index(combination = index_comb,data=kwargs['data'],l_num=kwargs['l_num'],line=line,ignore_index =kwargs['ignore_index'],date_obj=kwargs['date_obj'])
                    # if kwargs['date_obj']:break;
                else:
                    kwargs['ignore_index'] = i_company_index(line=line,ignore_index =kwargs['ignore_index'],date_obj=kwargs['date_obj'])
                if kwargs['ignore_index']: break;
    return kwargs['ignore_index'],kwargs['date_obj'],kwargs['date_line']




def remove_ignore_index(values,last_notes_no,**kwargs):
    try:
        values = [i for i in values if i != '$']
        ignore_index = list(kwargs['ignore_index'].values())
        ignore_index.sort()
        if 'notes' in kwargs['ignore_index']:
            current_notes = values[kwargs['ignore_index']['notes']] if kwargs['ignore_index']['notes'] < len(values) else ''
            if not get_digit(current_notes,num=True) :# (last_notes_no and not (len(last_notes_no) == len(current_notes))) or
                ignore_index.remove(kwargs['ignore_index']['notes'])
            elif len(values) == len(kwargs['date_obj']) + len(kwargs['ignore_index']) + 1:
                last_notes_no = current_notes if current_notes else last_notes_no

            elif len(values) != len(kwargs['date_obj']) + len(kwargs['ignore_index']) + 1:
                return values, last_notes_no
        for i in ignore_index:
            del values[i]
        return values,last_notes_no
    except Exception as e:
        return e
