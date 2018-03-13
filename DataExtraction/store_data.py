import PyPDF2

# from DataExtraction.common_functions import *
# from .old_save import *
from DataExtraction.common_files.all_regex import *
from DataExtraction.common_files.utils import *
from DataExtraction.table_content.get_table_content import table_content
from DataExtraction.common_files.extract_page_data import scrap_pdf_page

def all_pages(**kwargs):
    b_sheet = False
    pnl = False
    f_num= kwargs['f_num'] if 'f_num' in kwargs else 1
    l_num = kwargs['l_num'] if 'f_num' in kwargs else (kwargs['pdf'].getNumPages() + 1)
    for i in range(f_num,l_num):
        print (i)
        data, match = match_regex(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re=[balance_sheet])

        if match and not b_sheet:
            # import pdb;pdb.set_trace()
            bs_data = scrap_pdf_page(year_end=kwargs['year_end'],data=data, p_num=str(i),
                                     path=kwargs['path'], pdf_page=['balance sheet'],
                                     file=kwargs['file'], c_name=kwargs['c_name'],
                                     pdf_type=kwargs['pdf_type'])
            if bs_data:
                b_sheet = True


        elif not pnl:
            print ('ye pnl dekh rha ha behan')
            data, match = match_regex(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re=[pnl1,pnl2])
            if match:

                # import pdb;
                # pdb.set_trace()
                # data, match1= match_regex(page=str(i), path=kwargs['path'], f_obj=kwargs['file'], match_re=pnl2)
                notes_pages = kwargs['page_detail']['notes_section'] if 'notes_section' in kwargs['page_detail'] else 0
                pnl = scrap_pdf_page(year_end=kwargs['year_end'], data=data, p_num=str(i),
                                         path=kwargs['path'], pdf_page=['operations','income'],
                                         file=kwargs['file'], c_name=kwargs['c_name'],
                                         pdf_type=kwargs['pdf_type'],notes=notes_pages)
                if pnl:
                    pnl = True
    # return


            # if pnl_data:
            #     pnl=True


def update_financial_statements(**kwargs):
    page_detail = kwargs['page_detail']
    ##means i have exact page number from table content
    for statement_key, p_num in page_detail['statement_section'].items():
        if 'statement' not in page_detail['statement_section']:
            # import pdb;pdb.set_trace()
            if 'balance sheet' in statement_key.lower() or'balance sheets' in statement_key.lower():
                print (page_detail)

                notes_pages = page_detail['notes_section'] if 'notes_section' in page_detail else 0
                bs_data = scrap_pdf_page(year_end=kwargs['year_end'],p_num=p_num,
                                         path=kwargs['path'],
                                         pdf_page=['balance sheet'],
                                         file=kwargs['f_obj'], notes=notes_pages,
                                         c_name=kwargs['company_name'], pdf_type=kwargs['pdf_type'])

                print (bs_data)

            else:
                if 'operations' in statement_key.lower() or 'income' in statement_key.lower():
                    notes_pages = page_detail['notes_section'] if 'notes_section' in page_detail else 0
                    bs_data = scrap_pdf_page(year_end=kwargs['year_end'], p_num=p_num,
                                             path=kwargs['path'],
                                             pdf_page=['operations','income'],
                                             file=kwargs['f_obj'], notes=notes_pages,
                                             c_name=kwargs['company_name'], pdf_type=kwargs['pdf_type'])

                    print (bs_data)
                print ("operations and cash flow pending hai")
        else:
            f_num = int(page_detail['statement_section']['statement'].split('-')[0])
            l_num = int(page_detail['statement_section']['statement'].split('-')[1])
            all_pages(page_detail =page_detail,year_end=kwargs['year_end'],pdf=kwargs['pdf'], file=kwargs['f_obj'], c_name=kwargs['company_name'], path=kwargs['path'],f_num =f_num,l_num=l_num,pdf_type=kwargs['pdf_type'])
            break;


