from DataExtraction.common_files.mapping_data import pnl_objs,mapping_dict
from .save_functions import *

def save_pnl(**kwargs):
    try:
        if kwargs['new_dict']:
            data = get_new_data(kwargs['data'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],
                                year_end=kwargs['year_end'])

        obj_list = pnl_objs.sector_dict[kwargs['sector']]
        for keyword in data:
            print(keyword)
            if type(data[keyword])!=OrderedDict:
                obj = match_with_db(pdf_obj=keyword,db_key_list= obj_list,year_end=kwargs['year_end'],
                                pdf_key_list=data, img=kwargs['img_path'], page=kwargs['page'],
                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
                if not obj:

                    obj = match_synonym(pdf_obj=keyword, db_key_list=obj_list, year_end=kwargs['year_end'],
                                        pdf_key_list=data, img=kwargs['img_path'], page=kwargs['page'],
                                        c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])

                    if not obj:
                        if 'expense' in keyword:
                            other_key = 'Other Operating Expense'
                        elif 'income' in keyword:
                            other_key = 'Other Operating Revenue'
                        else:
                            other_key = 'Extra PNL Keywords'
                        not_match(keyword=keyword,year_end=kwargs['year_end'],data=data[keyword], type='breakdown',
                               c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],other_key=other_key)

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
                        obj = match_with_db(pdf_obj=key_obj, db_key_list=pnl_objs.sector_section['Oil and Gas Sector'][sec],
                                            year_end=kwargs['year_end'],
                                            pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                            c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
                        if obj:
                            break;
                    if not obj:
                        for sec in section_list:
                            obj = match_synonym(pdf_obj=key_obj, db_key_list=pnl_objs.sector_section['Oil and Gas Sector'][sec],
                                                year_end=kwargs['year_end'],
                                                pdf_key_list=data[keyword], img=kwargs['img_path'], page=kwargs['page'],
                                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
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
                            not_match(keyword=key_obj,year_end=kwargs['year_end'],data=data[keyword][key_obj],type='breakdown',
                                    c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'],other_key=other_key)

        return True
    except:
        return False


def match_with_db(**kwargs):
    try:
        found = False
        for loop, db_obj in enumerate(kwargs['db_key_list']):
            save_obj = False
            for synonym in [key for key in db_obj['i_synonyms'].strip().split('##')  if key]:
                scomp_list = get_alpha(synonym).split()
                c_list = get_alpha(kwargs['pdf_obj']).split()
                if  set(filter(lambda x:x.isalpha() , scomp_list))== set(filter(lambda x:x.isalpha() , c_list)) or \
                                kwargs['pdf_obj'].strip().lower()== synonym.strip(' s').lower():

                    pdf_val = redefined_data(comp=kwargs['pdf_obj'],year_end=kwargs['year_end'],
                                            pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                            d_obj=kwargs['db_key_list'][loop],type='breakdown',
                                                  c_name=kwargs['c_name'])

                    if 'insert' in db_obj :
                        found,save_obj=True,True
                        if kwargs['pdf_type']=='year':
                            save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                  pdf_obj=pdf_val,
                                                  d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                  c_name=kwargs['c_name'], insert=True)
                        else:
                            save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                      pdf_obj=pdf_val,
                                                      d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                      c_name=kwargs['c_name'], insert=True)
                        break;
                    db_obj['insert']=True
                    found = True
                    # save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter], type='synonym', c_name=c_name)
                    if kwargs['pdf_type']=='year':
                        save_obj = save_year_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'], pdf_obj=pdf_val,
                                            d_obj=kwargs['db_key_list'][loop], type='synonym', c_name=kwargs['c_name'])
                    else:
                        save_obj = save_qtr_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'], pdf_obj=pdf_val,
                                             d_obj=kwargs['db_key_list'][loop], type='synonym', c_name=kwargs['c_name'])

                    break;
            if found != True and 'i_breakdown' in db_obj and db_obj['i_breakdown']:
                found,save_obj = match(year_end= kwargs['year_end'],obj_split= db_obj['i_breakdown'].split('##'),p_obj=kwargs['pdf_obj'],
                                       obj_dict=db_obj,img =kwargs['img'],pdf_key_list = kwargs['pdf_key_list'],
                                             page=kwargs['page'], d_obj=kwargs['db_key_list'][loop],c_name= kwargs['c_name'],pdf_type=kwargs['pdf_type'])

            if found != True and 'i_keyword' in db_obj and db_obj['i_keyword']:
                found, save_obj = match(year_end= kwargs['year_end'],obj_split=db_obj['i_keyword'].split('##'), p_obj=kwargs['pdf_obj'],
                                            pdf_key_list = kwargs['pdf_key_list'],obj_dict=db_obj, img=kwargs['img'],
                                        page=kwargs['page'], d_obj=kwargs['db_key_list'][loop],c_name = kwargs['c_name'],pdf_type=kwargs['pdf_type'])


            if save_obj:
                return True
                break;
        else:
            print ("this key already inserted")

    except Exception as e:
        return e

def match(**kwargs):
    try:
        found,save_obj =False,False
        for i_obj in [key for key in kwargs['obj_split']  if key]:
            sim_key = similar_keyword_re % (i_obj[:-1].replace('-', '')) if i_obj.endswith('s ') else similar_keyword_re % (i_obj.strip().replace('-', ''))
            key_2 = extended_key % (i_obj[:-1].replace('-', '')) if i_obj.endswith('s ') else extended_key % (i_obj.strip().replace('-', ''))
            re_obj = re.compile(sim_key, re.I)
            re_obj2 = re.compile(key_2, re.I)
            if re_obj.match(kwargs['p_obj'].replace('-', '')) or re_obj2.match(kwargs['p_obj'].replace('-', '')):

                pdf_val = redefined_data(year_end=kwargs['year_end'], comp=kwargs['p_obj'],
                                              pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
                                              d_obj=kwargs['d_obj'],type='breakdown', c_name=kwargs['c_name'])

                if 'insert' in kwargs['obj_dict']:
                    found = True
                    if kwargs['pdf_type'] == 'year':
                        save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['p_obj'],
                                              pdf_obj=pdf_val,
                                              d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'],insert=True)
                    else:
                        save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['p_obj'],
                                              pdf_obj=pdf_val,
                                              d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'], insert=True)
                    if save_obj:break;
                found = True
                if kwargs['pdf_type']=='year':
                   save_obj = save_year_data(year_end = kwargs['year_end'],comp=kwargs['p_obj'], pdf_obj=pdf_val,
                                         d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'])
                else:
                    save_obj = save_qtr_data(year_end = kwargs['year_end'],comp=kwargs['p_obj'], pdf_obj=pdf_val,
                                              d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'])
                if save_obj: break;
                # save_obj = save_data(comp=kwargs['p_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
                #                      img=kwargs['img'],
                #                      page=kwargs['page'], db_obj=kwargs['d_obj'])
        return found,save_obj

    except Exception as e:
        return e

                
                

