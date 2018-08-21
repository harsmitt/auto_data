import re
import datetime
import tempfile, subprocess
from .basic_functions import *
from .mapping_data import k_list, stop_words
from collections import OrderedDict
# from BalanceSheet.models import *
from DataExtraction.logger_config import logger

'''
This function converts pdf page in text format. 
we are using pdftotext and conversion will be perform in  horizontal way.
removing unnecessary spacing, special chars,tabs,blank lines,decode etc.

Input:  page,path

output: return text format data or an exception
'''


def get_page_content(seprator=' ', **kwargs):
    try:
        pdfData = kwargs['file'].read()
        tf = tempfile.NamedTemporaryFile()
        tf.write(pdfData)
        tf.seek(0)
        outputTf = tempfile.NamedTemporaryFile()
        args = ['pdftotext', '-f', str(kwargs['page']), '-l', str(kwargs['page']), '-layout', '-enc', 'UTF-8', '-q',
                kwargs['path'],
                outputTf.name]
        txt = subprocess.check_output(args)
        data = outputTf.readlines()

        data = [i.decode('utf-8').replace('\xa0', ' ') for i in
                data]  # [re.sub(r'[^\x00-\x7A]',  '' , i.decode('utf-8')) for i in data]
        data = [i.lower().strip() for i in data if i != '\n'] if seprator == ' ' else [i.strip() for i in data if
                                                                                       i != '\n']
        # data= [re.sub('\s+', '     ', line) for line in data]
        data = [i.replace('\t', '  ').replace('\n', '') for i in data]
        data = [i for i in data if i != '']
        # data = [line.replace('  @@', ' - ').strip() for line in data]
        # data = [line.replace('@@', ' ').strip() for line in data]

        return data
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in get data %s " % e)
        return e


def check_content(**kwargs):
    try:
        k_words = [get_alpha(i.lower(), remove_space=True, remove_s=True) for i in k_list[kwargs['p_type']]]
        data = kwargs['data'] if type(kwargs['data']) == list else [kwargs['data']]
        for l_num, line in enumerate(data):
            if get_alpha(line.lower(), remove_s=True) in k_list[kwargs['p_type']] and not 'check_statement' in kwargs:
                return True
            elif get_alpha(line.lower(), remove_space=True,
                           remove_s=True) in k_words and not 'check_statement' in kwargs:
                return True
            else:
                for i in k_list[kwargs['p_type']]:
                    if (all((loop in get_alpha(line, remove_space=True, remove_s=True)) or (
                        loop in get_alpha(line, remove_space=True)) \
                            for loop in [word for word in i.lower().split() if word not in stop_words])) or \
                            (all((loop in get_alpha(' '.join(data), remove_space=True, remove_s=True)) or (
                                loop in get_alpha(' '.join(data), remove_space=True)) \
                                 for loop in [word for word in i.lower().split() if word not in stop_words])):
                        return True
        return False
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for values %s " % kwargs['data'])
        return e


'''
We need this function when we are iterating the complete pdf.
In this function we are getting the keyword lists for match_re.
and try to match those keywords one by one with our patterns.
e.g for bsheet  we have these ['balance sheet','financial position',
                        'consolidated balance sheet',
                        'consolidated statement of financial position',
                    'consolidated statement of balance sheet'] keywords

match keywords with regex 
1.removing s from the lines and then join the lines back. 
    if it is true then another condition will be check if the next 5
    lines are in tabular format only then it will retunr tru 
2. removing all s and space from the line then try to match with keywords 


Input: page, path, f_obj(file object), match_re='bsheet'

Output :Return True/False
'''


def match_re_list(**kwargs):
    try:
        from .all_regex import check_1, check_2
        data = get_page_content(seprator='@@', page=kwargs['page'], path=kwargs['path'], file=kwargs['f_obj'])
        keywords_list = k_list[kwargs['match_re']]
        for keys in keywords_list:
            re_1 = re.compile(check_1, re.I)
            r2 = check_2 % (keys)
            r3 = check_2 % (get_alpha(keys, remove_space=True))
            re_2 = re.compile(r2, re.I)
            re_3 = re.compile(r3, re.I)
            if [line for line in data if all(word in extract_s(line).split() for word in keys.split())] or \
                    (re_1.search(extract_s(' '.join(data))) and re_2.search(extract_s(' '.join(data)))) or \
                    re_2.search(extract_s(' '.join(data))):
                prev_line = [num for num, line in enumerate(data) if re_2.search(extract_s(line))]
                prev_l_num = prev_line[-1] if prev_line else 0

                res = check_in_re(data=data[prev_l_num:], r_1=re_1, r_2=re_2)
                if not res or prev_l_num > 20:
                    next_data = get_page_content(seprator='@@', page=int(kwargs['page']) + 1, path=kwargs['path'],
                                                 file=kwargs['f_obj'])
                    res = check_in_re(data=next_data[:10], r_1=re_1, r_2=re_2)
                    if res: data = data[prev_l_num - 1:] + next_data
                return data, res
            elif re_1.search(get_alpha(' '.join(data), remove_space=True)) and re_3.search(
                    get_alpha(' '.join(data), remove_space=True)):

                return data, True

        return data, False
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for values %s " % str(data))
        return e


