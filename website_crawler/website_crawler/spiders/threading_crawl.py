from sec_files import WebsiteSpider

import threading, queue

from twisted.internet import reactor

from scrapy.xlib.pydispatch import dispatcher
# from scrapy.core.manager import scrapymanager
# from scrapy.core.engine import scrapyengine
# from scrapy.core import signals
#
#
# class CrawlerThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.running = False
#
#     def run(self):
#         self.running = True
#         scrapymanager.configure(control_reactor=False)
#         scrapymanager.start()
#         reactor.run(installSignalHandlers=False)
#
#     def crawl(self, *args):
#         if not self.running:
#             raise RuntimeError("CrawlerThread not running")
#         self._call_and_block_until_signal(signals.spider_closed, \
#                                           scrapymanager.crawl, *args)
#
#     def stop(self):
#         reactor.callFromThread(scrapyengine.stop)
#
#     def _call_and_block_until_signal(self, signal, f, *a, **kw):
#         q = Queue.Queue()
#
#         def unblock():
#             q.put(None)
#
#         dispatcher.connect(unblock, signal=signal)
#         reactor.callFromThread(f, *a, **kw)
#         q.get()


# Usage example below:

import os

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'website_crawler.settings')

from scrapy.xlib.pydispatch import dispatcher
# from scrapy.core import signals
from scrapy.conf import settings
from scrapy.crawler import CrawlerThread

settings.overrides['LOG_ENABLED'] = False  # avoid log noise


def item_passed(item):
    print ("Just scraped item:"+ item)


dispatcher.connect(item_passed, signal=signals.item_passed)
crawler = CrawlerThread()
print ("Starting crawler thread...")
crawler.start()
print ("Crawling somedomain.com....")
crawler.crawl(WebsiteSpider,"AAPL","mahima test","December") # blocking call
print ("Crawling anotherdomain.com...")
crawler.crawl(WebsiteSpider,"kona","mahima test2","December")  # blocking call
print ("Stopping crawler thread...")
crawler.stop()