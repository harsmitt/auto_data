import PyPDF2

# from DataExtraction.common_functions import *
# from .old_save import *
from DataExtraction.common_files.all_regex import *
from DataExtraction.common_files.utils import *
from DataExtraction.table_content.get_table_content import table_content
from DataExtraction.common_files.extract_page_data import scrap_pdf_page

def all_pages(**kwargs):
    try:
        b_sheet = False
        pnl = False
        f_num= kwargs['f_num'] if 'f_num' in kwargs else 1
        l_num = kwargs['l_num'] if 'l_num' in kwargs else (kwargs['pdf'].getNumPages() + 1)
        notes_pages = kwargs['page_detail']['notes_section'] if 'notes_section' in kwargs['page_detail'] else 0

        for i in range(f_num,l_num):
            print (i)
            # data = get_page_content(seprator='@@', page=str(i), path=kwargs['path'], file=kwargs['file'])
            data,match = match_re_list(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re='bsheet')
            if match and not b_sheet:
                bs_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'],data=data, p_num=str(i),
                                         path=kwargs['path'], pdf_page='bsheet',override = kwargs['override'],
                                         file=kwargs['file'], c_name=kwargs['c_name'],
                                         pdf_type=kwargs['pdf_type'],notes=notes_pages)
                if bs_data[0]:
                    b_sheet = True


            elif not pnl:
                data,match = match_re_list(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re='pnl')
                if match:
                    pnl_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'], data=data, p_num=str(i),
                                             path=kwargs['path'], pdf_page='pnl',override = kwargs['override'],
                                             file=kwargs['file'], c_name=kwargs['c_name'],
                                             pdf_type=kwargs['pdf_type'],notes=notes_pages)
                    if pnl_data[1]:
                        pnl = True

            if b_sheet and pnl:
                return True

        return False

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return e

def update_financial_statements(**kwargs):
    try:
        bs_data = False
        page_detail = kwargs['page_detail']
        ##means i have exact page number from table content
        if 'statement' not in page_detail['statement_section']:
            if all(key in page_detail['statement_section'] for key in ['bsheet','pnl']):
                for statement_key, p_num in page_detail['statement_section'].items():
                    if statement_key in ['bsheet','pnl']:
                        notes_pages = page_detail['notes_section'] if 'notes_section' in page_detail else 0
                        bs_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'],p_num=p_num,
                                                 path=kwargs['path'],override = kwargs['override'],
                                                 pdf_page= statement_key,
                                                 file=kwargs['f_obj'], notes=notes_pages,
                                                 c_name=kwargs['company_name'], pdf_type=kwargs['pdf_type'])


                        if bs_data == (False,False):
                            break;

                if bs_data == (False,False):
                    res = all_pages(sector=kwargs['sector'], page_detail=page_detail, year_end=kwargs['year_end'],
                            pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],
                            path=kwargs['path'],pdf_type=kwargs['pdf_type'],override = kwargs['override'])


            else:
                res = all_pages(sector=kwargs['sector'], page_detail=page_detail, year_end=kwargs['year_end'],
                                pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],
                                path=kwargs['path'], pdf_type=kwargs['pdf_type'],override = kwargs['override'])
                return res

        else:
            f_num = int(page_detail['statement_section']['statement'].split('-')[0])
            # l_num = int(page_detail['statement_section']['statement'].split('-')[1])
            res = all_pages(override = kwargs['override'],sector =kwargs['sector'],page_detail =page_detail,year_end=kwargs['year_end'],
                            pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],
                            path=kwargs['path'],f_num =f_num,pdf_type=kwargs['pdf_type'])
            return res

        return bs_data

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return e