'''
inner function for match_re_list it will check the next minimum 5 lines should be in tabuler format 

'''


def check_in_re(**kwargs):
    try:
        if any(word in (' '.join(kwargs['data']).lower()) for word in
               ['supplementary financial data', 'summary of', 'summarized as', 'overview of', 'comparison between',
                'financial summary', 'financial comparison']):
            return False

        x = [i for i in kwargs['data'] if num_there(i.split()[-1]) and not check_datetime(i.split()[-1], pdf_type=True)]
        if len(x) > 5:
            return True

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for values %s " % kwargs['data'])
        return e


import copy


def remove_extra_keys(**kwargs):
    try:
        data_dict = copy.deepcopy(kwargs['data_dict'])
        for i, j in data_dict.items():
            if type(j) == OrderedDict:
                for inn, inn_d in j.items():
                    if not inn_d:
                        del data_dict[i][inn]
            elif not j:
                del data_dict[i]
        return data_dict
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in remove_extra_keys for data :%s " % data_dict)
        return e


def valid_yq_name(date_obj, y_end, pdf_type=None, p_type=None, ):
    try:
        date_dict = year_date(year_end=y_end) if pdf_type == 'year' else qtr_date(year_end=y_end)
        for key, val in date_dict.items():
            if pdf_type == 'year':
                if int(date_obj) == int(val):
                    val = val
                    return val
            else:
                last_month, next_month = next_last_month(val)
                if date_obj.lower() == val.lower() or date_obj.lower() == last_month.lower() or date_obj.lower() == next_month.lower():
                    val = val
                    return val


    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in remove_extra_keys for data :%s " % data_dict)
        return e


# sort the years list in descending order to get always latest data of the year.
def y_sorting(year_list):
    try:
        list1 = [int(i.split('.')[0]) for i in year_list]
        for loop1 in range(0, len(list1)):
            for i, j in enumerate(list1):
                if len(list1) > 1 and len(list1) != (i + 1):
                    if list1[i] < list1[i + 1]:
                        temp = list1[i]
                        list1[i] = list1[i + 1]
                        list1[i + 1] = temp
        return list1
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error  for data :%s " % year_list)
        return e


# sort the qtrs in descending order to get always latest data of qtr.
def q_sorting(q_list):
    try:
        # logger1.info("Entering in q_sorting")
        name_list = [i.split('.pdf')[0].replace('_', ' ') for i in q_list]
        for loop in range(0, len(name_list)):
            for i, j in enumerate(name_list):
                if len(name_list) > 1 and len(name_list) != (i + 1):
                    if datetime.strptime(name_list[i], '%B %Y') < datetime.strptime(name_list[i + 1], '%B %Y'):
                        temp = name_list[i]
                        name_list[i] = name_list[i + 1]
                        name_list[i + 1] = temp
        return name_list
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for data :%s " % q_list)
        return e


