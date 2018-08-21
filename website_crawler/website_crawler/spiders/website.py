import re
# Third parties
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class WebsiteItem(scrapy.Item):
    url = scrapy.Field()

url_list=['http://www.apple.com']

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
                if 'investor' in link:
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
                    yield scrapy.Request(url=link, callback=self.scrap_pdf,
                                             meta={'url': link,'old_url':response.meta['url']}, dont_filter=True)
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
                    import pdfkit
                    pdfkit.from_url(link, name)



# crawler = WebsiteSpider()
process = CrawlerProcess()
process.crawl(WebsiteSpider)
process.start()