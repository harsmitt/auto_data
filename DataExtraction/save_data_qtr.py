from .models import *
from .mapping_data import keywords_relation
from .common_functions import *
import copy
import re
synonym_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
similar_keyword_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
extended_key = '%s[ ,A-Za-z0-9.-]*$'
d_keywords =['less','deduction','depreciation','amortization','impairment']
equity_key_list =list(map(lambda x: get_aplha(x), ['shareholders-equity', 'stockholders-equity',"stockholders' equity","shareholders' equity"]))

def match_keyword_qtr(data,path,page=None,company_name='',new_dict=False):
    if new_dict:
        data = get_new_data(data,company_name)

    for keyword in data:
        if keyword =='current assets':
            c_asset= copy.deepcopy(keywords_relation.c_asset)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:
                print (comp)
                if 'total' not in comp.lower():
                    obj_save=place_keyword(comp,data[keyword],c_asset,img_path,page,c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item='Other Current Assets Deduction')
                            save_data(comp, data[keyword][comp], img_path, page,
                                      other_obj.id,
                                      other_obj.section.id,other_obj.item,
                                      sec='s1sec',
                                      type='breakdown', c_name=company_name)
                        else:
                            other_obj = S2Section.objects.get(item='Other Current Assets (not listed above)')

                            save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                                 other_obj.subsection.section.id, other_obj.item,
                                                 sec='s1sec',
                                                 type='breakdown', c_name=company_name,
                                                 subsec=other_obj.subsection.id)
                else:
                    pass

        elif keyword == 'non current assets':
            nc_asset = copy.deepcopy(keywords_relation.nc_asset)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], nc_asset, img_path, page, c_name=company_name)
                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item='Other Non-Current Assets Deduction')
                            save_data(comp, data[keyword][comp], img_path, page,
                                      other_obj.id,
                                      other_obj.section.id, other_obj.item,
                                      sec='s1sec',
                                      type='breakdown', c_name=company_name)
                        else:
                            other_obj = S2Section.objects.get(item='Other Non-Current Assets (not listed above)')
                            save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                             other_obj.subsection.section.id, other_obj.item,
                                             sec='s1sec',
                                             type='breakdown', c_name=company_name,
                                             subsec=other_obj.subsection.id)
                else:
                    pass

        elif keyword == 'current liabilities':
            c_lib = copy.deepcopy(keywords_relation.c_lib)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], c_lib, img_path, page, c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item='Other Current Liabilities Deduction')
                            save_data(comp, data[keyword][comp], img_path, page,
                                      other_obj.id,
                                      other_obj.section.id, other_obj.item,
                                      sec='s1sec',
                                      type='breakdown', c_name=company_name)
                        else:
                            other_obj = S2Section.objects.get(item='Other Current Liabilities (not listed above)')
                            save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                             other_obj.subsection.section.id, other_obj.item,
                                             sec='s1sec',
                                             type='breakdown', c_name=company_name,
                                             subsec=other_obj.subsection.id)
                else:
                    pass

        elif keyword == 'non current liabilities':
            nc_lib = copy.deepcopy(keywords_relation.nc_lib)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                # import pdb;pdb.set_trace()
                if 'total' not in comp.lower():
                    obj_save= place_keyword(comp, data[keyword], nc_lib, img_path, page, c_name=company_name)

                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item='Other Non-Current Liabilities Deduction')
                            save_data(comp, data[keyword][comp], img_path, page,
                                      other_obj.id,
                                      other_obj.section.id, other_obj.item,
                                      sec='s1sec',
                                      type='breakdown', c_name=company_name)
                        else:
                            other_obj = S2Section.objects.get(item='Other Non-Current Liabilities (not listed above)')
                            save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                             other_obj.subsection.section.id, other_obj.item,
                                             sec='s1sec',
                                             type='breakdown', c_name=company_name,
                                             subsec=other_obj.subsection.id)
                else:
                    pass

        elif keyword.lower() in equity_key_list :
            c_lib = copy.deepcopy(keywords_relation.equity_map_dict)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
                # import pdb;pdb.set_trace()
                if 'total' not in comp.lower():
                    obj_save = place_keyword(comp, data[keyword], c_lib, img_path, page, c_name=company_name)
                    # other_obj = SubSection.objects.get(item='Other Equity')
                    if not obj_save:
                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item='Other Equity Deduction')
                        else:
                            other_obj = SubSection.objects.get(item='Other Equity')
                        save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                         other_obj.section.id, other_obj.item,
                                         sec='s1sec',
                                         type='breakdown', c_name=company_name)
                else:
                    pass


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
                if 'subsection' in s1sec[s1_counter]:
                    save_obj = save_data(comp, data_dict[comp], img_path, page, s1sec[s1_counter]['id'],
                                         s1sec[s1_counter]['subsection__section'], s1sec[s1_counter]['item'],
                                         sec='s1sec',
                                         type='synonym', c_name=c_name,
                                         subsec=s1sec[s1_counter]['subsection'])
                else:
                    save_obj = save_data(comp, data_dict[comp], img_path, page,
                                         s1sec[s1_counter]['id'],
                                         s1sec[s1_counter]['section'], s1sec[s1_counter]['item'],
                                         sec='s1sec',
                                         type='synonym', c_name=c_name)
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
                    if 'subsection' in s1sec[s1_counter]:
                        save_obj = save_data(comp, data_dict[comp], img_path, page, s1sec[s1_counter]['id'],
                                             s1sec[s1_counter]['subsection__section'],
                                             s1sec[s1_counter]['item'], sec='s1sec',
                                             type='breakdown', c_name=c_name,
                                             subsec=s1sec[s1_counter]['subsection'])
                    else:
                        save_obj = save_data(comp, data_dict[comp], img_path, page,
                                             s1sec[s1_counter]['id'],
                                             s1sec[s1_counter]['section'], s1sec[s1_counter]['item'],
                                             sec='s1sec',
                                             type='breakdown', c_name=c_name)
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
                    if 'subsection' in s1sec[s1_counter]:
                        save_obj = save_data(comp, data_dict[comp], img_path, page, s1sec[s1_counter]['id'],
                                             s1sec[s1_counter]['subsection__section'],
                                             s1sec[s1_counter]['item'], sec='s1sec',
                                             type='breakdown', c_name=c_name,
                                             subsec=s1sec[s1_counter]['subsection'])
                    else:
                        save_obj = save_data(comp, data_dict[comp], img_path, page,
                                             s1sec[s1_counter]['id'],
                                             s1sec[s1_counter]['section'], s1sec[s1_counter]['item'],
                                             sec='s1sec',
                                             type='breakdown', c_name=c_name)
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
                        if 'subsection' in s1sec[s1_counter]:
                            save_obj= save_data(comp, data_dict[comp], img_path, page, s1sec[s1_counter]['id'],
                                      s1sec[s1_counter]['subsection__section'], s1sec[s1_counter]['item'], sec='s1sec',
                                      type='breakdown', c_name=c_name,subsec=s1sec[s1_counter]['subsection'])
                        else:
                            save_obj = save_data(comp, data_dict[comp], img_path, page,
                                                 s1sec[s1_counter]['id'],
                                                 s1sec[s1_counter]['section'], s1sec[s1_counter]['item'],
                                                 sec='s1sec',
                                                 type='breakdown', c_name=c_name)
                        break;
        if save_obj:
            return True
            break;

    else:
        print ("this key already inserted")

    return False

