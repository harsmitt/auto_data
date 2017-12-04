import re
import datetime
import tempfile,subprocess
from common_functions import *
from datetime import datetime
from collections import OrderedDict
from models import *
# from django.db.models import Q

mapping_dict ={'assets':'current assets','LIABILITIES AND'.lower():'current liabilities','total current assets':'non current assets','total current liabilities':'non current liabilities'}
main_keys_dict=['current assets','current liabilities','non current assets','non current liabilities','long term assets',
                'long term liabilities','shareholders\xe2\x80\x99 equity','stockholders\xe2\x80\x99 equity']

def get_date_obj(date_obj, str1, date_val,qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    get_month = [i for i in str1.split() if not num_there(i)]

    try:
        if len(get_month) in[2,0]:
            if not date_obj and not date_val==True and not get_year:
                date_obj=get_month
            else:
                month_year = zip(date_obj, get_year) if date_obj else zip(get_month,get_year)
                date_obj=[]
                for r1 in month_year:
                    obj = r1[0]+' '+r1[1]
                    d_obj = datetime.strptime(obj, '%B %Y')
                    if type(d_obj) == datetime:
                        date_obj.append(obj)
                qtr_list = qtr_date().values()
                for i in date_obj:
                    last_month,next_month = next_last_month(i)
                    if i in qtr_list or last_month in qtr_list or next_month in qtr_list:
                        date_val=True
                        qtr_exists=True
                        break;
                    else:
                        date_val,qtr_exists = False,False
    except:
        date_val, qtr_exists = False, False

    return date_obj,qtr_exists,date_val

def get_year(date_obj, str1, date_val,qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    if not len(get_year)==2 and not date_obj and date_val==False:
        for i in str1.split():
            try:
                if not num_there(i):
                    d_obj = datetime.strptime(i, '%B')
                    if d_obj and type(d_obj) == datetime:
                        date_obj.append(i)
                else:
                    break;
            except:
                return date_obj,False,date_val
    else:
        if len(get_year) == 2:
            date_obj = get_year
            date_val = True
            qtr_exists=True
    return date_obj, qtr_exists, date_val

def pdftotext(path, page=None,file_type=None,company_name=''):
    qtr_exists=''
    date_val = False
    date_obj = []
    data_dict = OrderedDict()
    file_object = file(path, 'rb')
    pdfData = file_object.read()
    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)
    outputTf = tempfile.NamedTemporaryFile()
    args = ['pdftotext', '-f', str(page), '-l', str(page), '-layout', '-q', path, outputTf.name]
    try:
        txt = subprocess.check_output(args, universal_newlines=True)
        data = outputTf.readlines()
        if page==1:
            str1 = 'Name of Registrant as Specified in its Charter'
            company_name = [data[key - 1].strip() for key, i in enumerate(data) if (str1).lower() in i.lower()]
            return company_name
        else:
            r1 = re.compile('[ (A-Za-z0-9. - )]consolidated balance (sheets|sheet)*[ (A-Za-z0-9. - )$]', re.IGNORECASE)
            if filter(r1.search, data):
                for i in data:
                    # if page ==3:import pdb;pdb.set_trace()
                    if 'total' in i.lower() and 'equity' in i.lower():
                        break;
                    elif i and num_there(i) and not date_val:
                        date_obj,qtr_exists,date_val = get_date_obj(date_obj, i, date_val,qtr_exists) if file_type=='qtr'\
                            else get_year(date_obj, i, date_val,qtr_exists)
                        if qtr_exists==False and len(date_obj)>1:
                            qtr_exists=False
                            break;
                    elif date_val == True:
                        word = i.strip().replace(':', '')
                        if word and len(word) < 100:
                            pass_list = ['Commitments and contingencies', 'LIABILITIES AND', ]
                            if word.lower() in ['assets','equity'] or any(i.lower() in word.lower() for i in pass_list):
                                pass;

                            elif any(i.lower() in word.replace('-',' ').lower() for i in main_keys_dict):
                                if word.lower() in data_dict:
                                    pass
                                else:
                                    data_dict[word.lower().replace('\xe2\x80\x99 ', '-')] = {}

                            elif word.lower() in ['total current assets','total current liabilities']:
                                print ("mahima")
                                data_dict[mapping_dict[word.lower()]]={}
                            #
                            # elif word.lower() in ['shareholders\xe2\x80\x99 equity','stockholders\xe2\x80\x99 equity']:
                            #    data_dict[word.lower().replace('\xe2\x80\x99 ', '-')] = {}

                            # elif data_dict and  not num_there(word) and word.lower() not in ['long-term liabilities']:
                            #     print word
                            #     import pdb;pdb.set_trace()
                            #     if '\xe2\x80\x99' in word:
                            #         word =word.replace('\xe2\x80\x99 ', '-')
                            #     if data_dict[data_dict.keys()[-1]] == {}:
                            #         data_dict[data_dict.keys()[-1]] = {word: {}}
                            #     else:
                            #         data_dict[data_dict.keys()[-1]][word] = {}
                            elif data_dict and num_there(word) and not alpha_there(word):
                                values = filter(lambda name: num_there(name), word.split())
                                dict1 = zip(date_obj, values)
                                for d1 in data_dict:
                                    for key in data_dict[d1]:
                                        if data_dict[d1][key] == {}:
                                            data_dict[d1][key] = dict1

                            elif data_dict and alpha_there(word):#and num_there(word) and len(word)>30 :
                                word = word.split(',')[0]
                                if data_dict[data_dict.keys()[-1]] == {}:
                                    data_dict[data_dict.keys()[-1]] = {word.replace('\xe2\x80\x99 ', '-'): {}}
                                else:
                                    data_dict[data_dict.keys()[-1]][word.replace('\xe2\x80\x99 ', '-')] = {}
                                # data_dict[data_dict.keys()[-1]] = {word.replace('\xe2\x80\x99 ', '-'): {}}


                        elif data_dict and len(word) > 100 and  ('                      ') in word :
                            # import pdb;pdb.set_trace()
                            values = re.split('  +', word)
                            if values[0].lower() in ['total current assets','total current liabilities']:
                                data_dict[mapping_dict[values[0].lower()]] = {}
                            elif (data_dict[data_dict.keys()[-1]].keys() and num_there(word)):
                                # import pdb;pdb.set_trace()
                            #     data_dict[data_dict.keys()[-1]][data_dict[data_dict.keys()[-1]].keys()[-1]] == {}
                                values = filter(lambda name: num_there(name), word.split()[-2:])
                                dict1 = zip(date_obj, values)
                                for d1 in data_dict:
                                    for key in data_dict[d1]:
                                        if data_dict[d1][key] == {}:
                                            data_dict[d1][key] = dict1
                            else:
                                new_key=values[0] if len(values[0])<60 else values[0].split(',')[0]

                                if '\xe2\x80\x93' in values[0]:
                                    new_key = values[0].replace(' \xe2\x80\x93 ','-')

                                if '\xe2\x80\x99' in values[0]:
                                    new_key = values[0].replace(' \xe2\x80\x99 ','-')

                                data_dict[data_dict.keys()[-1]][new_key] = \
                                    zip(date_obj, filter(lambda num: num_there(num), values[1:]))
                        elif data_dict and len(word) > 100 and  ('                       ') not in word :
                            word = word.split(',')[0]
                            data_dict[data_dict.keys()[-1]] = {word.replace('\xe2\x80\x99 ', '-'): {}}
            print (data_dict)
            return data_dict, qtr_exists



    except subprocess.CalledProcessError:
        data_dict = []
    # print data_dict
