import scrapy
from selenium import webdriver
from twisted.internet import reactor,defer
import pdfkit
import time
import re
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider


class GetUrlSpider(scrapy.Spider):
    name = "GetUrl"
    allowed_domains = ['google.com']
    start_urls = ['http://www.google.com']
    lists = []

    def __init__(self,company_name=''):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.company_name = company_name
        # navigate to the application home page
        self.driver.get("http://www.google.com/")

    def parse(self, response):
        self.driver.get(response.url)
        self.search_field = self.driver.find_element_by_name("q")
        # enter search keyword and submit
        self.search_field.send_keys(self.company_name)
        self.search_field.submit()
        global lists
        time.sleep(2)
        # get the list of elements which are displayed after the search
        # currently on result page usingfind_elements_by_class_namemethod
        words =[i for i in self.company_name.split(' ') if len(i)>2]
        for word in words:
            r1 = 'https?://[A-Za-z0-9.-](?i)*%s[A-Za-z0-9.-]*\.(com|in)/*$' % str(word)
            url_s = self.driver.find_elements_by_tag_name('a')
            for i in url_s:
                if i.get_attribute('href') != None and re.match(r1, i.get_attribute('href')):
                    if i.get_attribute('href') not in GetUrlSpider.lists:
                        GetUrlSpider.lists.append(i.get_attribute('href'))

        print (GetUrlSpider.lists)
        self.driver.close()


class WebsiteItem(scrapy.Item):
    url = scrapy.Field()

url_list=GetUrlSpider.lists

class WebsiteSpider(CrawlSpider):
    name = 'website'
    keyword = 'investor'
    allowed_domains = ['website.com']
    start_urls = url_list

    def start_requests(self): # Gets called automatically on running script
        urls = url_list
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

            # callback function for start_requests function. Gets passed response of url.

    def parse_url(self, response):
        try:
            for counter, link in enumerate(
                    response.css('a::attr(href)').extract()):  # Get all the <a herf> value from response page.
                if 'investor' in link or 'investors' in link:
                    if 'http' not in link and'https' not in link :
                        link = "http://www.apple.com/" + link
                    # dont_filter=True gets passed duplicate urls to crawl.
                    # meta to share data between functions.
                    yield scrapy.Request(url=link, callback=self.parse_item,
                                         meta={'url': link}, dont_filter=True)
        except:
            print("unable to extract the %s keyword in url:%s" % (WebsiteSpider.keyword, link))

    def parse_item(self, response):
        try:
            for counter,link in enumerate(response.css('a::attr(href)').extract()):
                if 'sec.' in link:
                    if 'http' not in link and 'https' not in link:
                        link = response.meta['url'] + '/'+ link +'/?DocType=Quarterly'
                        type_pdf = 'quarterly'
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                             meta={'url': link,'old_url':response.meta['url'],'type_pdf':type_pdf}, dont_filter=True)
        except:
            print ("unable to extract the %s keyword in url:%s" % (WebsiteSpider.keyword, link))

    def scrap_pdf(self,response):
        total_urls= response.css('a::attr(href)').extract()
        url_list = [i for i in total_urls  if ('secfiling.' in i) ]
        ac_url = set(url_list)
        for counter, link in enumerate(ac_url):
            if 'secfiling.' in link:
                if 'http' not in link and 'https' not in link:
                    link = response.meta['old_url'] + '/' + link
                    name='first_'+str(counter)+'.pdf'
                    pdfkit.from_url(link, name)

runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    company_name = raw_input('Enter the company name')
    print (company_name)
    # spider= GetUrlSpider(company_name=company_name)
    yield runner.crawl(GetUrlSpider,company_name)
    yield runner.crawl(WebsiteSpider)
    reactor.stop()

crawl()
reactor.run()