import scrapy
from twisted.internet import reactor,defer
import logging
import pdfkit
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider

DEFAULT_DATA_PATH = '/home/administrator/Automation/fin_dict/company_pdf/Apple/Quarter/'

class WebsiteItem(scrapy.Item):
    url = scrapy.Field()

class WebsiteSpider(CrawlSpider):
    name = 'website'
    keyword = 'investor'
    allowed_domains = ['website.com']

    def __init__(self,url=''):
        self.url_list = 'https://www.apple.com/in/'#url

    #This is initial process method.
    def start_requests(self): # Gets called automatically on running script
        urls = 'https://www.apple.com/in/'#self.url_list
        logging.info(">>>>>>>>>>>>>>Crawling starting<<<<<<<<<<<<<<<<<<<<")
        # for url in urls:
        yield scrapy.Request(url=urls, callback=self.parse_url)


    #callback function for start_requests function. Gets passed response of url.
    #This method will find the keyword investor in the url  and proceed it to find pdf's
    def parse_url(self, response):
        try:
            for counter, link in enumerate(
                    response.css('a::attr(href)').extract()):  # Get all the <a herf> value from response page.
                if 'investor' in link or 'investors' in link:
                    # import pdb;pdb.set_trace()
                    if 'http' not in link and'https' not in link :
                        link = self.url_list + link
                    # dont_filter=True gets passed duplicate urls to crawl.
                    # meta to share data between functions.
                    yield scrapy.Request(url=link, callback=self.parse_item,
                                         meta={'url': link}, dont_filter=True)
        except:
            print("unable to extract the %s keyword in url:%s" % (WebsiteSpider.keyword, link))

    #This method will find the quarterly pdf's from the url and pass the link one by one to the another method
    def parse_item(self, response):
        try:
            for counter,link in enumerate(response.css('a::attr(href)').extract()):
                if 'sec.' in link :
                    if 'http' not in link and 'https' not in link:
                        link = response.meta['url'] + '/'+ link +'/?DocType=Quarterly'
                        type_pdf = 'quarterly'
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                         meta={'url': link, 'old_url': response.meta['url'], 'type_pdf': type_pdf},
                                         dont_filter=True)

                elif 'investors' in link:
                    # if 'http' not in link and 'https' not in link:
                    link = response.meta['url']
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                             meta={'url': link,'old_url':response.meta['url']}, dont_filter=True)
        except:
            print ("unable to extract the %s keyword in url:%s" % (WebsiteSpider.keyword, link))

    #This method will get the html from the url and covert that html into pdf.
    def scrap_pdf(self,response):
        total_urls= response.css('a::attr(href)').extract()
        url_list = [i for i in total_urls  if ('secfiling.' in i) ]
        ac_url = set(url_list)
        for counter, link in enumerate(ac_url):
            if 'secfiling.' in link:
                if 'http' not in link and 'https' not in link:
                    link = response.meta['old_url'] + '/' + link
                    #'http://investor.apple.com/secfiling.cfm?filingID=1193125-16-439878&CIK=320193'
                    name=DEFAULT_DATA_PATH+'quarter_'+str(counter)+'.pdf'
                    pdfkit.from_url(link,name)

runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    url = raw_input(' Enter the company url')
    print (url)
    yield runner.crawl(WebsiteSpider,url=url)
    reactor.stop()

crawl()
reactor.run()

