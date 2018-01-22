from .models import *
from .mapping_data import keywords_relation
from .common_functions import *
import copy
import re
from django.db.models import Q
from django.forms.models import model_to_dict

synonym_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
similar_keyword_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
extended_key = '%s[ ,A-Za-z0-9.-]*$'
d_keywords =['less','deduction','depreciation','amortization','impairment']
equity_key_list =list(map(lambda x: get_aplha(x), ['shareholders-equity', 'stockholders-equity',"stockholders' equity","shareholders' equity"]))

def match_keyword(data,img_path,page=None,company_name='',new_dict=False):
    if new_dict:
        data = get_new_data(data,company_name)
    for keyword in data:
        if keyword =='current assets':
            c_asset=  copy.deepcopy(keywords_relation.c_asset)

            for comp in data[keyword]:
                print (comp)
                if 'total' not in comp.lower():
                    obj_save=place_keyword(comp,data[keyword],c_asset,img_path,page,c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.filter(item='Other Current Assets Deduction')
                            other_obj=list(other_obj.values('i_synonyms','i_breakdown','i_keyword','item','section','id'))[0]
                        else:
                            other_obj = S2Section.objects.filter(item='Other Current Assets (not listed above)')
                            other_obj=list(other_obj.values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id'))[0]
                        save_obj = save_data(comp, data[keyword][comp], other_obj, type='breakdown',
                                             c_name=company_name)
                else:
                    other_obj = Section.objects.get(id=1)
                    save_obj = save_data(comp, data[keyword][comp], model_to_dict(other_obj), type='synonym',
                                         c_name=company_name)

        elif keyword == 'non current assets':
            nc_asset = copy.deepcopy(keywords_relation.nc_asset)
            # img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], nc_asset, img_path, page, c_name=company_name)
                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.filter(item='Other Non-Current Assets Deduction')

                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                                         'id'))[0]
                        else:
                            other_obj = S2Section.objects.filter(item='Other Non-Current Assets (not listed above)')
                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'subsection',
                                                         'subsection__section', 'id'))[0]
                        save_obj = save_data(comp, data[keyword][comp], other_obj, type='breakdown',
                                             c_name=company_name)
                else:
                    other_obj = Section.objects.get(id=2)
                    save_obj = save_data(comp, data[keyword][comp], model_to_dict(other_obj), type='synonym',
                                         c_name=company_name)

        elif keyword == 'current liabilities':
            c_lib = copy.deepcopy(keywords_relation.c_lib)
            # img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], c_lib, img_path, page, c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.filter(item='Other Current Liabilities Deduction')
                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                             'id'))[0]
                        else:
                            other_obj = S2Section.objects.filter(item='Other Current Liabilities (not listed above)')
                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'subsection',
                                                         'subsection__section', 'id'))[0]
                        save_obj = save_data(comp, data[keyword][comp], other_obj, type='breakdown',
                                             c_name=company_name)
                else:
                    other_obj = Section.objects.get(id=3)
                    save_obj = save_data(comp, data[keyword][comp], model_to_dict(other_obj), type='synonym',
                                         c_name=company_name)

        elif keyword == 'non current liabilities':
            nc_lib = copy.deepcopy(keywords_relation.nc_lib)
            # img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                # import pdb;pdb.set_trace()
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], nc_lib, img_path, page, c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.filter(item='Other Non-Current Liabilities Deduction')
                            other_obj=list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                             'id'))[0]
                        else:
                            other_obj = S2Section.objects.filter(item='Other Non-Current Liabilities (not listed above)')
                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'subsection',
                                                         'subsection__section', 'id'))[0]
                        save_obj = save_data(comp, data[keyword][comp], other_obj, type='breakdown',
                                             c_name=company_name)
                else:
                    other_obj = Section.objects.get(id=4)
                    save_obj = save_data(comp, data[keyword][comp], model_to_dict(other_obj), type='synonym',
                                         c_name=company_name)

        elif keyword.lower() in equity_key_list :
            c_lib = copy.deepcopy(keywords_relation.equity_map_dict)
            # img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                # import pdb;pdb.set_trace()
                if 'total' not in comp.lower():
                    obj_save = place_keyword(comp, data[keyword], c_lib, img_path, page, c_name=company_name)
                    # other_obj = SubSection.objects.filter(item='Other Equity')
                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.filter(item='Other Equity Deduction')
                            other_obj =list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                             'id'))[0]
                        else:
                            other_obj = SubSection.objects.filter(item='Other Equity')
                            other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section',
                                                         'id'))[0]
                        save_obj = save_data(comp, data[keyword][comp], other_obj, type='breakdown',
                                             c_name=company_name)
                else:
                    other_obj = Section.objects.get(id=5)
                    save_obj = save_data(comp, data[keyword][comp], model_to_dict(other_obj), type='synonym',
                                         c_name=company_name)


    print (keyword)




