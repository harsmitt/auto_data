from .add_blank_in_data import *
from PNL.extract_pnl import ExtractPNL
from PNL.get_notes_data import *
from BalanceSheet.balance_sheet.extract_balance_sheet import ExtractBalnceSheet

from BalanceSheet.balance_sheet.save_data import save_bsheet
from PNL.save_pnl import *

from .ignore_index import i_index#,ignore_qtr_index
from .mapping_data import qtr_combinations

from DataExtraction.notes_section.get_notes import get_notes_data
from DataExtraction.logger_config import logger
    #,qtr_combinations
'''
This Function is mainly used to extract Page.
 1. loop variable we are using to loop 10 times in case of specific page number extraction.
    Because there are cases where pdf page number is different with theactual page.
    e.g page number 45 is for balance sheet but 
    when we are trying to extract page 45 it is actual page 42 in pdf. mention at the end of the page.

 2.Store units value for unit conversion used later
 3.Some keywords like reports to etc. for droping this page for extraction.
 4. ignore index concept is used for ignore columns(like notes, group company concept ) etc.
 5. geting date obj if all conditions will true then it will call Extraction function
 and notes extraction and saving data into database.
    

Input : sector, year_end,data, p_num, path, pdf_page,override ,file, c_name, pdf_type,notes

Output: balance_sheet_data,pnl_data in True/False (depending on the page ) or an exception
'''

