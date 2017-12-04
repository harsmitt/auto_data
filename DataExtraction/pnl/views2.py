from .data_scraping import get_data


def LoopPdfDir():
    path_list = [#'/home/administrator/DataAutomation/company_pdf/Apple/Quarter/','/home/administrator/DataAutomation/company_pdf/Apple/Year/',
            '/home/administrator/DataAutomation/company_pdf/Orchids/Year']
                #  '/home/administrator/DataAutomation/company_pdf/Tenet/Quarter/','/home/administrator/DataAutomation/company_pdf/Tenet/Year/',
                #  '/home/administrator/DataAutomation/company_pdf/Kona/Quarter/','/home/administrator/DataAutomation/company_pdf/Kona/Year/',
                # '/home/administrator/DataAutomation/company_pdf/SeaWorld/Quarter/','/home/administrator/DataAutomation/company_pdf/SeaWorld/Year/']
    # path_list=['2013.pdf','2016.pdf']
    import os
    for path in path_list:
        for filename in os.listdir(path):
            print (filename)
            new_path = path+filename
            data = get_data(path='/home/administrator/DataAutomation/company_pdf/Orchids/Year/2013.pdf')


LoopPdfDir()



