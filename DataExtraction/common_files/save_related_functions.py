
from BalanceSheet.models import *
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *
import copy
import re
from django.db.models import Q
from DataExtraction.common_files.mapping_data import bs_objs,mapping_dict
from DataExtraction.common_files.all_regex import *
from django.forms.models import model_to_dict
from PNL.models import *


def check_spl(str1):
    l1 = ['-', '—','Ã¢ÂÂ', 'â', '—']
    if str1 in l1 or str1 =='—':
        return str(0)
    else:
        return str(str1)

def save_data(**kwargs):
    try:
        if type(kwargs['pdf_obj'])==OrderedDict:# or  all(type(i)==tuple for i in kwargs['pdf_obj']):# (len(kwargs['pdf_obj'])==2 and type(kwargs['pdf_obj'][0][1])==list):
            for loop_obj in kwargs['pdf_obj']:
                save_data_p2(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=loop_obj, pdf_obj=kwargs['pdf_obj'][loop_obj],
                                                 d_obj=kwargs['d_obj'], type='breakdown',
                                                 c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])


        elif kwargs['pdf_obj'] and all(type(kwargs['pdf_obj'][num][1]) == list for num, i in enumerate(kwargs['pdf_obj'])):
            n_dict = OrderedDict({i[0]: kwargs['pdf_obj'][num][1] for num, i in enumerate(kwargs['pdf_obj'])})
            kwargs['pdf_obj'] = n_dict
            for loop_obj in kwargs['pdf_obj']:
                save_data_p2(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=loop_obj, pdf_obj=kwargs['pdf_obj'][loop_obj],
                                                 d_obj=kwargs['d_obj'], type='breakdown',
                                                 c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])


        else:
            save_data_p2(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['comp'], pdf_obj=kwargs['pdf_obj'],
                                                 d_obj=kwargs['d_obj'], type=kwargs['type'],
                                                 c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])


        return True
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        print("error hai save function me"+kwargs['c_name'])
        return e

