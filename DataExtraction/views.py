import PyPDF2
from  .scrap_pdf import pdftotext
from .save_data import match_keyword
# from .scrap_pnl import match_keyword
from .save_data_qtr import match_keyword_qtr
from .common_functions import *

def getQuarterContent(path,c_name):
    p = open(path, "rb")
    pdf = PyPDF2.PdfFileReader(p)
    for i in range(1, (pdf.getNumPages()+1)):
        if i ==1:
            company_name =pdftotext(path,page=i,file_type='qtr',company_name='')
            print (company_name)
            company_name = c_name.encode('utf-8') if not company_name or company_name[0].decode('utf-8')=='' else company_name[0]
        else:
            data,qtr_exists = pdftotext(path,page=i,file_type='qtr',company_name=company_name)
            if data :
                # import pdb;pdb.set_trace()
                # img_path = Create_blank_sheet(company_name,path,i)
                status = match_keyword_qtr(data,path,page=i,company_name=company_name)
                break;
    return company_name


def getYearContent(path,c_name):
    p = open(path, "rb")
    pdf = PyPDF2.PdfFileReader(p)
    for i in range(1, (pdf.getNumPages() + 1)):
        if i == 1:
            company_name =pdftotext(path,page=i,file_type='year',company_name='')
            print(company_name)
            company_name = c_name.encode('utf-8') if not company_name or company_name[0].decode('utf-8') =='' else company_name[0]
        else:
            print (i)
            data,qtr_exists = pdftotext(path,page=i,file_type='year',company_name=company_name)
            if data:
                status = match_keyword(data=data,path=path,page=i,company_name=company_name,new_dict=True)
                break;
    print (i)

def LoopPdfDir():
    fix_path='/home/administrator/DataAutomation/company_pdf/'
    # company_list =['Apple_1','Biolase','BOSTONBEER', 'EXTRASPACESTORAGE',
    #                'Hilton','HotelResortOperators','JakksPacific','KoonHoldings','Mid-ConEnergy',
    #                'ScorpioTankers','SocialNetworking','TechnologyConsultingServices','UnitedStatesSteelcompany']

    company_list=['American_Woodmark','Biolase','Apple_1','BOSTONBEER','Hilton','JakksPacific','SocialNetworking','TechnologyConsultingServices','UnitedStatesSteelcompany']
    # company_list =['American_Woodmark']
    import os
    for name in company_list:
        path_list = [fix_path+name+'/Quarter/', fix_path+name+'/Year/']
        print (path_list)
        for path in path_list:
            # import pdb;pdb.set_trace()
            if 'Year' in path:
                year_list = y_sorting(os.listdir(path))
                for year in year_list:
                    print (year)
                    new_path = path+str(year)+'.pdf'
                    getYearContent(new_path,c_name=name)
            else:
                q_list = q_sorting(os.listdir(path))
                for qtr in q_list:
                    new_path = path+qtr.replace(' ','_')+'.pdf'
                    getQuarterContent(new_path,c_name=name)
                    pass
    # for path in path_list:
    #     for filename in os.listdir(path):
    #         print (filename)
    #         new_path = path+filename
    #         if 'Quarter' in path:
    #             # getQuarterContent(new_path)
    #             pass
    #         else:
    #             getYearContent(new_path)
    #             # pass

LoopPdfDir()