# get qtr_dates mention in pdf page.
def get_pdf_quarter(**kwargs):
    try:
        q_list, y_list = [], []
        qtr_list = qtr_date(kwargs['year_end']).values()
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
        if (q_list and not y_list) or (y_list and not q_list) or (
                len(q_list) == 1 and len(y_list) == 1):  # >=1 and len(y_list)!=2 or len(q_list)!=2 and len(y_list)==2 :
            num = kwargs['l_num'] + 1
            while num <= kwargs['l_num'] + 5:
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
                    if q_list and y_list:
                        break;
                    else:
                        num += 1
                else:
                    num += 1
        if len(q_list) * 2 == len(y_list):
            q_list = q_list * 2
        elif len(y_list) * 2 == len(q_list):
            y_list = y_list * 2

        if len(q_list) == len(
                y_list):  # (len(q_list)>=1 and len(q_list)<=2 and len(y_list)==2) or (len(y_list)>=1 and len(y_list)<=2 and len(q_list)==2) :

            if len(q_list) == 2:
                if kwargs['year_end'].lower() in q_list:
                    yend_index = q_list.index(kwargs['year_end'].lower())
                    if max(y_list) == y_list[yend_index]:
                        y_list.append(max(y_list))
                        del y_list[yend_index]

            for i in list(zip(q_list, y_list)):
                q_date = ' '.join(i)
                last_month, next_month = next_last_month(q_date)
                kwargs['date_obj'].append(q_date)

        return kwargs['date_obj']


    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in fetching quarter date :%s " % str(kwargs))
        return e


def calculations(old, new):
    try:
        year, values = map(list, zip(*old))
        new = list(map(lambda num: get_digit(num), list(filter(lambda x: num_there(x), new))))
        new_values = [a + b for a, b in zip(values, new)]
        return new_values
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in calculation for values :%s , %s" %(old,new))
        return e

def get_date_obj(**kwargs):
    for d_obj in kwargs['word_list']:
        d_obj = d_obj.replace(',', '').replace('*', '').split('/')
        for objs in d_obj:
            list_obj = objs.split('.')
            for obj in list_obj:
                if check_datetime(obj, pdf_type='year'):
                    if kwargs['pdf_type'] == 'year':
                        year_list = year_date(year_end=kwargs['year_end']).values()
                        if obj not in kwargs['date_obj']:
                            kwargs['date_obj'].append(obj)
                    else:
                        pass

    return kwargs['date_obj']

def get_date(**kwargs):
    try:
        kwargs['date_obj'] = get_date_obj(word_list=kwargs['word_list'],year_end = kwargs['year_end'],
                                          pdf_type=kwargs['pdf_type'],date_obj=kwargs['date_obj'])
        if len(kwargs['date_obj'])==1:
            num=kwargs['l_num']+1
            while num <= kwargs['l_num'] + 3:
                if num_there(kwargs['data'][num]):
                    word_list = kwargs['data'][num].split()

                    kwargs['date_obj'] = get_date_obj(word_list=word_list, year_end=kwargs['year_end'],
                                                      pdf_type=kwargs['pdf_type'], date_obj=kwargs['date_obj'])
                    if len(kwargs['date_obj'])>1:
                        break;
                    num+=1
                else:
                    num+=1


        if kwargs['date_obj']:
            date_o = list(map(lambda x: int(x), kwargs['date_obj']))
            range_o = list(range(min(date_o), max(date_o) + 1))
            if sorted(date_o) == range_o:
                return kwargs['date_obj']
            else:
                kwargs['date_obj'] = []
                return kwargs['date_obj']

        return kwargs['date_obj']
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in fetching year date  :%s " % kwargs)
        return e


def check_date_obj(**kwargs):
    try:
        if kwargs['pdf_type'] == 'year':
            kwargs['date_obj'] = get_date(year_end=kwargs['year_end'], word_list=kwargs['line'].split(),
                                          pdf_type=kwargs['pdf_type'],data=kwargs['data'], l_num=kwargs['l_num'],
                                          date_obj=kwargs['date_obj'])
            if len(kwargs['date_obj']) < 2:
                kwargs['date_obj'] = []
            else:
                kwargs['date_line'] = kwargs['l_num'] + 1
        else:
            # get_quarter_date(data=kwargs['data'],l_num=kwargs['l_num'],line = kwargs['line'],year_end=kwargs['year_end'],date_obj=kwargs['date_obj'] )
            kwargs['date_obj'] = get_pdf_quarter(year_end=kwargs['year_end'], word_list=kwargs['line'].split(),
                                                 pdf_type=kwargs['pdf_type'],
                                                 date_obj=kwargs['date_obj'],
                                                 data=kwargs['data'], l_num=kwargs['l_num'])
            if len(kwargs['date_obj']) < 1:
                kwargs['date_obj'] = []

            else:
                kwargs['date_obj'] = [i for num, i in enumerate(kwargs['date_obj']) if
                                      i not in kwargs['date_obj'][num + 1:]]
                kwargs['date_line'] = kwargs['l_num'] + 1
        return kwargs['date_obj'], kwargs['date_line']
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for data :%s " % kwargs)
        return e