def scrap_pdf_page(**kwargs):
    try:
        balance_sheet_data = False
        unit =''
        pnl_data = False
        subtract=''
        ignore_index =OrderedDict()
        p_num = kwargs['p_num'].split('-')
        pdf_page = copy.deepcopy(p_num[0])
        # if data exists it means it is all_pages extraction else specific page extraction.
        loop = 1 if 'data' in kwargs else 10
        pdf_page_next = int(int(p_num[-1])- int(p_num[0])) if len(p_num)==2  and not check_datetime(p_num[-1]) else 1
        for i in range(loop):
            data_dict = OrderedDict()
            date_obj = []
            date_line = 0
            data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
            if check_content(data=data,p_type = kwargs['pdf_page'],check_statement=True ):
                l_data = data
                for l_num,line in enumerate(l_data):
                    from .mapping_data import ignore_index_list

                    #fetching units for units conversions.
                    if line and any(word in line.lower() for word in['millions','thousands']):
                        x = [w1 for word in line.lower().split() for w1 in ['millions', 'thousands'] if w1 in word]
                        unit =x[0] if x else ''

                    #find if the page is okk to extract or not
                    if any(word in line.lower() for word in
                                          ['results of','supplementary financial data','summary of','overview of','summarizes','summarized as' 'comparison',
                                           'dollers','selected financial data','standalone','statistics','directors']) and not 'special' in kwargs:
                        return balance_sheet_data,pnl_data

                    #if any keyword exists in ignore_index_list

                    elif line and len([i for i in re.split('  +',line) if i]) < 6 and \
                            not (len([i for i in re.split('  +',line) if i])==1 and len([i for i in ignore_index_list if all(word in extract_s(line).split() for word in i)])==1 )\
                            and(len([i for i in ignore_index_list if all(word in extract_s(line).split() for word in i)])>=1\
                            or (kwargs['pdf_page']=='pnl' and len([i for i in qtr_combinations if all(word in line.lower() for word in i)])>=1)):

                        #function called for getting ignore column index.
                        ignore_index, date_obj, date_line = i_index(year_end=kwargs['year_end'], data=data,
                                                                             l_num=l_num,pdf_page = kwargs['pdf_page'],
                                                                             pdf_type=kwargs['pdf_type'],ignore_index=ignore_index,
                                                                             date_obj=date_obj,date_line = date_line)
                        if date_obj: break;

                    #fetching date_obj

                    elif line and not date_obj and not ignore_index:
                        next_line = data[l_num + 1] if len(data) > l_num + 1 else ''
                        date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                         year_end=kwargs['year_end'], date_obj=date_obj,
                                                         date_line=date_line, data=data,
                                                         next_line=next_line, l_num=l_num)


                if date_obj and len(date_obj)<5:

                    if not balance_sheet_data and kwargs['pdf_page']=='bsheet':
                        for pdf in range(pdf_page_next):
                            data = get_page_content(seprator='@@',page=pdf_page, path=kwargs['path'], file=kwargs['file']) if not 'data' in kwargs else kwargs['data']
                            data_dict,unit = ExtractBalnceSheet(page= int(pdf_page)+1, path=kwargs['path'], file=kwargs['file'],date_line=date_line,data_dict=data_dict,data=data,ignore_index=ignore_index,date_obj=date_obj,unit=unit)
                            pdf_page = int(pdf_page) + 1
                        if 'p_extraction' in kwargs or  (data_dict and len(data_dict)>=3 and any(key in list(data_dict.keys()) for key in ['current assets','non current assets','current liablities','non burrent liabilities'])):
                            try:
                                data_dict = get_notes_data(date_obj=date_obj,year_end=kwargs['year_end'],
                                                           pdf_type=kwargs['pdf_type'],data_dict=data_dict,
                                                       page=pdf_page+1, path=kwargs['path'],pdf_page=kwargs['pdf_page'],
                                                       file=kwargs['file'], notes_sec=kwargs['notes'])

                                print (data_dict)
                                data_dict = remove_extra_keys(data_dict=data_dict)
                            except Exception as e:
                                import traceback
                                logger.debug("error in notes section %s " % str(e))
                                logger.debug(traceback.format_exc())
                                pass
                            print (data_dict)
                            #This function actually creates company object and all the financial parameters
                            img_path, c_name = Create_blank_sheet(year_end=kwargs['year_end'],c_name=kwargs['c_name'], path=kwargs['path'], page=pdf_page,dit_name=kwargs['dit_name'])

                            status = save_bsheet(override = kwargs['override'],year_end=kwargs['year_end'],data=data_dict,
                                                 img_path=img_path,
                                                 file=kwargs['file'], page=i, c_name=c_name,new_dict=True,date_obj =date_obj,
                                                 pdf_type = kwargs['pdf_type'],extraction='bsheet',unit=unit)

                            if status :
                                balance_sheet_data =True
                                return (balance_sheet_data,pnl_data)

                    elif not pnl_data and kwargs['pdf_page']=='pnl':
                        for pdf in range(pdf_page_next):
                            data = get_page_content(seprator='@@', page=pdf_page, path=kwargs['path'],file=kwargs['file']) if not 'data' in kwargs else kwargs['data']

                            data_dict,unit = ExtractPNL(date_line=date_line,data_dict=data_dict, data=data,  ignore_index=ignore_index,
                                                       date_obj=date_obj,unit=unit)
                            pdf_page = int(pdf_page) + 1
                        print (data_dict)
                        if 'p_extraction' in kwargs or (data_dict and (len(data_dict) >=4 or all(len(data_dict)>=2 and len(data_dict[x])>=2 for x in list(data_dict.keys())))):
                            try:
                                data_dict = get_notes_data(date_obj=date_obj,year_end=kwargs['year_end'],pdf_type=kwargs['pdf_type'],
                                                           data_dict=data_dict, page=pdf_page+1,
                                                       path=kwargs['path'], file=kwargs['file'],
                                                       pdf_page=kwargs['pdf_page'], notes_sec=kwargs['notes'])
                                data_dict = remove_extra_keys(data_dict=data_dict)
                            except Exception as e:
                                import traceback
                                logger.debug("error in notes section %s " % str(e))
                                logger.debug(traceback.format_exc())
                                pass

                            img_path, c_name = Create_pnl(year_end=kwargs['year_end'], c_name=kwargs['c_name'],dit_name=kwargs['dit_name'],
                                                                  path=kwargs['path'], page=pdf_page)

                            status = save_pnl(override = kwargs['override'],extraction='pnl',subtract=subtract,
                                              sector =kwargs['sector'],year_end=kwargs['year_end'],file=kwargs['file'],
                                              data=data_dict, img_path=img_path,unit=unit,date_obj=date_obj,
                                               page=i, c_name=c_name, new_dict=True, pdf_type=kwargs['pdf_type'])
                            if status:
                                pnl_data =True
                                return balance_sheet_data,pnl_data
                else:
                    pdf_page = str(int(pdf_page) + 1)


            else:
                pdf_page = str(int(pdf_page) + 1)
        return balance_sheet_data,pnl_data

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug("error in scrap pdf page  %s " % e)
        logger.debug(traceback.format_exc())

        return e
