from DataExtraction.store_data import pdf_detail
import os


def upload_pdf(file, filename):
    try:
        if not os.path.exists('/home/administrator/Desktop/uploads/'):
            os.mkdir('/home/administrator/Desktop/uploads/')

        with open('/home/administrator/Desktop/uploads/' + filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return True,'/home/administrator/Desktop/uploads/' + filename
    except:
        return False

# def extract(**kwargs):
#     import pdb;pdb.set_trace()
#     print (kwargs)
#     path = kwargs['file'],
#     company_name = kwargs['c_name'], pdf_type = kwargs['pdf_type'], year_end = kwargs['year_end'])
#
#     pdf_detail(file = kwargs['file'],pdf_type=kwargs['pdf_type'],year_end=kwargs['year_end'])
#



