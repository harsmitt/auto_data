import requests
import os
from bs4 import BeautifulSoup
import sys
import datetime
from DataExtraction.common_files.basic_functions import *
# from logger_config import get_logger_config

c_url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={%s}&Find=Search&owner=exclude&action=getcompany'
url_list =[c_url+'&type=10-k',c_url+'&type=10-q']

def get_html_page(**kwargs):
    for url in url_list:
        url = url %(kwargs['c_tik'])
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        all_link = soup.find_all('a', href=True)
        count=0
        y1 = list(year_list())
        urls = [ link for link in all_link if 'Archives' in link['href']]
        for url_8k in urls:
            url_str=str(url_8k)
            count+=1
            year_digit = url_str.split('-')[-3] if len(url_str.split('-')) > 3 else ''
            if (int(year_digit) in y1) :
                if 'http' not in url_str and 'https' not in url_str:
                    new_url = 'https://www.sec.gov' + url_8k['href']
                save_pdf(url =new_url,c_name =kwargs['c_name'],c_tik=kwargs['c_tik'])

from.crawler_functions import *
def save_pdf(**kwargs):
    print (kwargs['url'])
    r = requests.get(kwargs['url'])
    data = r.text
    soup = BeautifulSoup(data)
    page_link = soup.find_all('a', href=True)
    pdf_url = [i for i in page_link if any( word in i['href'] and '.htm' in i['href'] for word in ['10-k','10k','10q','10-q'])]
    if pdf_url and 'http' not in pdf_url[0] and 'https' not in pdf_url[0]:
        url_k = 'https://www.sec.gov/'+ pdf_url[0]['href']
        r = requests.get(url_k)
        data = r.text
        soup = BeautifulSoup(data)
        x = soup.get_text()
        for item in x.split("\n\n\n"):
            if "the quarterly period ended" in item.lower():
                item = x.lower().split('the quarterly period ended')[1][:20]
                save_qtr(item, kwargs['c_name'], 'Quarter', url_k)
                break;
            elif "the fiscal year ended" in item.lower():
                item = x.lower().split('the fiscal year ended')[1][:20]
                save_year(item, kwargs['c_name'], 'Year', url_k)
                break;
