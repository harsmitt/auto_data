import re
import datetime
import tempfile,subprocess
from .common_functions import *
from datetime import datetime
from collections import OrderedDict
import itertools
from .mapping_data import mapping_dict

from .models import *
# from django.db.models import QTotal Long-Term Liabilities

# mapping_dict ={'assets':'current assets','LIABILITIES AND'.lower():'current liabilities','total current assets':'non current assets',
#                'total current liabilities':'non current liabilities','long-term liabilities':'non current liabilities',
#                'total assets':'current liabilities','total liabilities':'stockholders equity'}
#
# main_keys_dict=['current assets','current liabilities','non current assets','non current liabilities',
#                 'long term assets','shareholders equity','stockholders equity']

spl_char=['\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x94']

# total_comp = list(mapping_dict.keys()) + list(mapping_dict.values())

def get_date_obj(date_obj, str1, date_val,qtr_exists):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    get_month = [i for i in str1.split() if not num_there(i) and i.lower().strip() not in ['current assets','assets']]

    if len(get_month) == 3:
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
            if list(filter(r1.search, data)):
                for line_no ,i in enumerate(data):
                    i=i.decode('utf8')
                    if i and num_there(i) and not date_val:
                        date_obj,qtr_exists,date_val = get_date_obj(date_obj, i, date_val,qtr_exists) if file_type=='qtr'\
                            else get_year(date_obj, i, date_val,qtr_exists)
                        if qtr_exists==False and len(date_obj)>1:
                            qtr_exists=False
                            break;
                    elif date_val == True:
                        word = i.lower().strip().replace(':', '')
                        print (word)

                        #sometime after total equity there are some other componants those are not useful
                        if (len(data)-line_no < 10 and not data_dict) or (('total' and 'equity') in word) and (len(data)!=line_no+1) :
                            break;

                        #if word has only key not values like "Assets" or "cash and cash" without numbers
                        if len(re.split('    +',word))<2:
                            pass_list = ['LIABILITIES AND',  ]

                            #sometime liability section has two keys like "LIABILITIES AND SHAREHOLDERS’ EQUITY:"
                            if any(i.lower() in word for i in pass_list)or (word in ['other assets','equity'] and not num_there(word)):
                                pass;

                            #if key is main key
                            elif any(k for k, v in mapping_dict.items() if get_aplha(word) in k):
                                if get_aplha(word) in data_dict:pass
                                else: data_dict[next(v for k, v in mapping_dict.items() if get_aplha(word) in k)] = {}

                            #correction in loop if data_dict.keys[-1] is my main key then this loop should be run
                            elif data_dict and len(data)>line_no+1 and (':' in data[line_no].decode('utf-8') + ' ' +data[line_no + 1].decode('utf-8')) and data_dict[
                                list(data_dict.keys())[-1]] in [[], {}]:
                                    pass

                            #if the struncture is in this format e.g(if first line contain key and second line
                            #contain key's values
                            elif data_dict and num_there(word) and not alpha_there(word):
                                values = list(filter(lambda name: num_there(name), word.split()))
                                val = list(map(lambda x: str(get_digit(x)), values))
                                dict1 = list(zip(date_obj, val))
                                for d1 in data_dict:
                                    for key in data_dict[d1]:
                                        if data_dict[d1][key] in [[],{}] and key not in list(itertools.chain(*mapping_dict.keys())):
                                            data_dict[d1][key] = dict1

                            #this loop will run when line conatins only key
                            elif data_dict and alpha_there(word) and word and word.split()[0].istitle() and check_datetime(word.split()[0]) ==False:
                                if any(data_dict[d1][key] in [[],{}] for d1 in data_dict for key in data_dict[d1]):
                                    pass
                                else:
                                    new_key = get_aplha(word.split(',')[0])
                                    if data_dict[list(data_dict.keys())[-1]] in [[],{}]:
                                        data_dict[list(data_dict.keys())[-1]] = {new_key: {}}
                                    else:
                                        data_dict[list(data_dict.keys())[-1]][new_key] = {}

                        #if line has key and value both
                        elif data_dict and len(re.split('  +', word))>2:
                            values = re.split('  +', word)

                            pattern = re.compile('[(|),-]')

                            key_name= get_aplha(values[0].trop())

                            #this loop executes when 'total' exist in key then we add a new ley in data dict
                            # mentioned in mapping dict for that `total ` key
                            if pattern.split(key_name)[0] in [i for i in list(itertools.chain(*mapping_dict.keys())) if 'total' in i]:
                               data_dict[next(v for k, v in mapping_dict.items() if pattern.split(key_name)[0] in k)] = {}

                            #exceptional case when total in one line and assests in another line
                            #at that time we need this condition
                            elif key_name in ['assets','liabilities']:
                                if  key_name =='assets': data_dict['current liabilities']={}
                                else: data_dict['stockholders equity']={}

                            #if blank key exist in data dict and no values in word then if part will be executed
                            # if key exists and values in word then else part will be executed
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
                                    val = map(lambda x: str(get_digit(x)), values)
                                    dict1 = list(zip(date_obj, val))
                                    for d1 in data_dict:
                                        for key in data_dict[d1]:
                                            if data_dict[d1][key] in [[],{}]:
                                                data_dict[d1][key] = dict1

                            #if mentioed conditions not satisfy then
                            #we assume word has simply two values along with the key and

                            #  we zip those values with date and add new
                            #component in dict

                            else:
                                new_key= key_name.split(',')[0]
                                new_values = list(filter(lambda num: num_there(num), values[1:]))
                                val = map(lambda x: str(get_digit(x)),new_values)
                                data_dict[list(data_dict.keys())[-1]][new_key] = \
                                    list(zip(date_obj,val))
                                # break;

                        #if key is more than 100
                        # elif data_dict and len(word) > 100 and len(re.split('  +'))<2 :
                        #
                        #     if list(filter(lambda x: True if str('total ' + str(x)) == word.lower() else False, total_comp)):
                        #         pass
                        #     else:
                        #         word = word.split(',')[0]
                        #         new_key = [word.replace(i, '-') for i in spl_char if i in word ]
                        #         new_key = "".join(new_key[0].split()) if new_key else word
                        #
                        #     data_dict[list(data_dict.keys())[-1]] = {new_key: {}}

            print (data_dict)
            return data_dict, qtr_exists



    except subprocess.CalledProcessError:
        data_dict = []
    # print data_dict