def save_data_p2(**kwargs):
    for i, j in enumerate(kwargs['pdf_obj']):
        p_extraction = 'bsheet' if kwargs['p_type']!='pnl' else 'pnl'
        yq_key = valid_yq_name(j[0], kwargs['year_end'], pdf_type=kwargs['pdf_type'], p_type=kwargs['p_type'])
        if yq_key:
            if 'section' not in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj']:
                sec_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'],
                                                         section__item=sec_item,
                                                         subsection_id=None,page_extraction = p_extraction
                                                         )
            elif 'section' in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj']:
                sub_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'],
                                                         subsection__item=sub_item,page_extraction = p_extraction)
            else:
                gbc_obj = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'],
                                                         section_id=kwargs['d_obj']['subsection__section'],
                                                         subsection_id=kwargs['d_obj']['subsection'],
                                                         s2section__item=kwargs['d_obj']['item'],page_extraction = p_extraction)

            if gbc_obj and kwargs['type'] == 'synonym':
                # get_id = yq_key + '_id'
                val_obj = gbc_obj.filter(quarter_date = yq_key)#quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                description = get_description(val_obj[0],kwargs['comp'],j[1])#val_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if val_obj[
                    #0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                if kwargs['comp'] == 'total assets':
                    old_obj = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'], section__id=1,
                                                             subsection_id=None)
                    old_y_obj = old_obj.filter(quarter_date = yq_key)#quarter_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(get_digit(j[1]) - get_digit(old_y_obj[0]))
                    val_dict = {'q1': new_val}
                else:
                    val_dict = {'q1':  check_spl(str(j[1])),
                                'description': description} if not 'insert' in kwargs else {'description': description}
                val_obj.update(**val_dict)
            elif gbc_obj and kwargs['type'] == 'breakdown':
                # get_id = yq_key + '_id'
                val_obj = gbc_obj.filter(quarter_date = yq_key)#quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if val_obj:
                    if kwargs['comp'] not in val_obj[0].description.split(','):
                        if '(' in str(j[1]) or '(' in val_obj[0].q1:
                            i2 = get_digit(str(j[1]).replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = get_digit(val_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            try:
                                val = val = get_digit(val_obj[0].q1.replace(',', '')) + get_digit(check_spl(str(j[1])).replace(',', ''))
                            except:
                                print (val_obj)

                        description =  get_description(val_obj[0],kwargs['comp'],j[1])# val_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if val_obj[
                            #0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                        val_dict = {'q1': val, 'description': description} if not 'insert' in kwargs else {
                            'description': description}
                        val_obj.update(**val_dict)
                    else:
                        pass


def get_description(obj,comp,val):
    des_list = obj.description.split('##')
    exist = [i for i in des_list if comp == i.split('(')[0]]
    if exist:
        add_des = str(comp) + '(' + str(val) + ')'
        des_list[des_list.index(exist[0])]=add_des
        des = '##'.join(des_list)
        return des

    else:
        des = obj.description + '##' + comp + '(' + str(val) + ')' if obj.description else comp + '(' + str(val) + ')'

    return des

def get_new_data(**kwargs):#data,c_name,t_pdf,year_end):
    p_extraction = 'bsheet' if kwargs['p_type'] != 'pnl' else 'pnl'
    try:
        data_list = list(kwargs['data'].values())
        try:
            d_val = data_list[0]
            year_list, val = map(list, zip(*d_val))
        except:
            d_val = list(data_list[0].values())[0]
            year_list, val = map(list, zip(*d_val))
        # year_list,val = map(list,zip(*d_val))
        for year in year_list:
            y_key = valid_yq_name(year,kwargs['year_end'],pdf_type = kwargs['t_pdf'],p_type = kwargs['p_type'])
            if y_key and str(y_key) not in kwargs['override']:
                # y1_key = y_key
                year_exist = quarter_data.objects.filter(Q(company_name__company_name=kwargs['c_name']), Q(quarter_date=y_key),~Q(q1=0), Q(page_extraction=p_extraction))
                if year_exist :
                    for i in kwargs['data']:
                        if type(kwargs['data'][i]) == OrderedDict:
                            for dict1 in kwargs['data'][i]:
                                old_dict = dict(kwargs['data'][i][dict1])
                                if year in old_dict: del (old_dict[year])
                                kwargs['data'][i][dict1] = [(k2, k1) for k2, k1 in old_dict.items()]
                        else:
                            old_dict = dict(kwargs['data'][i])
                            if year in old_dict: del (old_dict[year])
                            kwargs['data'][i] = list(zip(list(old_dict.keys()), list(old_dict.values())))
            elif y_key and str(y_key) in kwargs['override']:
                get_y_obj = quarter_data.objects.filter(Q(company_name__company_name=kwargs['c_name']), Q(quarter_date=y_key),~Q(q1=0), Q(page_extraction=p_extraction))
                for obj in get_y_obj:
                    obj.q1 = 0
                    obj.description=''
                    obj.save()

        return kwargs['data']

    except Exception as e:
        return e

#for pnl only to seperate income and expense logic
def redefined_data(**kwargs):
    #try:
     #   sub_obj = SubSection.objects.filter(item=kwargs['d_obj']['item'].split('##')[-1])
      #  if sub_obj and (sub_obj[0].is_expense or sub_obj[0].neg_ro):
       #     year_list, val = map(list, zip(*kwargs['pdf_obj']))
        #    new_val = list(map(lambda x1: str(-get_digit(x1)) if any(i.isdigit() for i in x1) else x1, val))
         #   new_data = list(zip(year_list,new_val))
          #  return new_data
       # elif sub_obj and sub_obj[0].is_income :
        #    new_list = []
         #   year_list, val = map(list, zip(*kwargs['pdf_obj']))
          #  for i,j in enumerate(val) :
           #     if any(i_d.isdigit() for i_d in j) and get_digit(j) > 0:
            #        new_list.append('0')
             #   else:
              #      new_list.append(j)
               #     val[i]='0'
            #if any(i!= '0' for i in new_list ):
             #   new_data = list(zip(year_list,new_list))
              #  other_obj = SubSection.objects.filter(item__icontains='Income with negative value')
               # other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]
                #save_data(model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['comp'], pdf_obj=new_data,
                 #         p_type=kwargs['p_type'],d_obj=other_obj, type=kwargs['type'], c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])

           # return list(zip(year_list,val))
       # else:
	return kwargs['pdf_obj']
   # except Exception as e:
    #    import traceback
     #   print (traceback.format_exc())
      #  print("error hai redefined data me " + kwargs['c_name'])
       # return e