def get_data(**kwargs):
    try:
        page_detail={}
        file_object = open(kwargs['path'], "rb")
        pdf = PyPDF2.PdfFileReader(file_object)
        for num in range(2, (pdf.getNumPages()+1)):
            data = get_page_content(page=num,path=kwargs['path'],file=file_object)
            try:
                if num<=10 and not page_detail:
                    page_detail = table_content(data=data,page_detail=page_detail,path=kwargs['path'],file=file_object)
                    if page_detail  and 'statement_section' in page_detail:
                        res = update_financial_statements(sector =kwargs['sector'],year_end=kwargs['year_end'],pdf_type =kwargs['pdf_type'],path=kwargs['path'],
                                                    page_detail=page_detail,company_name=kwargs['company_name'],
                                                          f_obj=file_object,pdf=pdf,override = kwargs['override'])
                        break;

                elif not page_detail or 'statement_section' not in page_detail:
                    # need to loop every page in worst case.
                    res = all_pages(override = kwargs['override'],sector =kwargs['sector'],page_detail=page_detail,
                                    year_end=kwargs['year_end'],pdf=pdf,file=file_object,
                                    c_name=kwargs['company_name'],path=kwargs['path'],
                                    pdf_type =kwargs['pdf_type'])
                    break;

            except Exception as e:
                import traceback
                print (traceback.format_exc())
                return e
        return res

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return e



def LoopPdfDir(**kwargs):
    new_path = '/home/mahima/Downloads/Automation Testing/www_sec_gov_Archives_edgar_data_745732_000074573218000019_ro.pdf'  # path+str(year)+'.pdf'
    get_data(sector="Oil and gas sector", path=new_path,override=[], company_name="mahimatest", pdf_type='quarter', year_end="December")
    # fix_path= '/home/administrator/different patterns/MahimaUSfiling/' if not kwargs['fix_path'] else kwargs['fix_path']
    # company_list = kwargs['company_list']
    # import os
    # for name in company_list:
    #     path_list = [fix_path+name+'/Year/',fix_path+name+'/Quarter/']
    #     for path in path_list:
    #         if 'Year' in path:
    #             year_list = y_sorting(os.listdir(path))
    #             for year in year_list:
    #                 new_path = '/home/administrator/Desktop/Round 2/US Steel/AR/AR-2016.pdf'#path+str(year)+'.pdf'
    #                 get_data(sector =kwargs['sector'],path=new_path,company_name=name, pdf_type='year', year_end=kwargs['year_end'])
    #     else:
    #         q_list = q_sorting(os.listdir(path))
    #         for qtr in q_list:
    #             new_path = path+qtr.replace(' ','_')+'.pdf'
    #
    #             get_data(sector =kwargs['sector'],path=new_path,company_name=name,pdf_type='quarter', year_end = kwargs['year_end'])
    #         # from.common_files.get_last_qtr_pnl import get_last_qtr_pnl
    #         # get_last_qtr_pnl(year_end = kwargs['year_end'],company_name=name)
    #         # pass


# LoopPdfDir()

def pdf_detail(**kwargs):
    try:
        if 'page_num' in kwargs and kwargs['page_num']:
            file_object = open(kwargs['file'], "rb")
            pdf = PyPDF2.PdfFileReader(file_object)
            page_detail={}
            result = all_pages(override=kwargs['override'], sector=kwargs['sector'], page_detail=page_detail,
                            year_end=kwargs['year_end'],
                            pdf=pdf, file=file_object, c_name=kwargs['c_name'],
                            path=kwargs['file'], f_num=int(kwargs['page_num']), pdf_type=kwargs['pdf_type'])
        else:
            result = get_data(path=kwargs['file'],company_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                              year_end=kwargs['year_end'],sector =kwargs['sector'],override=kwargs['override'])
        return result
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return e

def test(**kwargs):
    from .website_crawl import get_html_page
    get_html_page(c_name=kwargs['c_name'], c_tik=kwargs['c_ticker'], y_end=kwargs['year_end'])


#
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# runner = CrawlerRunner()
# # runner  =CrawlerProcess()
# from website_crawler.website_crawler.spiders.sec_files import WebsiteSpider
# def test(**kwargs):
#     import scrapy
#     from selenium import webdriver
#     from selenium.webdriver.firefox.options import Options
#     from twisted.internet import reactor, defer
#     import logging
#     import time
#     from scrapy.spiders import CrawlSpider
#     from selenium import webdriver
#     from scrapy.crawler import CrawlerProcess
#     from scrapy.settings import default_settings
#
#     # print (kwargs)
#
#     crawl(kwargs['c_name'],kwargs['c_ticker'],kwargs['year_end'])
#     reactor.run()
#
#
# @defer.inlineCallbacks
# def crawl(c_name,c_ticker,year_end):
#     # company_name = raw_input('Enter the company name : ')
#     print ("Opening Browser")
#     yield runner.crawl(WebsiteSpider,c_ticker,c_name,year_end)
#     reactor.stop()
