import PyPDF2

# from DataExtraction.common_functions import *
# from .old_save import *
from DataExtraction.common_files.all_regex import *
from DataExtraction.common_files.utils import *
from DataExtraction.table_content.get_table_content import table_content
from DataExtraction.common_files.extract_page_data import scrap_pdf_page

def get_start_page(**kwargs):
    f_num=1
    for page in range(1,kwargs['l_num']):
        data = get_page_content(seprator='@@', page=page, path=kwargs['path'], file=kwargs['f_obj'])
        if any('Report of Independent'.lower() in line.lower() for line in data):
            f_num = page
            break;

    return f_num

'''

This Function for complete pdf scanning for extracting from page 1 to last.
we need to match patterns for the correct page. (match_re_list)
if all conditions runs successfully then it will pass data to scrap_pdf_page.
b_sheet For Balance Sheet and pnl  for PNL. 
if balance sheet gets extracted then set b_sheet = True
 and for the remaining pages it will consider only PNL
 Same for the PNL.
 
 Input : override, sector, page_detail , year_end , pdf(PyPDF2 object), file_object, company_name, FilePath,f_num, pdf_type
 Output :return True/False or an exception. 

'''

def all_pages(**kwargs):
    try:
        b_sheet = False
        pnl = False
        if kwargs['pdf_type']!='year':
            f_num=  kwargs['f_num'] if 'f_num' in kwargs else 1
            l_num = kwargs['l_num'] if 'l_num' in kwargs else (kwargs['pdf'].getNumPages() + 1)
        else:
            l_num =kwargs['l_num'] if 'l_num' in kwargs else (kwargs['pdf'].getNumPages() + 1)
            f_num = get_start_page(path=kwargs['path'], f_obj=kwargs['file'] ,l_num=l_num)
        notes_pages = kwargs['page_detail']['notes_section'] if 'notes_section' in kwargs['page_detail'] else 0

        if 'status' in kwargs and kwargs['status']:
            status_keys = list(kwargs['status'].keys())
            if 'bsheet' in status_keys:
                b_sheet = True
            else:
                pnl = True
            status = kwargs['status']
        else:
            status = OrderedDict()

        for i in range(f_num,l_num):
            #get data and match patterns with balance sheet keywords
            data,match = match_re_list(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re='bsheet')
            if match and not b_sheet:
                bs_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'],data=data, p_num=str(i),
                                         path=kwargs['path'], pdf_page='bsheet',override = kwargs['override'],
                                         file=kwargs['file'], c_name=kwargs['c_name'],dit_name=kwargs['dit_name'],
                                         pdf_type=kwargs['pdf_type'],notes=notes_pages)
                if bs_data[0]:
                    b_sheet = True
                    status['bsheet']=True


            elif not pnl:
                # get data and match patterns with PNL keywords
                data,match = match_re_list(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re='pnl')
                if match and not pnl:
                    pnl_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'], data=data, p_num=str(i),
                                             path=kwargs['path'], pdf_page='pnl',override = kwargs['override'],
                                             file=kwargs['file'], c_name=kwargs['c_name'],dit_name=kwargs['dit_name'],
                                             pdf_type=kwargs['pdf_type'],notes=notes_pages)

                    if pnl_data[1]:
                        pnl = True
                        status['pnl']=True


        return status

    except Exception as e:
        import traceback
        # logger.error("error in all pages %s " %e)
        # logger.error(traceback.format_exc())
        return e

