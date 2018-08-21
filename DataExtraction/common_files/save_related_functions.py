
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
from DataExtraction.logger_config import logger


#todo need to optimize the code.

def check_spl(str1):
    try:
        l1 = ['-', '—','Ã¢ÂÂ', 'â', '—']
        if str1 in l1 or str1 =='—':
            return str(0)
        else:
            return str(str1)
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in check special chars for :%s " %str(str1))
        return e

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
        logger.debug(traceback.format_exc())
        logger.debug("error for values %s " % str(kwargs['pdf_obj']))
        return e

def save_data_p2(**kwargs):
    try:
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
                                    val = get_digit(val_obj[0].q1.replace(',', '')) + get_digit(check_spl(str(j[1]).replace('–','0').replace(',', '')))
                                except Exception as e:
                                    import traceback
                                    print (traceback.format_exc())
                                    logger.debug(traceback.format_exc())
                                    logger.debug("error for values %s " % str(j[1]))
                                    return e

                            description =  get_description(val_obj[0],kwargs['comp'],j[1])# val_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if val_obj[
                                #0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                            val_dict = {'q1': val, 'description': description} if not 'insert' in kwargs else {
                                'description': description}
                            val_obj.update(**val_dict)
                        else:
                            pass
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for values: %s " %str(kwargs['pdf_obj']))
        return e


def get_description(obj,comp,val):
    try:
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
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in get description for : %s " %str(obj))
        return e

def get_new_data(**kwargs):#data,c_name,t_pdf,year_end):
    override = [key.replace('_',' ') for key in kwargs['override']]
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
            if y_key and str(y_key) not in override:
                # y1_key = y_key
                year_exist = quarter_data.objects.filter(Q(company_name__company_name=kwargs['c_name']), Q(quarter_date=y_key),~Q(q1=0), Q(page_extraction=p_extraction))
                if year_exist :
                    for i in kwargs['data']:
                        if type(kwargs['data'][i]) == OrderedDict:
                            for dict1 in kwargs['data'][i]:
                                if not type(kwargs['data'][i][dict1])==OrderedDict:
                                    if len(kwargs['data'][i][dict1])<2:
                                        kwargs['data'][i].pop(dict1)
                                    else:
                                        old_dict = dict(kwargs['data'][i][dict1])
                                        if year in old_dict: del (old_dict[year])
                                        kwargs['data'][i][dict1] = [(k2, k1) for k2, k1 in old_dict.items()]
                                else:
                                    for item1 in kwargs['data'][i][dict1]:
                                        for d_1, k1 in enumerate(kwargs['data'][i][dict1][item1]) :
                                            if type(k1) != tuple:
                                                kwargs['data'][i][dict1][item1].pop(d_1)

                                        if len(kwargs['data'][i][dict1][item1])<2 :
                                            kwargs['data'][i][dict1].pop(item1)
                                        else:
                                            old_dict = dict(kwargs['data'][i][dict1][item1])
                                            if year in old_dict: del (old_dict[year])
                                            kwargs['data'][i][dict1][item1] = [(k2, k1) for k2, k1 in old_dict.items()]
                        else:
                            old_dict = dict(kwargs['data'][i])
                            if year in old_dict: del (old_dict[year])
                            kwargs['data'][i] = list(zip(list(old_dict.keys()), list(old_dict.values())))
            elif y_key and str(y_key) in override:
                get_y_obj = quarter_data.objects.filter(Q(company_name__company_name=kwargs['c_name']), Q(quarter_date=y_key),~Q(q1=0), Q(page_extraction=p_extraction))
                for obj in get_y_obj:
                    obj.q1 = 0
                    obj.description=''
                    obj.save()

        return kwargs['data']


    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error for values: %s " % str(kwargs['data']))
        return e


