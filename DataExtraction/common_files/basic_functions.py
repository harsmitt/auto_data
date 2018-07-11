#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: ascii -*-
import os
import errno
import re
from datetime import datetime

def num_there(s):
    if not [i for i in s if ord(i)<128] or s in ['-','*','—','- -']:
        return True
    return any(i.isdigit() for i in s)

def alpha_there(s):
    return any(i.isalpha() for i in s)


def get_alpha(s,key=False,pnl=False,remove_space=False,remove_s = False):
    str1 = s.split('(')[0]
    if pnl:
        str1 =s

    if not key:
        alpha_obj = (" ".join(re.findall("[a-zA-Z,]+", str1.lower().strip())))
    else:
        alpha_obj = (" ".join(re.findall("[a-zA-Z]+", str1.lower().strip())[:4]))
        # alpha_obj = (" ".join(re.findall("[a-zA-Z,]+", str1.lower().strip()))).split(',')[0]

    if not remove_space and not remove_s:
        return alpha_obj
    elif remove_s and not remove_space:
        remove_s_obj = ' '.join([' '.join([re.sub('s$', '', word)]) for word in alpha_obj.lower().split()])
        return remove_s_obj
    elif not remove_s and remove_space:
        remove_s_obj = ''.join([' '.join([re.sub('\s+', '', word)]) for word in alpha_obj.lower().split()])
        return remove_s_obj
    elif remove_s and remove_space:
        remove_s_obj = ''.join([' '.join([re.sub('\s+|s$', '', word)]) for word in alpha_obj.lower().split()])
        return remove_s_obj
    else:
        return alpha_obj


def extract_s(line):
    remove_s_obj =  ' '.join([' '.join([re.sub('s$', '', word)]) for word in line.lower().split()])

    return  remove_s_obj

def get_digit(s,num=False,ui_num=False):
    try:
        if ui_num==True:
            digit = ("".join(re.findall("[0-9-]+.", s.lower().strip())))
        elif num==True:
            digit = ("".join(re.findall("[0-9]+", s.lower().strip())))
        elif s in s in ['-','*','—','- -','?'] or not [i for i in s if ord(i)<128]:
            return s
        else:
            if s[0]=='-':
                digit = ("".join(re.findall("[0-9()*.-]+", s.lower().strip())))
            else:
                digit = ("".join(re.findall("[0-9()*.]+", s.lower().strip())))

        digit  = (digit.replace(',', '').replace('(', '-').replace(')', '').replace('$', '').replace('*','0'))
        if digit and '.' in digit:
            try:digit = float(digit)
            except :digit =0
        elif digit:
            try:digit = int(digit)
            except:digit=0
        return digit
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return 0

def check_datetime(obj,pdf_type = None):
    if not pdf_type:
        try:
           if  type(datetime.strptime(obj, '%B')) == datetime or type(datetime.strptime(obj, '%m')) == datetime :
               return True
        except:
            try:
                if type(datetime.strptime(obj, '%Y')) == datetime:
                    return True
            except :
                return False
    else:
        try:
            if type(datetime.strptime(obj, '%Y')) == datetime:
                return True
        except:
            return False

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

from datetime import datetime, timedelta
from collections import OrderedDict

def qtr_date_pnl():
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
