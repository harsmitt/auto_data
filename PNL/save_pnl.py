from PNL.models import *
# from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *

import copy
import re
from django.db.models import Q
from DataExtraction.common_files.mapping_data import pnl_objs
from DataExtraction.common_files.all_regex import *
from django.forms.models import model_to_dict


def save_pnl(**kwargs):
    try:
        if kwargs['new_dict']:
            data = get_new_data(kwargs['data'], c_name=kwargs['c_name'], t_pdf=kwargs['pdf_type'],
                                year_end=kwargs['year_end'])
        for keyword in data:
            print(keyword)
            obj_list =pnl_objs.sector_dict['Oil and Gas Sector']
            obj = match_with_db(pdf_obj=keyword,db_key_list= obj_list,year_end=kwargs['year_end'],
                                pdf_key_list=data, img=kwargs['img_path'], page=kwargs['page'],
                                c_name=kwargs['c_name'], pdf_type=kwargs['pdf_type'])
            if not obj:
                if not obj:
                    if 'expense' in keyword.lower():
                        other_exp_obj = SubSection.objects.filter(item__icontains='Other Operating Expense')
                        other_obj = \
                        list(other_exp_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]

                    elif 'income' in keyword.lower():
                        other_inco_obj = SubSection.objects.filter(item__icontains='Other Operating Revenue')
                        other_obj = list(other_inco_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]
                    else:
                        other_inco_obj = SubSection.objects.filter(item__icontains='Extra PNL Keywords')
                        other_obj = \
                        list(other_inco_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]

                    if other_obj:
                        if kwargs['pdf_type'] == 'year':
                            save_obj = save_year_data(year_end=kwargs['year_end'], comp=keyword,
                                                            pdf_obj=data[keyword], d_obj=other_obj, type='breakdown',
                                         c_name=kwargs['c_name'])
                        else:
                            save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=keyword,
                                                            pdf_obj=data[keyword], d_obj=other_obj, type='breakdown',
                                         c_name=kwargs['c_name'])

                        # save_obj = save_year_data(year_end=kwargs['year_end'], comp=keyword,
                        #                                     pdf_obj=data[keyword], d_obj=other_obj, type='breakdown',
                        #                  c_name=kwargs['c_name'])
        return True
    except:
        return False


def match_with_db(**kwargs):
    found = False
    for loop, db_obj in enumerate(kwargs['db_key_list']):
        save_obj = False
        print(db_obj)
        for synonym in db_obj['i_synonyms'].split('##'):
            scomp_list = get_alpha(synonym).split()
            c_list = get_alpha(kwargs['pdf_obj']).split()
            if  set(filter(lambda x:x.isalpha() , scomp_list))== set(filter(lambda x:x.isalpha() , c_list)) or \
                            kwargs['pdf_obj'].strip().lower()== synonym.strip(' s').lower():
                if 'insert' in db_obj :
                    found,save_obj=True,True
                    if kwargs['pdf_type']=='year':
                        save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                              pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                              d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                              c_name=kwargs['c_name'], insert=True)
                    else:
                        save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                  pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                  d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                  c_name=kwargs['c_name'], insert=True)
                    break;
                db_obj['insert']=True
                found = True
                # save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter], type='synonym', c_name=c_name)
                if kwargs['pdf_type']=='year':
                    save_obj = save_year_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                        d_obj=kwargs['db_key_list'][loop], type='synonym', c_name=kwargs['c_name'])
                else:
                    save_obj = save_qtr_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
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


        if found != True:
            break_comp = kwargs['pdf_obj'].split(',')
            for key in db_obj['i_synonyms'].split('##'):
                for b_comp in break_comp:
                    sim_key = similar_keyword_re % (key.strip(' s').replace('-', ''))
                    key_2 = extended_key % (key.strip(' s').replace('-', ''))
                    re_obj = re.compile(sim_key, re.I)
                    re_obj2 = re.compile(key_2, re.I)
                    if re_obj.match(b_comp.replace('-', '')) or re_obj2.match(b_comp.replace('-', '')):
                        if 'insert' in db_obj:
                            found,save_obj = True,True
                            if kwargs['pdf_type'] == 'year':
                                save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                          pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                          d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                          c_name=kwargs['c_name'],insert = True)
                            else:
                                save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                          pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                          d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                          c_name=kwargs['c_name'], insert=True)

                            break;
                        found = True
                        db_obj['insert'] = True
                        if kwargs['pdf_type']=='year':
                            save_obj = save_year_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'],
                                                      pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                 d_obj=kwargs['db_key_list'][loop],
                                                      type='breakdown', c_name=kwargs['c_name'])
                        else:
                            save_obj = save_qtr_data(year_end = kwargs['year_end'],comp=kwargs['pdf_obj'],
                                                 pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                 d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                 c_name=kwargs['c_name'])
                        break;

        if save_obj:
            return True
            break;
    else:
        print ("this key already inserted")

    return False

