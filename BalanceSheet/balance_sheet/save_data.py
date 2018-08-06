#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: ascii -*-

from django.forms.models import model_to_dict
from DataExtraction.common_files.match_keywords import *

def save_bsheet(**kwargs):
    try:
        data=kwargs['data']

        if kwargs['new_dict']:
            data = get_new_data(override = kwargs['override'],data= kwargs['data'], c_name=kwargs['c_name'],
                                t_pdf = kwargs['pdf_type'],year_end =kwargs['year_end'],
                                model = CompanyBalanceSheetData,p_type = 'bsheet')
            print (data)
            data = unit_conversion(data=data,unit= kwargs['unit'],file=kwargs['file']
                                   ,c_name=kwargs['c_name'], t_pdf = kwargs['pdf_type'],date_obj=kwargs['date_obj'])
        print (data)
        key_list = list(data.keys())

        if 'current assets' not in data :#len(key_list)>5:


            obj_list = copy.deepcopy(bs_objs.comp_mapping_dict['bsheet'])
            save_comp(data = data,extraction=kwargs['extraction'],
                      year_end=kwargs['year_end'],img_path=kwargs['img_path'],
                      page=kwargs['page'],key = 'combine'
                      ,c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],obj_list = obj_list)
        else:
            for key in key_list:
                if key == 'current assets' and 'non current assets' not in key_list:
                    obj_list = copy.deepcopy(bs_objs.comp_mapping_dict['assets'])
                elif key == 'current liabilities' and 'non current liabilities' not in key_list:
                    obj_list = copy.deepcopy(bs_objs.comp_mapping_dict['liabilities'])
                else:
                    obj_list = copy.deepcopy(bs_objs.comp_mapping_dict[key])
                save_comp(data=data[key], extraction=kwargs['extraction'], year_end=kwargs['year_end']
                          , c_name=kwargs['c_name'],img_path=kwargs['img_path'],key=key,
                      page=kwargs['page'], pdf_type=kwargs['pdf_type'],obj_list =obj_list,p_type='bsheet')


        return True
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        return False


def save_comp(**kwargs):
    for comp in kwargs['data']:
        print (comp)
        import pdb;pdb.set_trace()
        if all(word in comp.lower() for word in ['total' , 'discontinued']) or 'total' not in comp.lower():
            obj_save = match_with_db(extraction=kwargs['extraction'], year_end=kwargs['year_end'],
                                     pdf_obj=comp,
                                     pdf_key_list=kwargs['data'], db_key_list= kwargs['obj_list'],
                                     img=kwargs['img_path'],page=kwargs['page'],p_type= kwargs['p_type'],
                                     c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                     model=CompanyBalanceSheetData)
            if not obj_save:
                obj_save = match_synonym(extraction=kwargs['extraction'], pdf_obj=comp,
                                    db_key_list=kwargs['obj_list'],
                                    year_end=kwargs['year_end'],p_type= kwargs['p_type'],
                                    pdf_key_list=kwargs['data'], img=kwargs['img_path'],
                                    page=kwargs['page'],
                                    c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                    model=CompanyBalanceSheetData)

                if not obj_save:
                    if kwargs['key'] != 'stockholders equity' and kwargs['key']!='combine':
                        other_obj = S2Section.objects.filter(
                            item=mapping_dict.other_mapping_dict[kwargs['key']]['other_asset'])
                        other_obj = \
                        list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'subsection',
                                              'subsection__section', 'id'))[0]
                    elif kwargs['key'] =='combine':
                        other_obj = S2Section.objects.filter(item=mapping_dict.other_mapping_dict['current assets']['other_asset'])
                        other_obj = \
                            list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'subsection',
                                                  'subsection__section', 'id'))[0]
                    else:
                        other_obj = SubSection.objects.filter(
                            item=mapping_dict.other_mapping_dict[kwargs['key']]['other_asset'])
                        other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                                          'id'))[0]
                    save_obj = save_data(extraction=kwargs['extraction'], year_end=kwargs['year_end'], comp=comp,
                                         pdf_obj=kwargs['data'][comp],p_type= kwargs['p_type'],
                                         d_obj=other_obj, pdf_type=kwargs['pdf_type'],
                                         type='breakdown', c_name=kwargs['c_name'],
                                         model=CompanyBalanceSheetData)


    return True