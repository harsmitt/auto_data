import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from twisted.internet import reactor,defer
import time
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider
from .common_functions import *
from selenium import webdriver
from scrapy.crawler import CrawlerProcess
from scrapy.settings import default_settings

# qtr_path = '/home/administrator/Automation/fin_dict/company_pdf/identiv/Quarter/'
# year_path = '/home/administrator/Automation/fin_dict/company_pdf/identiv/Year/'

class WebsiteItem(scrapy.Item):
    url = scrapy.Field()

class WebsiteSpider(scrapy.Spider):
    name = 'website'
    keyword = 'investor'
    allowed_domains = ['website.com']

    def __init__(self,c_ticker='',company_name='',year_end =''):

        print ("Opening Sec Website")
        self.company_name = company_name
        self.c_ticker = c_ticker
        self.year_end = year_end
        self.url ='https://www.sec.gov'

    #This is initial process method.
    def start_requests(self):
        urls = 'https://www.sec.gov/'
        yield scrapy.Request(url=urls, callback=self.parse_url)

    def parse_url(self, response):
        c_url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={%s}&Find=Search&owner=exclude&action=getcompany' %(self.c_ticker)#self.driver.current_url

        url_list =[c_url+'&type=10-k',c_url+'&type=10-q']

        for i in url_list:
            yield scrapy.Request(url=i, callback=self.get_url,meta={'url': i,'old_url':self.url},dont_filter=True)


    def get_url(self,response):
        urls=[i for i in response.css('a::attr(href)').extract() if 'Archives' in i]
        count=0
        y1 = year_list()
        for url_8k in urls:
            count+=1
            year_digit = url_8k.split('-')[-3] if len(url_8k.split('-')) > 3 else ''
            if (int(year_digit) in y1) :
                if 'http' not in url_8k and 'https' not in url_8k:
                    url_8k = response.meta['old_url'] +url_8k
                yield scrapy.Request(url=url_8k, callback=self.get_html_url, meta={'url': url_8k}, dont_filter=True)



    def get_html_url(self,response):
        pdf_url = [i for i in response.css('a::attr(href)').extract() if ('10-k' in i or '10k' in i or '10-q' in i or '10q'in i) and ('.htm' in i)]
        if pdf_url and 'http' not in pdf_url[0] and 'https' not in pdf_url[0]:
            url_8k = self.url + pdf_url[0]
            from bs4 import BeautifulSoup
            import requests
            r = requests.get(url_8k)
            data = r.text
            soup = BeautifulSoup(data)
            x = soup.get_text()
            for item in x.split("\n\n\n"):
                if "the quarterly period ended" in item:
                    item=x.split('the quarterly period ended')[1][:20]
                    c_name = self.company_name
                    save_qtr(item, c_name, 'Quarter', url_8k)
                    break;
                elif "the fiscal year ended" in item:
                    item=x.split('the fiscal year ended')[1][:20]
                    c_name = self.company_name
                    save_year(item,c_name, 'Year', url_8k)
                    break;