def get_data(**kwargs):
    page_detail={}
    file_object = open(kwargs['path'], "rb")
    pdf = PyPDF2.PdfFileReader(file_object)
    for num in range(2, (pdf.getNumPages()+1)):
        data = get_page_content(page=num,path=kwargs['path'],file=file_object)
        try:
            if num<=5 and not page_detail:

                print (num)
                # import pdb;pdb.set_trace()
                page_detail = table_content(data=data,page_detail=page_detail,path=kwargs['path'],file=file_object)
                print (page_detail)
                if page_detail  and 'statement_section' in page_detail:
                    update_financial_statements(year_end=kwargs['year_end'],pdf_type =kwargs['pdf_type'],path=kwargs['path'],
                                                page_detail=page_detail,company_name=kwargs['company_name'],f_obj=file_object,pdf=pdf)
                    break;

            elif not page_detail or 'statement_section' not in page_detail:
                # need to loop every page in worst case.
                print (num)

                all_pages(page_detail=page_detail,year_end=kwargs['year_end'],pdf=pdf,file=file_object,c_name=kwargs['company_name'],path=kwargs['path'],pdf_type =kwargs['pdf_type'])
                break;
        except Exception as e:
            print (e)



# def LoopPdfDir():
#     path_list = [#'/home/administrator/DataAutomation/company_pdf/Apple/Quarter/','/home/administrator/DataAutomation/company_pdf/Apple/Year/',
#                 '/home/administrator/DataAutomation/company_pdf/Orchids/Year']
#                 #  '/home/administrator/DataAutomation/company_pdf/Tenet/Quarter/','/home/administrator/DataAutomation/company_pdf/Tenet/Year/',
#                 #  '/home/administrator/DataAutomation/company_pdf/Kona/Quarter/','/home/administrator/DataAutomation/company_pdf/Kona/Year/',
#                 # '/home/administrator/DataAutomation/company_pdf/SeaWorld/Quarter/','/home/administrator/DataAutomation/company_pdf/SeaWorld/Year/']
#     # path_list=['2013.pdf','2016.pdf']
#     import os
#     for path in path_list:
#         for filename in os.listdir(path):
#             print (filename)
#             new_path = path+filename
#             data = get_data(path='/home/administrator/DataAutomation/company_pdf/Hilton/Quarter/June_2017.pdf',company_name='HotelResortOperators')
#             # data = get_data(path='/home/administrator/DataAutomation/company_pdf/different patterns/KoonHoldings/Year/2016.pdf',company_name='Koon')


def LoopPdfDir():
    fix_path='/home/administrator/DataAutomation/company_pdf/'
    # company_list =['Apple_1','Biolase','BOSTONBEER', 'EXTRASPACESTORAGE',
    #                'Hilton','HotelResortOperators','JakksPacific','KoonHoldings','Mid-ConEnergy',
    #                'ScorpioTankers','SocialNetworking','TechnologyConsultingServices','UnitedStatesSteelcompany']

    # company_list=['Apple_1','BOSTONBEER','Hilton','JakksPacific','SocialNetworking','TechnologyConsultingServices','UnitedStatesSteelcompany','Biolase']
    company_list =['ScorpioTankers']
    import os
    for name in company_list:
        path_list = [fix_path+name+'/Year/',fix_path+name+'/Quarter/']
        print (path_list)
        for path in path_list:
            # import pdb;pdb.set_trace()
            if 'Year' in path:
                year_list = y_sorting(os.listdir(path))
                for year in year_list:
                    new_path = path+str(year)+'.pdf'
                    get_data(path=new_path,company_name=name,pdf_type='year',year_end = 'December')
            else:
                q_list = q_sorting(os.listdir(path))
                for qtr in q_list:
                    new_path = path+qtr.replace(' ','_')+'.pdf'
                    get_data(path=new_path,company_name=name,pdf_type='quarter',year_end = 'December')
                    # pass


LoopPdfDir()


