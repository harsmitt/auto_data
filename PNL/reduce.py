def match_with_db(**kwargs):
    found = False
    for loop, db_obj in enumerate(kwargs['db_key_list']):
        save_obj = False
        for synonym in db_obj['i_synonyms'].split('##'):
            scomp_list = get_alpha(synonym).split()
            c_list = get_alpha(kwargs['pdf_obj']).split()
            if  set(filter(lambda x:x.isalpha() , scomp_list))== set(filter(lambda x:x.isalpha() , c_list)) or \
                            kwargs['pdf_obj'].strip().lower()== synonym.strip(' s').lower():
                if 'insert' in db_obj :
                    found,save_obj=True,True
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
            # found, save_obj = match(obj_split=db_obj['i_synonyms'].split('##'), p_obj=kwargs['obj'],
            #                         obj_dict=db_obj, img=kwargs['img_path'],
            #                         page=kwargs['page'], d_obj=kwargs['db_key_list'][loop])

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
                            break;
                        found = True
                        db_obj['insert'] = True
                        if kwargs['pdf_type']=='year':
                            save_obj = save_year_data(year_end= kwargs['year_end'],comp=kwargs['pdf_obj'], pdf_obj=kwargs['pdf_key_list'][kwargs['pdf_obj']],
                                                 d_obj=kwargs['db_key_list'][loop], type='breakdown', c_name=kwargs['c_name'])
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
                save_obj = True
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
