from DataExtraction.common_files.mapping_data import pnl_objs,mapping_dict
from DataExtraction.common_files.match_keywords import *
from DataExtraction.common_files.save_related_functions import *

import copy

def save_pnl(**kwargs):
    try:
        if kwargs['new_dict']:
            data = get_new_data(override = kwargs['override'],data = kwargs['data'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],
                                year_end=kwargs['year_end'],model=CompanyPNLData,p_type='pnl')

            data = unit_conversion(data=data, unit=kwargs['unit'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],date_obj=kwargs['date_obj'])

        for keyword in data:
            if type(data[keyword])!=OrderedDict :
                if 'total' not in keyword:
                    obj_list = copy.deepcopy(pnl_objs.sector_dict[kwargs['sector']])
                    obj = match_with_formula_cell(pdf_obj=keyword)
                    if not obj:
                        obj = match_with_db(extraction =kwargs['extraction'],pdf_obj=keyword,
                                            db_key_list= obj_list,year_end=kwargs['year_end'],
                                        pdf_key_list=data, img=kwargs['img_path'], page=kwargs['page'],
                                            p_type= 'pnl',model =CompanyPNLData,
                                        c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
                        if not obj:

                            obj = match_synonym(extraction =kwargs['extraction'],pdf_obj=keyword, db_key_list=obj_list, year_end=kwargs['year_end'],
                                                p_type='pnl',pdf_key_list=data, img=kwargs['img_path'], page=kwargs['page'],
                                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                                model=CompanyPNLData)

                            if not obj:
                                other_key = 'Extra PNL Keywords'
                                not_match(keyword=keyword,year_end=kwargs['year_end'],data=data[keyword], type='breakdown',p_type='pnl',
                                       c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                          other_key=other_key,model=CompanyPNLData)

            else:
                key_map = mapping_dict.pnl_mapping_dict
                data_sec=[]
                # key_map2= mapping_dict.pnl2_mapping_dict
                #todo add concept of combination and breakdown concept for key_map
                    # for p1 in key1
                for key1, val1 in key_map.items():
                    for key2 in key1:
                        if match_breakdown_words(match_with=key2, pdf_obj=keyword.replace('-', '')):
                            data_sec = [key_map[key1]]
                            break;#[j for i, j in key_map.items() for p1 in i if keyword.strip(' s').strip() == p1.strip(' s').lower()]

                if not data_sec:
                    data_sec = ['opearting cost and expense and nonop']

                for key_obj in data[keyword]:
                    if  'total' not in key_obj:
                        section_list =  list(pnl_objs.sector_section[kwargs['sector']].keys()) if not data_sec else data_sec
                        ##todo find that keyword belongs to which section and loop directly that section so that we can save loop time

                        for sec in section_list:
                            objs = copy.deepcopy(pnl_objs.sector_section[kwargs['sector']][sec])

                            obj = match_with_formula_cell(pdf_obj=key_obj)
                            if not obj:
                                obj = match_with_db(extraction =kwargs['extraction'],pdf_obj=key_obj, db_key_list=objs,
                                                    year_end=kwargs['year_end'],p_type= 'pnl',
                                                    pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                                    c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                                    model=CompanyPNLData)
                            if obj:
                                break;
                        if not obj:
                            for sec in section_list:
                                objs = copy.deepcopy(pnl_objs.sector_section[kwargs['sector']][sec])
                                obj = match_synonym(extraction =kwargs['extraction'],pdf_obj=key_obj, db_key_list=objs,
                                                    year_end=kwargs['year_end'],p_type= 'pnl',
                                                    pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                                    c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                                    model=CompanyPNLData)
                                if obj:break;

                            if not obj:
                                if data_sec:
                                    other_key = mapping_dict.other_pnl_mapping[sec]
                                else:
                                    other_key = 'Extra PNL Keywords'
                                not_match(keyword=key_obj,year_end=kwargs['year_end'],data=data[keyword][key_obj],type='breakdown',p_type='pnl',
                                        c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                          other_key=other_key,model=CompanyPNLData)

        return True
    except:
        import traceback
        print(traceback.format_exc())
        return False

def match_with_formula_cell(**kwargs):
    import itertools
    pnl_sec = Section.objects.filter(i_related = 'Profit and Loss')
    for s_obj in pnl_sec:
        for syn in s_obj.i_synonyms.split('##'):
            x2 = list(itertools.permutations(syn.split(), len(syn.split())))
            obj_per = [' '.join(word) for word in x2]
            if kwargs['pdf_obj'] in obj_per:
                return True
    return False