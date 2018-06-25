#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: ascii -*-
from DataExtraction.models import *
from PNL.models import *
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
from DataExtraction.common_files.all_regex import *
# from .redefined_extracted_data import *
from django.db.models import Q
#
#
# def not_match(**kwargs):
#
#     # if 'expense' in kwargs['keyword'].lower():
#     try:
#
#         other_obj = SubSection.objects.filter(item__icontains=kwargs['other_key'])
#         if not other_obj:
#             other_obj = SubSection.objects.filter(item__icontains=kwargs['other_key'])
#
#         other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]
#
#
#         if other_obj:
#             if kwargs['pdf_type'] == 'year':
#                 save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['keyword'],
#                                           pdf_obj=kwargs['data'], d_obj=other_obj, type=kwargs['type'],
#                                           c_name=kwargs['c_name'])
#             else:
#                 save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['keyword'],
#                                           pdf_obj=kwargs['data'], d_obj=other_obj, type=kwargs['type'],
#                                           c_name=kwargs['c_name'])
#
#     except Exception as e:
#         return e

#
#
#
# def save_year_data(**kwargs):
#     try:
#         for i, j in enumerate(kwargs['pdf_obj']):
#             y_key = get_year_name(j[0],kwargs['year_end'])
#             if y_key:
#                 if 'section' not in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj'] :
#                     sec_item =kwargs['d_obj']['item'].split('##')[-1]
#                     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section__item= sec_item,
#                                                      subsection_id=None
#                                                      )
#                 elif 'section' in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj']:
#                     sub_item = kwargs['d_obj']['item'].split('##')[-1]
#                     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],subsection__item= sub_item)
#                 else:
#                     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section_id=kwargs['d_obj']['subsection__section'],
#                                                      subsection_id=kwargs['d_obj']['subsection'],s2section__item=kwargs['d_obj']['item'])
#
#                 if gbc_obj and kwargs['type']=='synonym':
#                     get_id = y_key + '_id'
#                     y_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
#                     description = y_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if y_obj[
#                         0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
#                     if kwargs['comp'] =='total assets':
#                         old_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
#                                                subsection_id=None)
#                         old_y_obj = quarter_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
#                         new_val = str(int(j[1]) - int(old_y_obj[0].q1))
#                         y_dict = {'q1':new_val}
#                     else:
#                         y_dict = {'q1':('0' if str(j[1]) in ['-','—'] else str(j[1])),'description':description} if not 'insert' in kwargs else {'description':description}
#                     y_obj.update(**y_dict)
#                 elif gbc_obj and kwargs['type']=='breakdown':
#                     get_id = y_key + '_id'
#                     y_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
#                     if y_obj:
#                         if kwargs['comp'] not in y_obj[0].description.split(','):
#                             if '(' in str(j[1]) or '(' in y_obj[0].q1:
#                                 i2 = int(str(j[1]).replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
#                                 i1 = int(y_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
#                                 val = i1 + i2
#                                 val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
#                             else:
#                                 val = int(y_obj[0].q1.replace(',', ''))+int(('0' if str(j[1]) in ['-','—'] else str(j[1])).replace(',', ''))
#                             description = y_obj[0].description +'##'+kwargs['comp']+'('+ str(j[1])+')' if y_obj[0].description else kwargs['comp']+'('+ str(j[1])+')'
#                             y_dict = {'q1': val,'description':description} if not 'insert' in kwargs else {'description':description}
#                             y_obj.update(**y_dict)
#                         else:
#                             pass
#         return True
#     except Exception as e:
#         return e
#
# def match_synonym(**kwargs):
#     try:
#         for loop, db_obj in enumerate(kwargs['db_key_list']):
#             save_obj = False
#             break_comp = kwargs['pdf_obj'].strip().split(',')
#             for key in [key for key in db_obj['i_synonyms'].strip().split('##')  if key]:
#                 for b_comp in break_comp:
#                     sim_key = similar_keyword_re % (key[:-1].lower().replace('-', '')) if key.endswith(
#                         's ') else similar_keyword_re % (key.strip().lower().replace('-', ''))
#                     key_2 = extended_key % (key[:-1].lower().replace('-', '')) if key.endswith('s ') else extended_key % (
#                     key.strip().lower().replace('-', ''))
#                     re_obj = re.compile(sim_key, re.I)
#                     re_obj2 = re.compile(key_2, re.I)
#                     if re_obj.match(b_comp.replace('-', '')) or re_obj2.match(b_comp.replace('-', '')):
#                         pdf_val = redefined_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
#                                                           pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
#                                                           d_obj=kwargs['db_key_list'][loop], type='breakdown',
#                                                           c_name=kwargs['c_name'])
#                         if 'insert' in db_obj:
#                             found, save_obj = True, True
#                             if kwargs['pdf_type'] == 'year':
#                                 save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
#                                                           pdf_obj=pdf_val,
#                                                           d_obj=kwargs['db_key_list'][loop], type='breakdown',
#                                                           c_name=kwargs['c_name'], insert=True)
#                             else:
#                                 save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
#                                                          pdf_obj=pdf_val,
#                                                          d_obj=kwargs['db_key_list'][loop], type='breakdown',
#                                                          c_name=kwargs['c_name'], insert=True)
#                             if save_obj:break;
#                         if kwargs['pdf_type'] == 'year':
#                             save_obj = save_year_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
#                                                       pdf_obj=pdf_val,
#                                                       d_obj=kwargs['db_key_list'][loop],
#                                                       type='breakdown', c_name=kwargs['c_name'])
#                         else:
#                             save_obj = save_qtr_data(year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
#                                                      pdf_obj=pdf_val,
#                                                      d_obj=kwargs['db_key_list'][loop], type='breakdown',
#                                                      c_name=kwargs['c_name'])
#                         break;
#             if save_obj:
#                 return True
#                 break;
#         else:
#             pass
#     except Exception as e:
#         return e
#
# def save_qtr_data(**kwargs):
#     try:
#         for i, j in enumerate(kwargs['pdf_obj']):
#             q_key = get_quarter_name(j[0],kwargs['year_end'])#'q' + str(i + 1)
#             if q_key:
#                 if 'section' not in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj'] :
#                     sec_item =kwargs['d_obj']['item'].split('##')[-1]
#                     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section__item= sec_item,
#                                                      subsection_id=None
#                                                      )
#                 elif 'section' in  kwargs['d_obj'] and 'subsection' not in  kwargs['d_obj']:
#                     sub_item = kwargs['d_obj']['item'].split('##')[-1]
#                     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],subsection__item= sub_item)
#                 # else:
#                 #     gbc_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'],section_id= kwargs['d_obj']['subsection__section'],
#                 #                                      subsection_id= kwargs['d_obj']['subsection'],s2section__item= kwargs['d_obj']['item'])
#
#                 if gbc_obj and kwargs['type']=='synonym':
#                     get_id = q_key + '_id'
#                     q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
#                     description = q_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if q_obj[
#                         0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
#                     if kwargs['comp'] =='total assets':
#                         old_obj = CompanyPNLData.objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
#                                                subsection_id=None)
#                         old_q_obj = quarter_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
#                         new_val = str(int(j[1]) - int(old_q_obj[0].q1))
#                         q_dict = {'q1':new_val}
#                     else:
#                         q_dict = {'q1': ('0' if str(j[1]) in ['-', '—'] else str(j[1])),
#                                   'description': description} if not 'insert' in kwargs else {'description': description}
#                     q_obj.update(**q_dict)
#
#                 elif gbc_obj and kwargs['type']=='breakdown':
#                     get_id = q_key + '_id'
#                     q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
#                     if q_obj:
#                         if kwargs['comp'] not in q_obj[0].description.split(','):
#                             if '(' in j[1] or '(' in q_obj[0].q1:
#                                 i2 = int(j[1].replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
#                                 i1 = int(q_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
#                                 val = i1 + i2
#                                 val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
#                             else:
#                                 val = int(q_obj[0].q1.replace(',', ''))+int(('0' if j[1] in ['-','—'] else j[1]).replace(',', ''))
#                             description = q_obj[0].description +'##'+kwargs['comp']+'('+ str(j[1])+')' if q_obj[0].description else kwargs['comp']+'('+ str(j[1])+')'
#                             q_dict = {'q1': val,'description':description}
#                             q_obj.update(**q_dict)
#                         else:
#                             pass
#         return True
#     except Exception as e:
#         return e

