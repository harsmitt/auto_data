from datetime import datetime, timedelta
import pdfkit
import os
import errno
from collections import OrderedDict
DEFAULT_DATA_PATH='/home/administrator/DataAutomation/company_pdf/'

# from fun import year_date,qtr_date

def qtr_date():
    latest_q=[]
    qtr_dict = OrderedDict()
    date_time = datetime.now() - timedelta(days=45)
    current_year= date_time.year
    current_month = date_time.month
    qtr_year_list = [i for i in range(2014,current_year)]
    q_d =['march','june','september','december']
    for i in qtr_year_list:
        for q1 in q_d:
            key = 'q' + str(len(qtr_dict)+1)
            qtr_dict[key] = q1+' '+str(i)
    if current_month>3 and current_month<=6:
        latest_q = ['march']
    elif current_month>6 and current_month<=9:
        latest_q=['march','june']
    elif current_month>9 and current_month<=12:
        latest_q = ['march','june','september']
    for l_qtr in latest_q:
        key = 'q'+str(len(qtr_dict)+1)
        qtr_dict[key]= l_qtr+' '+str(current_year)
    return qtr_dict


def year_date(year_end):
    c_date = datetime.now()
    y_start =2011
    year_dict =OrderedDict()
    year_end_month = datetime.strptime(year_end, '%B').month
    year_pdf = year_end_month+int(3)
    for i in range(y_start,c_date.year):
        y_key= 'y'+str(len(year_dict) + 1)
        year_dict[y_key] = i
    if c_date.month > year_pdf:
        y_key = 'y' + str(len(year_dict) + 1)
        year_dict[y_key] = c_date.year
    return year_dict


def year_list():
    return range(11,19)


def save_qtr(date_obj,cname,ftype,link=None,file_type =None,file_name=None):
    if len(date_obj)>500:
        s2 = date_obj.split('\n\n')[1][:500]
        date_obj=s2.split('or')[1].split()
    q1 = date_obj.split()
    pdf_qtr = []
    for i in q1:
        try:
            try:
                if datetime.strptime(i.split('or')[0], '%Y'):
                    i=i.split('or')[0]
                    q_1 = i
                    pdf_qtr.append(i)
            except:
                if datetime.strptime(i, '%B'):
                    i=i.split('or')[0]
                    pdf_qtr.append(i)
        except:
            pass


    make_directory(cname,ftype)
    path = os.path.join(DEFAULT_DATA_PATH, cname,ftype)
    pdf_name = '_'.join(pdf_qtr)
    date_1 = qtr_date()
    if [i for i in date_1 if q_1 in date_1[i]]:
        name = path + '/'+pdf_name + '.pdf'
        if not file_type:
            pdfkit.from_url(link, name)
        else:
            os.rename(file_name,name)

import re

def get_digit(s,num=False):
    if num==True:
        digit = ("".join(re.findall("[0-9]+", s.lower().strip())))
    elif s in s in ['-','*','â','- -'] or not [i for i in s if ord(i)<128]:
        return s
    else:
        if s[0]=='-':
            digit = ("".join(re.findall("[0-9()*.-]+", s.lower().strip())))
        else:
            digit = ("".join(re.findall("[0-9()*.]+", s.lower().strip())))

    digit  = (digit.replace(',', '').replace('(', '-').replace(')', '').replace('$', '').replace('*','0'))
    if digit and '.' in digit:
        digit = float(digit)

    elif digit:
        digit = int(digit)
    return digit


def save_year(date_obj,cname,ftype,link,file_type=None,file_name=None):
    if len(date_obj)>500:
        s2 = date_obj.split('\n\n')[1][:500]
        date_obj=s2.split('or')[1].split()
    y1 = date_obj.split()
    for i in y1:
        try:
            obj=i.split('or')[0]
            obj=i.split('OR')
            if datetime.strptime(str(get_digit(obj[0])), '%Y'):
                y_1 = obj[0]
        except:
            pass

    make_directory(cname,ftype)
    path = os.path.join(DEFAULT_DATA_PATH, cname, ftype)
    date_1 = year_date("December")
    if [i for i in date_1 if int(y_1) == int(date_1[i])]:
        name = path +'/'+ y_1 + '.pdf'
        if not file_type:
            pdfkit.from_url(link, name)
        else:
            os.rename(file_name, name)



import urllib

def download_file(download_url,file_name,cname):
    import tempfile, subprocess
    import re
    # download_url = re.sub('.*http', 'http', download_url)
    try:
        response = urllib.urlopen(download_url)

        file = open(file_name, 'w')
        file.write(response.read())
        file.close()
        page=1
        file_object = open(file_name, 'rb')
        pdfData = file_object.read()
        tf = tempfile.NamedTemporaryFile()
        tf.write(pdfData)
        tf.seek(0)
        outputTf = tempfile.NamedTemporaryFile()
        args = ['pdftotext', '-f', str(page), '-l', str(page), '-layout', '-q', file_name, outputTf.name]
        txt = subprocess.check_output(args, universal_newlines=True)
        data = outputTf.readlines()
        for i in data :
            i=i.replace('\xc2\xa0', ' ')
            if 'For the quarterly period ended' in i:
                save_qtr(i,cname,'Quarter',file_type='pdf',file_name=file_name)
                break;

            elif "For the fiscal year ended" in i:
                save_year(i,cname,'Year',file_type='pdf', file_name=file_name)
                break;

    except:
        pass
    print("Completed")


def make_directory(company_name, file_type):
    # Making the directory to save comapny filings
    path = os.path.join(DEFAULT_DATA_PATH, company_name, file_type)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


def get_url_list(url=None,link=None):
    u_list=[]
    if url and link:
        if url.endswith('/') and link.startswith('/'):
            u_list.append(url[:-1] + link +'/?DocType=Quarterly')
            u_list.append(url[:-1] + link + '/?DocType=Annual')
        elif url.endswith('/') and not link.startswith('/') or not url.endswith('/') and link.startswith('/')  :
            u_list.append(url + link +'/?DocType=Quarterly')
            u_list.append(url + link + '/?DocType=Annual')
        else:
            u_list.append(url +'/'+ link +'/?DocType=Quarterly')
            u_list.append(url + '/' + link + '/?DocType=Annual')
    else:
        if url.endswith('/') :
            u_list.append(url[:-1] +'/?DocType=Quarterly')
            u_list.append(url[:-1] + '/?DocType=Annual')
        else:
            u_list.append(url + '/?DocType=Quarterly')
            u_list.append(url + '/?DocType=Annual')


    return u_list

