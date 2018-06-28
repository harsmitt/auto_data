from DataExtraction.common_files.mapping_data import pnl_objs,mapping_dict
from DataExtraction.common_files.match_keywords import *
from DataExtraction.common_files.save_related_functions import *

import copy

def save_pnl(**kwargs):
    try:
        if kwargs['new_dict']:
            data = get_new_data(override = kwargs['override'],data = kwargs['data'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],
                                year_end=kwargs['year_end'],model=CompanyPNLData,p_type='pnl')
        print (data)
        for keyword in data:
            print (keyword)
            if type(data[keyword])!=OrderedDict:
                obj_list = copy.deepcopy(pnl_objs.sector_dict[kwargs['sector']])
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
                        if 'expense' in keyword:
                            other_key = 'Other Operating Expense'
                        elif 'income' in keyword:
                            other_key = 'Other Operating Revenue'
                        else:
                            other_key = 'Extra PNL Keywords'
                        not_match(keyword=keyword,year_end=kwargs['year_end'],data=data[keyword], type='breakdown',p_type='pnl',
                               c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                  other_key=other_key,model=CompanyPNLData)

            else:
                key_map = mapping_dict.pnl_mapping_dict
                # key_map2= mapping_dict.pnl2_mapping_dict

                data_sec = [j for i, j in key_map.items() for p1 in i if keyword.strip(' s').strip() == p1.strip(' s').lower()]

                if not data_sec:
                    data_sec = ['opearting cost and expense and nonop']

                for key_obj in data[keyword]:
                    section_list =  list(pnl_objs.sector_section['Oil and Gas Sector'].keys()) if not data_sec else data_sec
                    ##todo find that keyword belongs to which section and loop directly that section so that we can save loop time

                    for sec in section_list:
                        objs = copy.deepcopy(pnl_objs.sector_section['Oil and Gas Sector'][sec])
                        obj = match_with_db(extraction =kwargs['extraction'],pdf_obj=key_obj, db_key_list=objs,
                                            year_end=kwargs['year_end'],p_type= 'pnl',
                                            pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                            c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                            model=CompanyPNLData)
                        if obj:
                            break;
                    if not obj:
                        for sec in section_list:
                            objs = copy.deepcopy(pnl_objs.sector_section['Oil and Gas Sector'][sec])
                            obj = match_synonym(extraction =kwargs['extraction'],pdf_obj=key_obj, db_key_list=objs,
                                                year_end=kwargs['year_end'],p_type= 'pnl',
                                                pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                                model=CompanyPNLData)
                            if obj:break;

                        if not obj:
                            if data_sec:
                                other_key = mapping_dict.other_pnl_mapping[sec]
                            elif 'expense' in keyword:
                                other_key ='Other Operating Expense'
                            elif 'income' in keyword:
                                other_key = 'Other Operating Revenue'
                            else:
                                other_key = 'Extra PNL Keywords'
                            not_match(keyword=key_obj,year_end=kwargs['year_end'],data=data[keyword][key_obj],type='breakdown',p_type='pnl',
                                    c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],
                                      other_key=other_key,model=CompanyPNLData)



        if kwargs['subtract']:
            subtract_val = subtarct_values(data = kwargs['data'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],
                                year_end=kwargs['year_end'],model=CompanyPNLData,p_type='pnl',subtract = kwargs['subtract'])
        return True
    except:
        import traceback
        print(traceback.format_exc())
        return False

#for 9 months subtract q1, q2 from q3
#for 6 months subtract q1 from q2

def subtarct_values(**kwargs):
    c_obj = CompanyList.objects.filter(company_name = kwargs['c_name'])
    pnl_obj = CompanyPNLData.objects.filter(gbc_name_id= c_obj[0].id)
    if pnl_obj:
        for i in pnl_obj:
            print(i)
            if kwargs['subtract']=='q1,q2':
                new_val = int(i.q3.q1) - int(i.q2.q1)- int(i.q1.q1)
                q_obj = quarter_data.objects.filter(id=i.q3.id)
            else:
                new_val = int(i.q2.q1)-int(i.q1.q1)
                q_obj = quarter_data.objects.filter(id=i.q2.id)
            n_dict = {'q1': new_val}
            q_obj.update(**n_dict)