# def get_new_data(data,c_name,t_pdf,year_end):
#     try:
#         data_list = list(data.values())
#         d_val = data_list[0]
#         try:
#             year_list,val = map(list,zip(*d_val))
#             for year in year_list:
#                 if t_pdf == 'year':
#                     y_key = get_year_name(year,year_end)
#                     y1_key = y_key +'__q1'
#                 else:
#                     y_key = get_quarter_name(year,year_end)
#                     y1_key = y_key + '__q1'
#                 if y_key:
#                     year_exist = CompanyPNLData.objects.filter(gbc_name__company_name=c_name).filter(~Q(**{y_key:None}),~Q(**{y1_key:'0'}))
#                     # year_exist= year_data.objects.filter(year_date=year)
#                     if year_exist :
#                         for i in data:
#                             if type(data[i])==OrderedDict:
#                                 for dict1 in data[i]:
#                                     old_dict = dict(data[i][dict1])
#                                     if year in old_dict: del (old_dict[year])
#                                     data[i][dict1] = [(i, j) for i, j in old_dict.items()]
#                             else:
#                                 old_dict = dict(data[i])
#                                 if year in old_dict:del(old_dict[year])
#                                 data[i] = list(zip(list(old_dict.keys()), list(old_dict.values())))
#
#             return data
#                     # print (data_list)
#         except:
#             d_val = list(data_list[0].values())[0]
#             year_list, val = map(list, zip(*d_val))
#             for year in year_list:
#                 if t_pdf == 'year':
#                     y_key = get_year_name(year, year_end)
#                     y1_key = y_key + '__q1'
#                 else:
#                     y_key = get_quarter_name(year, year_end)
#                     y1_key = y_key + '__q1'
#                 if y_key :
#                     year_exist = CompanyPNLData.objects.filter(gbc_name__company_name=c_name).filter(
#                         ~Q(**{y_key: None}), ~Q(**{y1_key: '0'}))
#                     # year_exist= year_data.objects.filter(year_date=year)
#                     if year_exist:
#                         for i in data_list:
#                             for dict1 in i:
#                                 old_dict = dict(i[dict1])
#                                 if year in old_dict: del (old_dict[year])
#                                 i[dict1] = [(i, j) for i, j in old_dict.items()]
#             return data
#             # if year_exist :
#             #     for i in data_list:
#             #         for dict1 in i:
#             #             old_dict = dict(i[dict1])
#             #             if year in old_dict:del(old_dict[year])
#             #             i[dict1] = [(i,j) for i,j in old_dict.items()]
#
#
#     except Exception as e:
#         return e
#
#
# # def redefined_data(**kwargs):
# #     try:
# #         sub_obj = SubSection.objects.filter(item=kwargs['d_obj']['item'].split('##')[-1])
# #         if sub_obj and (sub_obj[0].is_expense or sub_obj[0].neg_ro):
# #             year_list, val = map(list, zip(*kwargs['pdf_obj']))
# #             # val_list = any(i.isdigit() for i in val)
# #             new_val = list(map(lambda x1: str(-int(x1)) if any(i.isdigit() for i in x1) else x1, val))
# #             new_data = list(zip(year_list,new_val))
# #             return new_data
# #         elif sub_obj and sub_obj[0].is_income :
# #             new_list = []
# #             year_list, val = map(list, zip(*kwargs['pdf_obj']))
# #             for i,j in enumerate(val) :
# #                 if any(i_d.isdigit() for i_d in j) and int(j) > 0:
# #                     new_list.append('0')
# #                 else:
# #                     new_list.append(j)
# #                     val[i]='0'
# #             if any(i!= '0' for i in new_list ):
# #                 new_data = list(zip(year_list,new_list))
# #                 other_obj = SubSection.objects.filter(item__icontains='Income with negative value')
# #                 other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]
# #                 save_year_data(year_end=kwargs['year_end'], comp=kwargs['comp'], pdf_obj=new_data,
# #                                d_obj=other_obj, type=kwargs['type'], c_name=kwargs['c_name'])
# #
# #                 # save_year_data(year_end=kwargs['year_end'], comp=kwargs['keyword'],
# #                 #                pdf_obj=kwargs['data'], d_obj=other_obj, type=kwargs['type'],
# #                 #                c_name=kwargs['c_name'])
# #             return list(zip(year_list,val))
# #         else:
# #             return kwargs['pdf_obj']
# #     except Exception as e:
# #         return e
# #
