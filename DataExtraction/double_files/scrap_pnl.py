from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine,LTTextLineHorizontal,LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
import re

from .common_functions import *
from collections import OrderedDict


def GetData(file_path):
    print ("mahima")

    qtr_exists = ''
    date_val = False
    date_obj = []
    data_dict = OrderedDict()

    fp = open(file_path, "rb")
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    laparams = LAParams(detect_vertical=True)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for num, page in enumerate(PDFPage.create_pages(document)):
        extracted_text = ""
        interpreter.process_page(page)
        layout = device.get_result()
        print (num)
        for lt_obj in layout:
            if num==48:
                if isinstance(lt_obj, LTTextLineHorizontal) or isinstance(lt_obj, LTTextBoxHorizontal):
                    extracted_text += (lt_obj.get_text())


        r1 = re.compile('[ (A-Za-z0-9. - _ )]consolidated statements of net income *[ (A-Za-z0-9. - )$]',
                        re.IGNORECASE)
        if re.search(r1, extracted_text):
            print (extracted_text)
            for i in extracted_text.split('\n'):
                if i and num_there(i) and not date_val:

                    date_obj, qtr_exists, date_val = get_year(date_obj, i, date_val, qtr_exists)
                    if qtr_exists == False :
                        qtr_exists = False
                        break;
                elif date_val == True:
                    word = i.strip().replace(':', '')
                    print (word)