def place_keyword(comp,data_dict,s1sec,img_path,page,c_name):
    found=False
    for s1_counter,c_rel in enumerate(s1sec):
        save_obj=False
        for synonym in c_rel['i_synonyms'].split('##'):
            scomp_list = get_aplha(synonym).split()
            c_list = get_aplha(comp).split()
            if  set(filter(lambda x:x.isalpha() , scomp_list))== set(filter(lambda x:x.isalpha() , c_list)) or comp.strip().lower()== (synonym.strip().lower()[:-1] if synonym.strip()[-1] == 's' else synonym.strip().lower()) :
                if 'insert' in c_rel :
                    found=True
                    save_obj=True
                    break;
                c_rel['insert']=True
                found=True
                save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter],type='synonym', c_name=c_name)
                break;

        if found!=True and c_rel['i_breakdown']:
            for breakdown in c_rel['i_breakdown'].split('##'):
                sim_key = similar_keyword_re %(breakdown.strip().lower()[:-1].replace('-','') if breakdown.strip()[-1] == 's' else breakdown.strip().lower().replace('-',''))
                key_2 = extended_key % (breakdown.strip().lower()[:-1].replace('-', '') if breakdown.strip()[
                                                                                               -1] == 's' else breakdown.strip().lower().replace(
                    '-', ''))
                re_obj = re.compile(sim_key, re.I)
                re_obj2 = re.compile(key_2, re.I)
                if re_obj.match(comp.replace('-', '')) or re_obj2.match(comp.replace('-', '')):
                    if 'insert' in c_rel:
                        found=True
                        save_obj=True
                        break;
                    found=True
                    save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter], type='breakdown', c_name=c_name)

                    break;
        if found!=True and c_rel['i_keyword']:
            for key in c_rel['i_keyword'].split(','):
                sim_key = similar_keyword_re %(key.strip().lower()[:-1] if key.strip()[-1] == 's' else key.strip().lower())
                key_2 = extended_key % (key.strip().lower()[:-1].replace('-', '') if key.strip()[
                                                                                               -1] == 's' else key.strip().lower().replace(
                    '-', ''))
                re_obj = re.compile(sim_key, re.I)
                re_obj2 = re.compile(key_2, re.I)
                if re_obj.match(comp.replace('-', '')) or re_obj2.match(comp.replace('-', '')):
                    if 'insert' in c_rel:
                        found=True
                        save_obj = True
                        break;
                    found=True
                    save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter], type='breakdown', c_name=c_name)

                    break;
        if found!=True :
            break_comp=comp.split(',')
            count=0
            for key in c_rel['i_synonyms'].split('##'):
                for b_comp in break_comp:
                    sim_key = synonym_re % (key.strip().lower()[:-1] if key.strip()[-1] == 's' else key.strip().lower())
                    key_2 = extended_key % (key.strip().lower()[:-1].replace('-', '') if key.strip()[
                                                                                             -1] == 's' else key.strip().lower().replace(
                        '-', ''))
                    re_obj = re.compile(sim_key, re.I)
                    re_obj2 = re.compile(key_2, re.I)
                    if re_obj.match(b_comp.replace('-', '')) or re_obj2.match(b_comp.replace('-', '')):
                        if 'insert' in c_rel:
                            found = True
                            save_obj = True
                            break;
                        found = True
                        c_rel['insert']=True
                        save_obj = save_data(comp, data_dict[comp], s1sec[s1_counter], type='breakdown', c_name=c_name)

                        break;
        if save_obj:
            return True
            break;

    else:
        print ("this key already inserted")

    return False


def save_data(obj_name,obj_val,obj_dict,type,c_name):
    print (obj_name)
    for i, j in enumerate(obj_val):
        y_key = get_year_name(j[0])
        if y_key:
            if 'section' not in obj_dict and 'subsection' not in obj_dict :
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=c_name,section__item=obj_dict['item'],
                                                 subsection_id=None
                                                 )
            elif 'section' in obj_dict and 'subsection' not in obj_dict:
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=c_name,section_id=obj_dict['section'],
                                                 subsection__item=obj_dict['item'])
            else:
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=c_name,section_id=obj_dict['subsection__section'],
                                                 subsection_id=obj_dict['subsection'],s2section__item=obj_dict['item'])

            if gbc_obj and type=='synonym':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if obj_name =='total assets':
                    old_obj = GbcData.objects.filter(gbc_name__company_name=c_name, section__id=1,
                                           subsection_id=None)
                    old_y_obj = year_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(int(j[1]) - int(old_y_obj[0].y1))
                    y_dict = {'y1':new_val}
                else:
                    y_dict = {'y1':('0' if j[1] in ['-','—'] else j[1])}
                y_obj.update(**y_dict)

            elif gbc_obj and type=='breakdown':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if y_obj:
                    if obj_name not in y_obj[0].description.split(','):
                        if '(' in j[1] or '(' in y_obj[0].y1:
                            i2 = int(j[1].replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = int(y_obj[0].y1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            val = int(y_obj[0].y1.replace(',', ''))+int(('0' if j[1] in ['-','—'] else j[1]).replace(',', ''))
                        description = y_obj[0].description +'##'+obj_name+'('+ str(j[1])+')' if y_obj[0].description else obj_name+'('+ str(j[1])+')'
                        y_dict = {'y1': val,'description':description}
                        y_obj.update(**y_dict)
                    else:
                        pass
    return True

def get_new_data(data,c_name):
    data_list = list(data.values())
    d_val = list(data_list[0].values())[0]
    y_list,val = map(list,zip(*d_val))
    for year in y_list:
        y_key = get_year_name(year)
        y_key = y_key +'__y1'
        qtr_exist = GbcData.objects.filter(gbc_name__company_name=c_name).filter(~Q(**{y_key: '0'}))
        if qtr_exist :
            for i in data_list:
                print (i)
                for dict1 in i:
                    old_dict = dict(i[dict1])
                    del(old_dict[year])
                    i[dict1] = [(i,j) for i,j in old_dict.items()]
    return data

