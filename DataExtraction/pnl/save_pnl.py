from DataExtraction.models import *
from DataExtraction.mapping_data import keywords_relation
from DataExtraction.common_functions import *
synonym_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
similar_keyword_re = '[A-Za-z0-9. - ]*%s[ ,A-Za-z0-9.-]*$'

def save_pnl(**kwargs):
    import pdb;pdb.set_trace()
    found = False
    print (kwargs['data'])
    for keyword in kwargs['data']:
        print (keyword)
        pnl_dict = keywords_relation.pnl_map_dict
        img_path = save_image(kwargs['path'], kwargs['page'], kwargs['company_name'])
        import pdb;pdb.set_trace()
        obj = match_keyword(keyword,pnl_dict, img_path,data=kwargs['data'], page= kwargs['page'], c_name=kwargs['company_name'])
        if not obj:
            if 'expense' in keyword.lower():
                other_exp_obj =SubSection.objects.filter(item__icontains='Other Operating Expense')
                save_obj = save_data(obj=keyword,
                                     key_obj=kwargs['data'][keyword],
                                     path=img_path,
                                     page=kwargs['page'],
                                     id=other_exp_obj.id,
                                     sec_id=other_exp_obj.section,
                                     item=other_exp_obj.item,
                                     sec='pnl_dict',
                                     type='breakdown', c_name=kwargs['c_name'])
                print ("expense")
                break;
            elif 'income' in keyword.lower():
                other_inco_obj = SubSection.objects.filter(item__icontains='Other Operating Income')
                save_obj = save_data(obj=keyword,
                                     key_obj=kwargs['data'][keyword],
                                     path=img_path,
                                     page=kwargs['page'],
                                     id=other_inco_obj.id,
                                     sec_id=other_inco_obj.section,
                                     item=other_inco_obj.item,
                                     sec='pnl_dict',
                                     type='breakdown', c_name=kwargs['c_name'])
                print ("income")

def match_keyword(keyword,pnl_dict,img_path,**kwargs):
    for s1_counter, c_rel in enumerate(pnl_dict):
        save_obj = False
        found=False
        for synonym in c_rel['i_synonyms'].split('##'):
            scomp_list = map(lambda x: " ".join(re.findall("[a-zA-Z]+", x)), synonym.strip().lower().split())
            c_list = map(lambda x: " ".join(re.findall("[a-zA-Z]+", x)), keyword.strip().lower().split())
            if set(filter(lambda x: x.isalpha(), scomp_list)) == set(
                    filter(lambda x: x.isalpha(), c_list)) or keyword.strip().lower() == (
                    synonym.strip().lower()[:-1] if synonym.strip()[-1] == 's' else synonym.strip().lower()):
                if 'insert' in c_rel:
                    found = True
                    save_obj = True
                    break;
                c_rel['insert'] = True
                found = True
                save_obj = save_data(obj=keyword,
                                     key_obj=kwargs['data'][keyword],
                                     path=img_path,
                                     page=kwargs['page'],
                                     id=pnl_dict[s1_counter]['id'],
                                     sec_id=pnl_dict[s1_counter]['section'],
                                     item=pnl_dict[s1_counter]['item'],
                                     sec='pnl_dict',
                                     type='synonym', c_name=kwargs['c_name'])

                break;

        if found != True and c_rel['i_breakdown']:
            for breakdown in c_rel['i_breakdown'].split('##'):
                sim_key = similar_keyword_re % (
                    get_aplha(breakdown.strip().lower()[:-1].replace('-', '')) if breakdown.strip()[
                                                                           -1] == 's' else get_aplha(breakdown.strip().lower().replace(
                        '-', '')))
                re_obj = re.compile(sim_key, re.I)
                if re_obj.match(get_aplha(keyword)):
                    if 'insert' in c_rel:
                        found = True
                        save_obj = True
                        break;
                    found = True

                    save_obj = save_data(obj=keyword,
                                         key_obj=kwargs['data'][keyword],
                                         path=img_path,
                                         page=kwargs['page'],
                                         id=pnl_dict[s1_counter]['id'],
                                         sec_id=pnl_dict[s1_counter]['section'],
                                         item=pnl_dict[s1_counter]['item'],
                                         sec='pnl_dict',
                                         type='breakdown', c_name=kwargs['c_name'])

                    break;
        if found != True and c_rel['i_keyword']:
            for key in c_rel['i_keyword'].split(','):
                sim_key = similar_keyword_re % (
                    get_aplha(key.strip().lower()[:-1]) if key.strip()[-1] == 's' else get_aplha(key.strip().lower()))
                re_obj = re.compile(sim_key, re.I)
                if re_obj.match(get_aplha(keyword)):
                    if 'insert' in c_rel:
                        found = True
                        save_obj = True
                        break;
                    found = True

                    save_obj = save_data(obj=keyword,
                                         key_obj=kwargs['data'][keyword],
                                         path=img_path,
                                         page=kwargs['page'],
                                         id=pnl_dict[s1_counter]['id'],
                                         sec_id=pnl_dict[s1_counter]['section'],
                                         item=pnl_dict[s1_counter]['item'],
                                         sec='pnl_dict',
                                         type='breakdown', c_name=kwargs['c_name'])
                    break;



        if save_obj:
            return True
            break;

    return False


