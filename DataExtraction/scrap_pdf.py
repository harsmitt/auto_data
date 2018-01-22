import re
import datetime
import tempfile,subprocess
from .common_functions import *
from datetime import datetime
from collections import OrderedDict
from .models import *
# from django.db.models import QTotal Long-Term Liabilities

mapping_dict ={'assets':'current assets','LIABILITIES AND'.lower():'current liabilities','total current assets':'non current assets',
               'total current liabilities':'non current liabilities','long-term liabilities':'non current liabilities',
               'total assets':'current liabilities','total liabilities':'stockholders equity'}

main_keys_dict=['current assets','current liabilities','non current assets','non current liabilities','long term assets'
                ,"Stockholders' equity",'shareholders\xe2\x80\x99 equity','stockholders\xe2\x80\x99 equity']

spl_char=['\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x94']

total_comp = list(mapping_dict.keys()) + list(mapping_dict.values())

def get_date_obj(date_obj, str1, date_val,qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    get_month = [i for i in str1.split() if not num_there(i) and i.lower().strip() not in ['current assets','assets']]

    if len(get_month) ==3:
        try:
            if  list(filter(lambda x:  datetime.strptime(x, '%B') ,date_obj) ):
                get_month=get_month[1:]
        except:
            pass

    try:
        if len(get_month) in[2,0] :
            if not date_obj and not date_val==True and not get_year:
                date_obj=get_month
            else:
                month_year = list(zip(date_obj, get_year) if date_obj else zip(get_month,get_year))
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
    file_object = open(path, 'rb')
    pdfData = file_object.read()
    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)
    outputTf = tempfile.NamedTemporaryFile()
    args = ['pdftotext', '-f', str(page), '-l', str(page), '-layout', '-q', path, outputTf.name]
    try:
        txt = subprocess.check_output(args, universal_newlines=True)
        data = outputTf.readlines()
        if page == 1:
            str1 = 'Name of Registrant as Specified in its Charter'
            company_name = [data[key - 1].strip() for key, i in enumerate(data) if (str1).lower() in i.decode('utf8').lower()]
            return company_name
        else:
            r1 = re.compile('[ (A-Za-z0-9. - )]consolidated balance (sheets|sheet)*[ (A-Za-z0-9. - )$]', re.IGNORECASE)
            if filter(r1.search, data):
                for line_no ,i in enumerate(data):
                    i=i.decode('utf8')

                    if i and num_there(i) and not date_val:
                        date_obj,qtr_exists,date_val = get_date_obj(date_obj,i,date_val,qtr_exists) if file_type=='qtr'\
                            else get_year(date_obj, i, date_val,qtr_exists)
                        if qtr_exists==False and len(date_obj)>1:
                            qtr_exists=False
                            break;

                    elif date_val == True:
                        word = i.strip().replace(':', '')
                        print (word)
                        if len(data)-line_no < 10 and not data_dict:
                            break;

                        if (('total' and 'equity') in word.lower()) :
                            if (len(data)!=line_no+1) :
                                if ('total' in data[line_no+1].decode('utf-8').lower()):
                                    break;

                        if len(re.split('  +',word))<2 and len(word) < 110 :
                            pass_list = ['LIABILITIES AND',  ]

                            if any(i.lower() in word.lower() for i in pass_list)or (word.lower().strip() in ['other assets','equity'] and not num_there(word)):
                                pass;

                            elif [get_aplha(word) for i in main_keys_dict if get_aplha(i)== get_aplha(word)]:

                                if word.lower() in data_dict:pass
                                else:
                                    new_key = get_aplha(word)
                                    data_dict[new_key] = {}

                            elif data_dict and  len(data)>line_no+1 and  (':' in data[line_no].decode('utf-8') + ' ' +data[line_no + 1].decode('utf-8')) and data_dict[
                                list(data_dict.keys())[-1]] in [[], {}]:
                                    pass

                            elif word.lower() in list(mapping_dict.keys()):
                                if mapping_dict[get_aplha(word)] not in data_dict:
                                    data_dict[mapping_dict[get_aplha(word)]]={}

                            elif data_dict and num_there(word) and not alpha_there(word):
                                values = list(filter(lambda name: num_there(name), word.split()))
                                val = map(lambda x: str(get_digit(x)), values)
                                dict1 = list(zip(date_obj, val))
                                for d1 in data_dict:
                                    for key in data_dict[d1]:
                                        if data_dict[d1][key] in [[],{}] and key not in ['non current assets','non current liabilities']:
                                            data_dict[d1][key] = dict1

                            elif data_dict and alpha_there(word) and word and  word.split()[0].istitle() and check_datetime(word.split()[0]) ==False:
                                if any(data_dict[d1][key] in [[],{}] for d1 in data_dict for key in data_dict[d1]):
                                    pass
                                else:
                                    if data_dict[list(data_dict.keys())[-1]] in [[],{}]:
                                        word = word.split(',')[0]
                                        new_key = get_aplha(word)
                                        data_dict[list(data_dict.keys())[-1]] = {new_key: {}}
                                    else:
                                        data_dict[list(data_dict.keys())[-1]][get_aplha(word)] = {}

                        elif data_dict and len(word) > 100:
                            values = re.split('  +', word)
                            pattern = re.compile('[(|),-]')
                            key_name= get_aplha(values[0])
                            if pattern.split(key_name)[0].strip() in ['total assets','total current assets','total current liabilities','total liabilities']:
                                new_key = key_name if len(key_name) < 60 else key_name.split(',')[0]
                                new_values = list(filter(lambda num: num_there(num), values[1:]))
                                val = map(lambda x: str(get_digit(x)), new_values)
                                data_dict[list(data_dict.keys())[-1]][new_key] = list(zip(date_obj, val))
                                data_dict[mapping_dict[pattern.split(key_name)[0].strip()]] = {}

                            elif key_name in ['assets','liabilities']:
                                if  key_name =='assets':
                                    import pdb;pdb.set_trace()
                                    data_dict['current liabilities']={}
                                else:
                                    data_dict['stockholders equity']={}
                            elif list(filter(lambda x: True if str('total ' + str(x)) == key_name else False, total_comp)):
                                pass
                            elif any(data_dict[d1][key]in [{},[]] for d1 in data_dict for key in data_dict[d1]):
                                values = list(filter(lambda name: num_there(name), re.split('  +',word)[1:]))
                                if not values:
                                    no_val= ["xxx" for i in spl_char if i in re.split('  +',word)[1:]]
                                    if no_val:
                                        for d1 in data_dict:
                                            for key in data_dict[d1]:
                                                if data_dict[d1][key] in [[],{}]:
                                                    del data_dict[d1][key]
                                                break;
                                else:
                                        # for d1 in data_dict for key in data_dict[d1] if data_dict[d1][key] == {}]
                                    val = map(lambda x: str(get_digit(x)), values)
                                    dict1 = list(zip(date_obj, val))
                                    for d1 in data_dict:
                                        for key in data_dict[d1]:
                                            if data_dict[d1][key] in [[],{}]:
                                                data_dict[d1][key] = dict1
                            else:
                                new_key=key_name if len(key_name)<60 else key_name.split(',')[0]

                                # new_values = list(map(lambda x: x.replace(x,'-') if x in spl_char else x, values[1:]))
                                new_values = list(filter(lambda num: num_there(num), values[1:]))
                                val = map(lambda x: str(get_digit(x)),new_values)
                                data_dict[list(data_dict.keys())[-1]][new_key] = \
                                    list(zip(date_obj,val))
                                # break;
                        elif data_dict and len(word) > 100 and  ('                       ') not in word :

                            # if list(filter(lambda x: True if str('total ' + str(x)) == word.lower() else False, total_comp)):
                            #     pass
                            # else:
                            word = word.split(',')[0]
                            new_key = [word.replace(i, '-') for i in spl_char if i in word ]
                            new_key = "".join(new_key[0].split()) if new_key else word

                            data_dict[list(data_dict.keys())[-1]] = {new_key: {}}
            print (data_dict)
            return data_dict, qtr_exists



    except subprocess.CalledProcessError:
        data_dict = []
    # print data_dict