def unit_conversion(**kwargs):
    try:
        c_obj = CompanyList.objects.filter(company_name=kwargs['c_name'])
        if c_obj:
            prev_unit = c_obj[0].c_y_unit.split('##') if c_obj[0].c_y_unit else ''
            if prev_unit:
                if not prev_unit:
                    ##todo yhan change krna hai
                    kwargs['unit'] = 'thousands'
                elif prev_unit[1] == kwargs['unit']:
                    return kwargs['data']
                else:
                    if kwargs['t_pdf'] != 'year' or int(prev_unit[0]) > max(
                            map(lambda x: int(x.split()[-1]), kwargs['date_obj'])) \
                            or (int(prev_unit[0]) < max(map(lambda x: int(x), kwargs['date_obj'])) and not kwargs[
                                'unit']):
                        print ("convert only data_dict into the stored unit")
                        for k1, k2 in kwargs['data'].items():
                            if type(k2) == OrderedDict:
                                for p1, p2 in k2.items():
                                    if kwargs['data'][k1][p1]:
                                        if type(kwargs['data'][k1][p1]) != OrderedDict:
                                            if kwargs['data'][k1][p1]:
                                                date_obj, values = map(list, zip(*kwargs['data'][k1][p1]))

                                                if prev_unit[1] == 'millions':
                                                    values = list(map(lambda x: str(get_digit(x)), values))
                                                    if kwargs['unit']:
                                                        val = [int(val) / 1000 if val.isdigit() else 0 for val in
                                                               values]
                                                    else:
                                                        val = [int(val) / 1000000 if val.isdigit() else 0 for val in
                                                               values]
                                                    kwargs['data'][k1][p1] = list(zip(date_obj, val))
                                                else:
                                                    values = list(map(lambda x: str(get_digit(x)), values))
                                                    if kwargs['unit']:
                                                        val = [int(val) * 1000 if val.isdigit() else 0 for val in
                                                               values]
                                                    else:
                                                        val = [int(val) / 1000 if val.isdigit() else 0 for val in
                                                               values]
                                                    kwargs['data'][k1][p1] = list(zip(date_obj, val))
                                        else:
                                            for p1_key, p1_val in kwargs['data'][k1][p1].items():
                                                if kwargs['data'][k1][p1][p1_key]:
                                                    date_obj, values = map(list, zip(*kwargs['data'][k1][p1][p1_key]))

                                                    if prev_unit[1] == 'millions':
                                                        values = list(map(lambda x: str(get_digit(x)), values))
                                                        if kwargs['unit']:
                                                            val = [int(val) / 1000 if val.isdigit() else 0 for val in
                                                                   values]
                                                        else:
                                                            val = [int(val) / 1000000 if val.isdigit() else 0 for val in
                                                                   values]
                                                        kwargs['data'][k1][p1][p1_key] = list(zip(date_obj, val))
                                                    else:
                                                        values = list(map(lambda x: str(get_digit(x)), values))
                                                        if kwargs['unit']:
                                                            val = [int(val) * 1000 if val.isdigit() else 0 for val in
                                                                   values]
                                                        else:
                                                            val = [int(val) / 1000 if val.isdigit() else 0 for val in
                                                                   values]
                                                        kwargs['data'][k1][p1][p1_key] = list(zip(date_obj, val))

                            else:
                                if kwargs['data'][k1]:
                                    date_obj, values = map(list, zip(*kwargs['data'][k1]))
                                    try:
                                        if prev_unit[1] == 'millions':
                                            values = list(map(lambda x: str(get_digit(x)), values))
                                            if kwargs['unit']:
                                                val = [int(val) / 1000 if val.isdigit() else 0 for val in values]
                                            else:
                                                val = [int(val) / 1000000 if val.isdigit() else 0 for val in values]
                                            kwargs['data'][k1] = list(zip(date_obj, val))
                                        else:
                                            values = list(map(lambda x: str(get_digit(x)), values))
                                            if kwargs['unit']:

                                                val = [int(val) * 1000 if val.isdigit() else 0 for val in values]
                                            else:
                                                val = [int(val) / 1000 if val.isdigit() else 0 for val in values]
                                            kwargs['data'][k1] = list(zip(date_obj, val))
                                    except:
                                        print("shi mil gya")
                        return kwargs['data']


                    elif kwargs['t_pdf'] == 'year' and int(prev_unit[0]) < max(
                            map(lambda x: int(x), kwargs['date_obj'])) and kwargs['unit']:
                        already_saved = quarter_data.objects.filter(Q(company_name_id=1), ~Q(q1=0)).values_list(
                            'quarter_date',
                            flat=True).distinct()
                        for saved_d in already_saved:
                            total_objs = quarter_data.objects.filter(company_name_id=1, quarter_date=saved_d)
                            for i in total_objs:
                                if kwargs['unit'] == 'millions':
                                    i.update(**{'q1': int(i.q1) / 1000})
                                    i.save()
                                else:
                                    i.update(**{'q1': int(i.q1) * 1000})
                                    i.save()

                        return kwargs['data']


            elif not prev_unit:
                f_name = max(map(lambda x: int(x.split()[-1]), kwargs['date_obj']))
                unit_val = str(f_name) + '##' + kwargs['unit']
                c_obj.update(**{'c_y_unit': unit_val})
                return kwargs['data']

        return kwargs['data']

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        logger.debug(traceback.format_exc())
        logger.debug("error in unit conversion for values %s " % str(kwargs['data']))
        return e