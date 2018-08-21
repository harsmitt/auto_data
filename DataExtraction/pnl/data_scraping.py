import PyPDF2

from DataExtraction.pnl.save_pnl import *
from .utils import *


def get_data(*args,**kwargs):
    company_name=''

    page_detail={}

    page=1

    file_object = open(kwargs['path'], "rb")
    pdf = PyPDF2.PdfFileReader(file_object)

    for num in range(1, (pdf.getNumPages()+1)):
        data = get_page_content(page=num,path=kwargs['path'],file=file_object)
        try:
            if num == 1 and not company_name:
                str1 = 'Name of Registrant as Specified in its Charter'
                company_name = [data[key - 1].strip() for key, i in enumerate(data) if
                                (str1).lower() in i.decode('utf8').lower()]
                if not company_name:
                    company_name = [data[key].strip() for key, i in enumerate(data) if
                                ('company\n').lower() in i.decode('utf8').lower()]
                page += 1

            elif not page_detail:
                page_detail = table_content(data=data,page_detail=page_detail,path=kwargs['path'],file=file_object)
                print (page_detail)

            else:
                for key,p_num in page_detail['page_list'].items():
                    if 'operations' in key.lower() or 'income' in key.lower():
                        op_data,real_page = get_operations_data(num=p_num,path=kwargs['path'],file=file_object)
                        print (op_data)
                        if op_data:
                            save_pnl(data=op_data,page=real_page,path=kwargs['path'],company_name=company_name[0])

                # print ("abhi pending ha")

        except:
            print ("kuch to locha ha")

