from datetime import datetime, timedelta
import pdfkit
import os
import errno

DEFAULT_DATA_PATH='/home/administrator/DataAutomation/company_pdf/'

# from fun import year_date,qtr_date

def qtr_date():
    # import pdb;pdb.set_trace()
    date_time = datetime.now()-timedelta(days=45)
    month = date_time.month
    year = date_time.year
    if month<=3:
        year=year-1
        qtr1 = 'December ' + str(year)
        qtr2 ='September ' + str(year)
        qtr3 = 'June ' + str(year)
        qtr4 = 'March '+ str(year)
        qtr5 ='December '+ str(year-1)
    elif month>3 and month<=6:
        year1 = year - 1
        qtr1 = 'March '+ str(year)
        qtr2 = 'December ' + str(year1)
        qtr3 = 'September '+ str(year1)
        qtr4 = 'June ' + str(year1)
        qtr5 = 'March '+ str(year1)
    elif month>6 and month<9:
        year1 = year - 1
        qtr1 = 'June ' +  str(year)
        qtr2 = 'March '+ str(year)
        qtr3 = 'December ' + str(year1)
        qtr4 = 'September '+ str(year1)
        qtr5 = 'June ' +  str(year1)
    qtr_dict={'q1':qtr1,'q2':qtr2,'q3':qtr3,'q4':qtr4,'lrq':qtr5}
    return qtr_dict

def year_date():
    year = datetime.now().year
    year_dict ={'y1':year-4,'y2':year-3,'y3':year-2,'y4':year-1}
    return year_dict

def year_list():
    return range(13,18)


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

    # import pdb;
    # pdb.set_trace()
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

def save_year(date_obj,cname,ftype,link,file_type=None,file_name=None):
    if len(date_obj)>500:
        s2 = date_obj.split('\n\n')[1][:500]
        date_obj=s2.split('or')[1].split()
    y1 = date_obj.split()
    for i in y1:
        try:
            obj=i.split('or')[0]
            obj=i.split('OR')
            if datetime.strptime(obj[0], '%Y'):
                y_1 = obj[0]
        except:
            pass

    make_directory(cname,ftype)
    path = os.path.join(DEFAULT_DATA_PATH, cname, ftype)
    date_1 = year_date()
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
        print ("error aa gya")
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
    print ("make url")
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