'''
This function will call only when we have the specific page number for statements.
In case any issue comes then complete extraction will be called.

Input: sector,year_end,pdf_type,path,page_detail,company_name,file_object,pdf,override

Output: return True/False.

'''
def update_financial_statements(**kwargs):
    try:
        bs_data = False
        status = OrderedDict()

        page_detail = kwargs['page_detail']
        # logger.info('entering in update_finanical')
        ##means i have exact page number from table content
        if 'statement' not in page_detail['statement_section']:
            if all(key in page_detail['statement_section'] for key in ['bsheet','pnl']):
                for statement_key, p_num in page_detail['statement_section'].items():
                    if statement_key in ['bsheet','pnl']:
                        # getting notes section key to pass in scrap pdf
                        notes_pages = page_detail['notes_section'] if 'notes_section' in page_detail else 0

                        # calling scrap pdf page to extract that page
                        # logger.ingo("calleg scrap page for %s") %(statement_key)

                        bs_data = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'],p_num=p_num,
                                                 path=kwargs['path'],override = kwargs['override'],
                                                 pdf_page= statement_key,dit_name=kwargs['dit_name'],
                                                 file=kwargs['f_obj'], notes=notes_pages,special=True,
                                                 c_name=kwargs['company_name'], pdf_type=kwargs['pdf_type'])

                        if True in bs_data:
                            status[statement_key] = True

                        elif bs_data == (False,False) or type(bs_data)==AttributeError:

                            break;

                if bs_data == (False,False) or type(bs_data)==AttributeError:

                    #if not bs_data then it process will run for all pdf pages.
                    status = all_pages(sector=kwargs['sector'], page_detail=page_detail, year_end=kwargs['year_end'],status=status,
                            pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],dit_name=kwargs['dit_name'],
                            path=kwargs['path'],pdf_type=kwargs['pdf_type'],override = kwargs['override'])


            else:
                status = all_pages(sector=kwargs['sector'], page_detail=page_detail, year_end=kwargs['year_end'],status=status,
                                dit_name=kwargs['dit_name'],pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],
                                path=kwargs['path'], pdf_type=kwargs['pdf_type'],override = kwargs['override'])

                return status

        else:
            f_num = int(page_detail['statement_section']['statement'].split('-')[0])
            status = all_pages(override = kwargs['override'],sector =kwargs['sector'],page_detail =page_detail,year_end=kwargs['year_end'],
                            dit_name=kwargs['dit_name'],pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'],
                            path=kwargs['path'],f_num =f_num,pdf_type=kwargs['pdf_type'],status=status)
            return status

        return status

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        # logger.error('error in update financial statement %s'  % e)
        # logger.error(traceback.format_exc())
        return e
'''
This will be main function for pdf processing, passing pdf then get its table content
and then start process it depending on table content output.

Input : filepath,company_name, pdf_type,year_end,sector,override
                
Output :  Return True/False
  
'''

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
                                                          dit_name=kwargs['dit_name'],page_detail=page_detail,company_name=kwargs['company_name'],
                                                          f_obj=file_object,pdf=pdf,override = kwargs['override'])
                        break;

                elif not page_detail or 'statement_section' not in page_detail:
                    # need to loop every page in worst case.
                    res = all_pages(override = kwargs['override'],sector =kwargs['sector'],page_detail=page_detail,
                                    year_end=kwargs['year_end'],pdf=pdf,file=file_object,
                                    dit_name=kwargs['dit_name'],c_name=kwargs['company_name'],path=kwargs['path'],
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
        # logger.error("Error is %s" % e)
        # logger.error(traceback.format_exc())
        return e



def LoopPdfDir(**kwargs):
    new_path = '/home/mahima/+Akshat/Other Countries/Emperor Entertainment Hotel Limited-Hong Kong SAR China/source file/AR/AR 2010.pdf'
    result = get_data(sector="Aviation Services", path=new_path,override=[],dit_name='Sugarcane Farming & Processing', company_name="china test", pdf_type='year', year_end="December")
    print (result)
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

"""
If page_num in kwargs then it will extract that page directly from pdf 
          else it will call get_data for pdf extraction
          
Input : company_name,sector,year_end, FilePath, pdf_type(year or qtr) ,
                override (if you want to override any existing year's data ),
                page_num(for specific page extraction) 
          
Output : Result will be True/False or an exception.

"""
def pdf_detail(**kwargs):
    try:
        if [key for key,val in kwargs['page_num'].items() if any(val)]:
            for key,pnum in kwargs['page_num'].items():
                file_object = open(kwargs['file'], "rb")
                pdf = PyPDF2.PdfFileReader(file_object)
                notes = {}#0 if not pnum else int(pnum)+3
                if pnum:
                    if key == 'bs_num':
                        result = scrap_pdf_page(sector =kwargs['sector'],year_end=kwargs['year_end'],
                                                 p_num=pnum,p_extraction=True,
                                                 path=kwargs['file'],override = kwargs['override'],
                                                 pdf_page= 'bsheet',dit_name=kwargs['dit_name'],
                                                 file=file_object, notes=notes,special=True,
                                                 c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
                        # print (bs_data)

                    elif key == 'pnl_num':
                        # logger.info("specific Balance Sheet Page number")
                        result = scrap_pdf_page(sector=kwargs['sector'], year_end=kwargs['year_end'],
                                                p_num=pnum,p_extraction=True,
                                                path=kwargs['file'], override=kwargs['override'],
                                                pdf_page='pnl', dit_name=kwargs['dit_name'],
                                                file=file_object, notes=notes,special=True,
                                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
                    else:
                        print ("call Notes section")

        else:
            #for pdf extraction

            result = get_data(path=kwargs['file'],company_name=kwargs['c_name'],
                              pdf_type=kwargs['pdf_type'],dit_name=kwargs['dit_name'],
                                  year_end=kwargs['year_end'],sector =kwargs['sector'],override=kwargs['override'])

        return result
    except Exception as e:
        import traceback
        # logger.error("error in pdf detail %s " % e)
        # logger.error(traceback.format_exc())
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
