from datetime import datetime, timedelta
import pdfkit
import os
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


def save_qtr(date_obj,link,qtr_path):
    q1 = date_obj.split()
    pdf_qtr = []
    for i in q1:
        try:
            try:
                if datetime.strptime(i, '%Y'):
                    q_1 = i
                    pdf_qtr.append(i)
            except:
                if datetime.strptime(i, '%B'):
                    pdf_qtr.append(i)
        except:
            pass
    pdf_name = '_'.join(pdf_qtr)
    date_1 = qtr_date()
    if [i for i in date_1 if q_1 in date_1[i]]:
        name = qtr_path + pdf_name + '.pdf'
        pdfkit.from_url(link, name)

def save_year(date_obj,link,year_path):
    y1 = date_obj.split()
    for i in y1:
        try:
            if datetime.strptime(i, '%Y'):
                y_1 = i
        except:
            pass

    date_1 = year_date()
    if [i for i in date_1 if int(y_1) == int(date_1[i])]:
        name = year_path + y_1 + '.pdf'
        pdfkit.from_url(link, name)