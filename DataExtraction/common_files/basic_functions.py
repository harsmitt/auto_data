import os
import errno
import re
from datetime import datetime

def num_there(s):
    if s in ['-','*','—','- -']:
        return True

    return any(i.isdigit() for i in s)

def alpha_there(s):
    return any(i.isalpha() for i in s)

def get_digit(s):
    if s in ['-','- -']:
        return s
    else:
        digit = ("".join(re.findall("[0-9()*]+", s.lower().strip())))
        return int(digit.replace(',', '').replace('(', '-').replace(')', '').replace('$', '').replace('*','0'))

def get_alpha(s,pnl=False):
    str1 = s.split('(')[0]

    ##need exact key name as mention in pdf

    if pnl:
        str1 =s

    return (" ".join(re.findall("[a-zA-Z,]+", str1.lower().strip())))



def get_number(s):
    digit = ("".join(re.findall("[0-9]+", s.lower().strip())))

    return int(digit) if digit else 0

def check_datetime(obj):
    try:
       if  type(datetime.strptime(obj, '%B')) == datetime :
           return True
    except:
        try:
            if type(datetime.strptime(obj, '%Y')) == datetime:
                return True
        except :
            return False

from datetime import datetime, timedelta
def qtr_date(year_end):
    date_time = datetime.now()-timedelta(days=30)
    month = date_time.month
    year = date_time.year
    year1 = year - 1
    if month<=3:
        qtr5 = 'december ' + str(year1)
        qtr4 ='september ' + str(year1)
        qtr3 = 'june ' + str(year1)
        qtr2 = 'march '+ str(year1)
        qtr1 ='december '+ str(year1-1)
    elif month>3 and month<=6:
        qtr5 = 'march '+ str(year)
        qtr4 = 'december ' + str(year1)
        qtr3 = 'september '+ str(year1)
        qtr2 = 'june ' + str(year1)
        qtr1 = 'march '+ str(year1)
    elif month>6 and month<=9:
        qtr5 = 'june ' +  str(year)
        qtr4 = 'march '+ str(year)
        qtr3 = 'december ' + str(year1)
        qtr2 = 'september '+ str(year1)
        qtr1 = 'june ' +  str(year1)
    elif month >9 and month<=12:
        qtr5 = 'september ' + str(year)
        qtr4 = 'june ' + str(year)
        qtr3 = 'march ' + str(year)
        qtr2 = 'december ' + str(year1)
        qtr1 = 'september ' + str(year1)
    qtr_dict={'q1':qtr1,'q2':qtr2,'q3':qtr3,'q4':qtr4,'lrq':qtr5}
    return qtr_dict

def year_date(year_end):
    c_date= datetime.now()
    if year_end == 'December':
        c_year = c_date.year
        c_month = c_date.month
        year = c_year if c_month >3 else c_year-1
    elif year_end == 'March':
        c_year = c_date.year
        c_month = c_date.month
        year = c_year if c_month > 6 else c_year - 1
    elif year_end == 'June':
        c_year = c_date.year
        c_month = c_date.month
        year = c_year if c_month > 9 else c_year - 1
    elif year_end == 'September':
        c_year = c_date.year
        c_month = c_date.month
        year = c_year if c_month > 11 else c_year - 1
    year_dict ={'y1':str(year-4),'y2':str(year-3),'y3':str(year-2),'y4':str(year-1)}
    return year_dict

#get next and last month from a current month
def next_last_month(current_month):
    if datetime.strptime(current_month, '%B %Y').month!=1:
        last_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(month=datetime.strptime(current_month, '%B %Y').month-1)).strftime('%B %Y')
    else:
        year=datetime.strptime(current_month, '%B %Y').year - 1
        last_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=12,year=year)).strftime('%B %Y')
    if datetime.strptime(current_month, '%B %Y').month != 12:
        next_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(month=datetime.strptime(current_month, '%B %Y').month + 1)).strftime('%B %Y')
    else:
        year = datetime.strptime(current_month, '%B %Y').year + 1
        next_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=1,year=year)).strftime('%B %Y')
    return last_month,next_month