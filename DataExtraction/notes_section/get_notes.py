from DataExtraction.common_files.utils import *
from DataExtraction.common_files.all_regex import *
from DataExtraction.common_files.basic_functions import *
from .extracted_notes import extract_notes
notes_key =['net sales', 'cost of sales','selling, general and administrative expenses','interest expense', 'other income','other income expense, net', 'other income expense , net']
import PyPDF2


def get_notes_pages(**kwargs):
    try:
        notes_section_dict=OrderedDict()
        pdf = PyPDF2.PdfFileReader(kwargs['file'])
        end = (pdf.getNumPages() + 1)
        if kwargs['pdf_type'] =='year':
            if kwargs['notes_sec'] :
                if len(list(kwargs['notes_sec'].keys()))==2:
                    for key in list(kwargs['notes_sec'].keys()):
                        f_num = kwargs['notes_sec'][key].split('-')[0]
                        if len(kwargs['notes_sec'][key].split('-'))==2:
                            l_num = kwargs['notes_sec'][key].split('-')[-1]
                        else:
                            if key == 'discussion':
                                l_num = kwargs['page']
                            else:
                                l_num = end
                        notes_section_dict[key] = OrderedDict({'f_num':f_num,'l_num':l_num})
                elif len(list(kwargs['notes_sec'].keys()))==1:
                    if 'discussion' in kwargs['notes_sec']:
                        f_num = kwargs['notes_sec']['discussion'].split('-')[0]
                        if len(kwargs['notes_sec']['discussion'].split('-'))==2:
                            l_num = kwargs['notes_sec']['discussion'].split('-')[-1]
                        else:
                             l_num = kwargs['page']
                        notes_section_dict['discussion'] = OrderedDict({'f_num': f_num, 'l_num': l_num})
                        notes_section_dict['notes'] = OrderedDict({'f_num': kwargs['page'], 'l_num': end})
                    else:
                        f_num = kwargs['notes_sec']['notes'].split('-')[0]
                        if len(kwargs['notes_sec']['discussion'].split('-')) == 2:
                            l_num = kwargs['notes_sec']['notes'].split('-')[-1]
                        else:
                            l_num = end
                        notes_section_dict['discussion'] = OrderedDict({'f_num': 1, 'l_num': kwargs['page']})
                        notes_section_dict['notes'] = OrderedDict({'f_num': f_num, 'l_num': l_num})

            else:
                notes_section_dict['discussion'] = OrderedDict({'f_num':1,'l_num':kwargs['page']})
                notes_section_dict['notes'] = OrderedDict({'f_num': kwargs['page'], 'l_num': end})

        elif kwargs['pdf_type'] == 'quarter':
            notes_section_dict['notes'] = OrderedDict({'f_num': kwargs['page'], 'l_num': end})

        return notes_section_dict
    except:
        pass


def find_breakup_bsheet(**kwargs):
    key_list =[]
    pdf_page_keys = list(kwargs['data_dict'].keys())
    for key in pdf_page_keys:
        if type(kwargs['data_dict'][key])==OrderedDict:
            for i_key in kwargs['data_dict'][key]:
                key_list.append(i_key)
        elif key:
            key_list.append(key)
        else:
            pass
    key_list = [i for i in key_list if i]
    return key_list

def get_notes_data(**kwargs):
    try:
        import pdb;pdb.set_trace()
        pdf_page_keys = find_breakup_bsheet(data_dict=kwargs['data_dict'])
        page_detail = get_notes_pages(pdf_type = kwargs['pdf_type'],pdf_page = kwargs['pdf_page'],
                                      notes_sec=kwargs['notes_sec'],page= kwargs['page'],
                                      file=kwargs['file'])
        data_dict,pdf_page_keys = extract_notes(year_end=kwargs['year_end'],date_obj=kwargs['date_obj'],
                                  pdf_type = kwargs['pdf_type'],key = page_detail['notes'],
                                  data_dict = kwargs['data_dict'],path=kwargs['path'],
                                  file=kwargs['file'],pdf_page_keys = pdf_page_keys,pdf_page = kwargs['pdf_page'],)

        if data_dict:
            data_dict,pdf_page_keys = extract_notes(year_end=kwargs['year_end'], date_obj=kwargs['date_obj'],
                                  pdf_type=kwargs['pdf_type'], key=page_detail['discussion'],
                                  data_dict=data_dict, path=kwargs['path'],
                                  file=kwargs['file'],pdf_page_keys = pdf_page_keys,pdf_page = kwargs['pdf_page'],)
        return data_dict
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        print("error hai get notes +" ,str(e))
        return kwargs['data_dict']
