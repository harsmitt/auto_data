from DataExtraction.store_data import pdf_detail
import os

Default_path='/home/administrator/Desktop/uploads/'

def upload_pdf(file_1,c_name, file_n):
    try:
        path = os.path.join(Default_path, c_name)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                import traceback
                print (traceback.format_exc())
        path+='/'
        with open(path + file_n, 'wb+') as destination:
            for chunk in file_1.chunks():
                destination.write(chunk)

        return True, path+ file_n

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return False