def save_data(**kwargs):
    import pdb;pdb.set_trace()
    c_obj = CompanyList.objects.filter(company_name__icontains=kwargs['c_name'])
    if not c_obj:
        c_dict = {'company_name':kwargs['c_name']}
        c_obj=CompanyList(**c_dict)
        c_obj.save()
    else:
        c_obj=c_obj[0]

    for i, j in enumerate(kwargs['key_obj']):
        y_key = get_year_name(j[0])
        if y_key:
            gbc_obj = GbcData.objects.filter(gbc_name=c_obj, section_id=kwargs['sec_id'], subsection__item=kwargs['item'])
            if gbc_obj and type == 'synonym':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if y_obj:
                    y_dict = {'y1': j[1]}
                    y_obj.update(**y_dict)
                    y_obj.update(**y_dict)
                else:
                    key_dict = {'description': kwargs['obj'], 'year_date': j[0], 'y1': j[1], 'pdf_page': kwargs['page'],
                                'pdf_image_path': kwargs['path']}
                    query1 = year_data(**key_dict)
                    query1.save()
                    gbc_dict = {y_key: query1.id}
                    gbc_obj.update(**gbc_dict)

            elif gbc_obj and type == 'breakdown':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if y_obj:
                    if kwargs['obj'] not in y_obj[0].description.split(','):
                        if '(' in j[1] or '(' in y_obj[0].y1:
                            i2 = j[1].replace(',', '')
                            i2 = i2.replace('(', '')
                            i2 = i2.replace(')', '')
                            i1 = y_obj[0].y1.replace(',', '')
                            i1 = i1.replace('(', '')
                            i1 = i1.replace(')', '')
                            val = int(i1) - int(i2)
                            val = abs(val) if int(i1) < int(i2) else '(' + str(val) + ')'
                        else:
                            val = int(''.join(x for x in y_obj[0].y1 if x.isdigit())) + int(
                                ''.join(x for x in j[1] if x.isdigit()))
                        description = y_obj[0].description + ',' + kwargs['obj']
                        y_dict = {'y1': val, 'description': description}
                        y_obj.update(**y_dict)
                    else:
                        pass
                else:
                    key_dict = {'description': kwargs['obj'], 'year_date': j[0], 'y1': j[1], 'pdf_page': kwargs['page'],
                                'pdf_image_path': kwargs['path']}
                    query1 = year_data(**key_dict)
                    query1.save()
                    gbc_dict = {y_key: query1.id}
                    gbc_obj.update(**gbc_dict)
            else:
                key_dict = {'description': kwargs['obj'], 'year_date': j[0], 'y1': j[1], 'pdf_page': kwargs['page'],
                            'pdf_image_path': kwargs['path']}
                query1 = year_data(**key_dict)
                query1.save()

                gbc_dict = {'gbc_name': c_obj, 'section_id': kwargs['sec_id'], 'subsection_id': kwargs['id'], y_key: query1}

                gbc = GbcData(**gbc_dict)
                gbc.save()
    return True