def save_data(obj,key_obj,path,page,sub_id,f_obj,item,sec,type,c_name,subsec=''):
    print (obj)
    c_obj = CompanyList.objects.filter(company_name__icontains=c_name)
    if not c_obj:
        c_dict = {'company_name':c_name}
        c_obj=CompanyList(**c_dict)
        c_obj.save()
    else:
        c_obj=c_obj[0]
    for i, j in enumerate(key_obj):
        q_key = get_quarter_name(j[0])#'q' + str(i + 1)
        if q_key:
            if sec=='s1sec':
                if not subsec:
                    gbc_obj = GbcData.objects.filter(gbc_name=c_obj,section_id=f_obj,subsection__item=item)
                else:
                    gbc_obj = GbcData.objects.filter(gbc_name=c_obj,section_id=f_obj,subsection_id=subsec,s2section__item=item)

                if gbc_obj and type=='synonym':
                        get_id = q_key+'_id'
                        q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id,flat=True))
                        if q_obj:
                            q_dict = {'q1':('0' if j[1] in ['-','—'] else j[1])}
                            q_obj.update(**q_dict)
                        else:
                            key_dict = {'description': obj, 'quarter_date': j[0], 'q1': ('0' if j[1] in ['-','—'] else j[1]), 'pdf_page': page,
                                        'pdf_image_path': path}
                            query1 = quarter_data(**key_dict)
                            query1.save()
                            gbc_dict = {q_key: query1.id}
                            gbc_obj.update(**gbc_dict)

                elif gbc_obj and type=='breakdown':
                    get_id = q_key + '_id'
                    q_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                    if q_obj:
                        if obj not in q_obj[0].description.split(','):
                            if '(' in j[1] or '(' in q_obj[0].q1:
                                i2 = int(j[1].replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                                i1 = int(q_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                                val = i1 + i2
                                val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                            else:
                                val = int(q_obj[0].q1.replace(',', ''))+int(('0' if j[1] in ['-','—'] else j[1]).replace(',', ''))
                            description = q_obj[0].description +','+obj
                            q_dict = {'q1': val,'description':description}
                            q_obj.update(**q_dict)
                        else:
                            pass
                    else:
                        key_dict = {'description': obj, 'quarter_date': j[0], 'q1': ('0' if j[1] in ['-','—'] else j[1]), 'pdf_page': page,
                                    'pdf_image_path': path}
                        query1 = quarter_data(**key_dict)
                        query1.save()
                        gbc_dict = {q_key: query1.id}
                        gbc_obj.update(**gbc_dict)
                else:
                    key_dict = {'description':obj,'quarter_date': j[0], 'q1': ('0' if j[1] in ['-','—'] else j[1]),'pdf_page':page,'pdf_image_path':path}
                    query1 = quarter_data(**key_dict)
                    query1.save()
                    if not subsec:
                        gbc_dict = {'gbc_name': c_obj, 'section_id': f_obj,'subsection_id': sub_id, q_key: query1}
                    else:
                        gbc_dict = {'gbc_name': c_obj, 'section_id': f_obj, 's2section_id': sub_id,'subsection_id':subsec, q_key: query1}
                    gbc = GbcData(**gbc_dict)
                    gbc.save()
    return True

def get_new_data(data):
    data_list = list(data.values())
    d_val = list(data_list[0].values())[0]
    q_list,val = map(list,zip(*d_val))
    for qtr in q_list:
        qtr_exist= quarter_data.objects.filter(quarter_date=qtr)
        if qtr_exist :
            for i in data_list:
                print (i)
                for dict1 in i:
                    old_dict = dict(i[dict1])
                    del(old_dict[qtr])
                    i[dict1] = [(i,j) for i,j in old_dict.items()]
            print (data_list)
    return data