def match(**kwargs):
    found,save_obj =False,False
    for i_obj in kwargs['obj_split']:
        sim_key = similar_keyword_re % (i_obj.strip(' s').replace('-', ''))
        key_2 = extended_key % (i_obj.strip(' s').replace('-', ''))
        re_obj = re.compile(sim_key, re.I)
        re_obj2 = re.compile(key_2, re.I)
        if re_obj.match(kwargs['p_obj'].replace('-', '')) or re_obj2.match(kwargs['p_obj'].replace('-', '')):
            if 'insert' in kwargs['obj_dict']:
                found = True

                save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['p_obj'],
                                          pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
                                          d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'],insert=True)
                break;
            found = True
            if kwargs['pdf_type']=='year':
               save_obj = save_year_data(year_end = kwargs['year_end'],comp=kwargs['p_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
                                     d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'])
            else:
                save_obj = save_qtr_data(year_end = kwargs['year_end'],comp=kwargs['p_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
                                          d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'])
            # save_obj = save_data(comp=kwargs['p_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['p_obj']],
            #                      img=kwargs['img'],
            #                      page=kwargs['page'], db_obj=kwargs['d_obj'])
    return found,save_obj

                
                

def save_year_data(**kwargs):#obj_name,obj_val,obj_dict,type,c_name):
    print (kwargs['comp'])
    for i, j in enumerate(kwargs['pdf_obj']):
        y_key = get_year_name(j[0],kwargs['year_end'])
        if y_key:
            if 'section' not in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj'] :
                sec_item =kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section__item= sec_item,
                                                 subsection_id=None
                                                 )
            elif 'section' in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj']:
                sub_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],subsection__item= sub_item)


            if gbc_obj and kwargs['type']=='synonym':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                description = y_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if y_obj[
                    0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                if kwargs['comp'] =='total assets':
                    old_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
                                           subsection_id=None)
                    old_y_obj = year_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(int(j[1]) - int(old_y_obj[0].y1))
                    y_dict = {'y1':new_val}
                else:
                    y_dict = {'y1':('0' if str(j[1]) in ['-','—'] else str(j[1])),'description':description} if not 'insert' in kwargs else {'description':description}

                y_obj.update(**y_dict)

            elif gbc_obj and kwargs['type']=='breakdown':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if y_obj:
                    if kwargs['comp'] not in y_obj[0].description.split(','):
                        if '(' in str(j[1]) or '(' in y_obj[0].y1:
                            i2 = int(str(j[1]).replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = int(y_obj[0].y1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            val = int(y_obj[0].y1.replace(',', ''))+int(('0' if str(j[1]) in ['-','—'] else str(j[1])).replace(',', ''))
                        description = y_obj[0].description +'##'+kwargs['comp']+'('+ str(j[1])+')' if y_obj[0].description else kwargs['comp']+'('+ str(j[1])+')'
                        y_dict = {'y1': val,'description':description} if not 'insert' in kwargs else {'description':description}
                        y_obj.update(**y_dict)
                    else:
                        pass
    return True



def save_qtr_data(**kwargs):

    print (kwargs['comp'])

    for i, j in enumerate(kwargs['pdf_obj']):
        q_key = get_quarter_name(j[0],kwargs['year_end'])#'q' + str(i + 1)
        if q_key:
            if 'section' not in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj'] :
                sec_item =kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section__item= sec_item,
                                                 subsection_id=None
                                                 )
            elif 'section' in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj']:
                sub_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],subsection__item= sub_item)
            # else:
            #     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section_id= kwargs['d_obj']['subsection__section'],
            #                                      subsection_id= kwargs['d_obj']['subsection'],s2section__item= kwargs['d_obj']['item'])

            if gbc_obj and kwargs['type']=='synonym':
                get_id = q_key + '_id'
                q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                description = q_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if q_obj[
                    0].description else kwargs['comp'] + '(' + str(j[1]) + ')'

                if kwargs['comp'] =='total assets':
                    old_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
                                           subsection_id=None)
                    old_q_obj = quarter_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(int(j[1]) - int(old_q_obj[0].q1))
                    q_dict = {'q1':new_val}
                else:
                    q_dict = {'q1': ('0' if str(j[1]) in ['-', '—'] else str(j[1])),
                              'description': description} if not 'insert' in kwargs else {'description': description}
                q_obj.update(**q_dict)

            elif gbc_obj and kwargs['type']=='breakdown':
                get_id = q_key + '_id'
                q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if q_obj:
                    if kwargs['comp'] not in q_obj[0].description.split(','):
                        if '(' in j[1] or '(' in q_obj[0].q1:
                            i2 = int(j[1].replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = int(q_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            val = int(q_obj[0].q1.replace(',', ''))+int(('0' if j[1] in ['-','—'] else j[1]).replace(',', ''))
                        description = q_obj[0].description +'##'+kwargs['comp']+'('+ str(j[1])+')' if q_obj[0].description else kwargs['comp']+'('+ str(j[1])+')'
                        q_dict = {'q1': val,'description':description}
                        q_obj.update(**q_dict)
                    else:
                        pass
    return True


def get_new_data(data,c_name,t_pdf,year_end):
    data_list = list(data.values())
    d_val = data_list[0]
    year_list,val = map(list,zip(*d_val))
    for year in year_list:
        if t_pdf == 'year':
            y_key = get_year_name(year,year_end)
            y1_key = y_key +'__y1'
        else:
            y_key = get_quarter_name(year,year_end)
            y1_key = y_key + '__q1'
        year_exist = CompanyPNLData.objects.filter(gbc_name__company_name=c_name).filter(~Q(**{y_key:None}),~Q(**{y1_key:'0'}))
        # year_exist= year_data.objects.filter(year_date=year)
        if year_exist :
            for i in data_list:
                for dict1 in i:

                    old_dict = dict(i)
                    if year in old_dict:del(old_dict[year])
                    i= [(i,j) for i,j in old_dict.items()]
            # print (data_list)
    return data