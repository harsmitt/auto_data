import scrapy
from selenium import webdriver
from twisted.internet import reactor,defer
import logging
import pdfkit
import time
import re
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider

class Crawler2(scrapy.Item):
    url = scrapy.Field()

class CrawlerSpider(CrawlSpider):
    name = 'Crawler'
    keyword = 'investor'
    allowed_domains = ['website.com']

    def __init__(self,url=''):
        self.url_list = url

    def start_requests(self):  # Gets called automatically on running script
        urls = self.url_list
        logging.info(">>>>>>>>>>>>>>Crawling starting<<<<<<<<<<<<<<<<<<<<")
        # for url in urls:
        yield scrapy.Request(url=urls, callback=self.parse_url)

    def parse_url(self, response):
        try:
            for counter, link in enumerate(
                    response.css('a::attr(href)').extract()):  # Get all the <a herf> value from response page.
                if 'investor' in link or 'investors' in link or 'javascript' in link :
                    if 'http' not in link and'https' not in link :
                        link = self.url_list + link
                    # dont_filter=True gets passed duplicate urls to crawl.
                    # meta to share data between functions.
                    if 'javascript' in link:
                        pass
                    yield scrapy.Request(url=link, callback=self.parse_item,
                                         meta={'url': self.url_list}, dont_filter=True)
                elif 'annual' in link or 'financials' in link:
                    if 'http' not in link and'https' not in link :
                        url_1= re.search('(ftp|http)://.*\.(com)', self.url_list)
                        link = url_1.group(0) +'/'+ link
                    # dont_filter=True gets passed duplicate urls to crawl.
                    # meta to share data between functions.
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                         meta={'url': self.url_list}, dont_filter=True)
        except:
            print("unable to extract the %s keyword in url:%s" % (CrawlerSpider.keyword, link))

    def parse_item(self, response):
        try:
            for counter,link in enumerate(response.css('a::attr(href)').extract()):
                if 'annual-reports' in link :
                    if 'http' not in link and 'https' not in link:
                        link = response.meta['url'] + link.split('..')[-1]
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                         meta={'url': link, 'old_url': response.meta['url']},
                                         dont_filter=True)

                elif 'financial-results' in link:
                    # if 'http' not in link and 'https' not in link:
                    link = response.meta['url']+  link.split('..')[-1]
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                             meta={'url': link,'old_url':response.meta['url']}, dont_filter=True)
        except:
            print ("unable to extract the %s keyword in url:%s" % (CrawlerSpider.keyword, link))


    def scrap_pdf(self,response):
        # total_urls= response.css('a::attr(href)').extract()
        # url_list = [i for i in total_urls  if ('secfiling.' in i) ]
        pdf_urls = [i for i in response.css('a::attr(href)').extract() if '.pdf' in i]
        ac_url = set(pdf_urls)

        for url in ac_url:
            if 'http' not in url and 'https' not in url:

                url_1 = re.search('(ftp|http)://.*\.(com)', response.meta['url'])
                url = url_1.group(0) + '/' + url if url[0]!='/' else url_1.group(0) + url

            import urllib
            webFile = urllib.urlopen(url)
            pdfFile = open(url.split('/')[-1], 'w')
            pdfFile.write(webFile.read())
            webFile.close()
            pdfFile.close()


runner = CrawlerRunner()



@defer.inlineCallbacks
def crawl():
    url = raw_input('Enter the company url')
    print (url)
    # spider= GetUrlSpider(company_name=company_name)
    # yield runner.crawl(GetUrlSpider,company_name)
    yield runner.crawl(CrawlerSpider,url=url)
    reactor.stop()

crawl()
reactor.run()