from DataExtraction.models import *
from .save_related_functions import *
from DataExtraction.logger_config import logger



def match_all_synonym_words(**kwargs):
    try:
        match_with = ''.join([word for word in  get_alpha(kwargs['match_with'],key=True,remove_s=True).split() if word not in stop_words])
        pdf_word = ''.join([word for word in get_alpha(kwargs['pdf_obj'], remove_s=True).split() if word not in stop_words])
        import itertools
        i_list = list(itertools.permutations(match_with.split(),len(match_with.split())))
        if any(' '.join(i)==pdf_word for i in i_list):
            return True
        else:
            False
    except Exception as e:
        import traceback
        logger.debug("error in for values %s " %kwargs)
        logger.debug(traceback.format_exc())
        return e

def match_synonym(**kwargs):
    try:
        for loop, db_obj in enumerate(kwargs['db_key_list']):
            save_obj = False
            break_comp = kwargs['pdf_obj'].strip().split(',')
            for key in [key for key in db_obj['i_synonyms'].strip().split('##')  if key]:
                for b_comp in break_comp:
                    sim_key = similar_keyword_re % (extract_s(key).strip().lower().replace('-',''))
                    key_2 = extended_key % (extract_s(key).strip().lower().replace('-',''))
                    re_obj = re.compile(sim_key, re.I)
                    re_obj2 = re.compile(key_2, re.I)
                    if re_obj.match(b_comp.replace('-', '')) or re_obj2.match(b_comp.replace('-', '')):
                        pdf_obj = kwargs['pdf_key_list'][kwargs['pdf_obj']]
                        if 'insert' in db_obj:
                            found, save_obj = True, True
                            save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                      pdf_obj=pdf_obj,pdf_type = kwargs['pdf_type'],
                                                      d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                      c_name=kwargs['c_name'], insert=True)

                            if save_obj:break;
                        save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                                      pdf_obj=pdf_obj,pdf_type = kwargs['pdf_type'],
                                                      d_obj=kwargs['db_key_list'][loop],
                                                      type='breakdown', c_name=kwargs['c_name'])

                        break;
            if save_obj:
                return True
                break;
        else:
            pass
    except Exception as e:
        import traceback
        logger.debug("error in match synonym %s " % e)
        logger.debug(traceback.format_exc())
        return e


def match_breakdown_words(**kwargs):
    try:
        match_with = ' '.join([word for word in get_alpha(kwargs['match_with'], key=True,remove_s=True).split() if word not in stop_words])
        pdf_word = ' '.join([word for word in get_alpha(kwargs['pdf_obj'], remove_s=True).split() if word not in stop_words])
        import itertools
        i_list = list(itertools.permutations(match_with.split(), len(match_with.split()))) if len(match_with.split())<=7 else \
                    list(match_with.split())
        i_list_words = [' '.join(i).strip().replace('-','') for i in i_list]
        for comb in i_list_words:
            if comb:
                sim_key = similar_keyword_re % comb
                key_2 = extended_key % comb
                re_obj = re.compile(sim_key, re.I)
                re_obj2 = re.compile(key_2, re.I)
                if re_obj.match(pdf_word.replace('-', '')) or re_obj2.match(pdf_word.replace('-', '')):
                    return True
                else:
                    return False
            else:
                pass
    except Exception as e:
        import traceback
        logger.debug("error in match breakdown permutations for values %s " % kwargs)
        logger.debug(traceback.format_exc())
        return e


def match_breakdown(**kwargs):
    try:
        found,save_obj =False,False
        for i_obj in [key for key in kwargs['obj_split']  if key]:
            if match_breakdown_words(match_with=i_obj,pdf_obj=kwargs['p_obj'].replace('-', '')):#re_obj.match(kwargs['p_obj'].replace('-', '')) or re_obj2.match(kwargs['p_obj'].replace('-', '')):

                pdf_obj = kwargs['pdf_key_list'][kwargs['p_obj']]
                if 'insert' in kwargs['obj_dict']:
                    found = True
                    save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['p_obj'],
                                          pdf_obj=pdf_obj,pdf_type = kwargs['pdf_type'],
                                          d_obj=kwargs['d_obj'], type='breakdown', c_name=kwargs['c_name'],insert=True)

                    if save_obj:break;
                found = True
                save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end = kwargs['year_end'],comp=kwargs['p_obj'], pdf_obj=pdf_obj,
                                     d_obj=kwargs['d_obj'], type='breakdown',pdf_type = kwargs['pdf_type'], c_name=kwargs['c_name'])

                if save_obj: break;
        return found,save_obj


    except Exception as e:
        import traceback
        logger.debug("error in match breakdown for values %s " % kwargs)
        logger.debug(traceback.format_exc())
        return e

def not_match(**kwargs):
    try:
        other_obj = SubSection.objects.filter(item__icontains=kwargs['other_key'])
        if not other_obj:
            other_obj = SubSection.objects.filter(item__icontains=kwargs['other_key'])

        other_obj = list(other_obj.values('i_synonyms', 'i_breakdown', 'i_keyword', 'item', 'section', 'id'))[0]
        if other_obj:
            save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], comp=kwargs['keyword'],
                                      pdf_obj=kwargs['data'], d_obj=other_obj, type=kwargs['type'],
                                      c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])

    except Exception as e:
        import traceback
        logger.debug("error for values %s " % kwargs)
        logger.debug(traceback.format_exc())
        return e

def match_with_db(**kwargs):
    try:
        found = False
        for loop, db_obj in enumerate(kwargs['db_key_list']):
            save_obj = False
            for synonym in [key for key in db_obj['i_synonyms'].strip().split('##') if key]:
                if match_all_synonym_words(match_with = synonym,pdf_obj=kwargs['pdf_obj']):
                    pdf_obj = kwargs['pdf_key_list'][kwargs['pdf_obj']]

                    if 'insert' in db_obj:
                        found, save_obj = True, True
                        save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'],
                                                comp=kwargs['pdf_obj'],
                                                     pdf_obj=pdf_obj,pdf_type = kwargs['pdf_type'],
                                                     d_obj=kwargs['db_key_list'][loop], type='breakdown',
                                                     c_name=kwargs['c_name'], insert=True)
                        break;
                    db_obj['insert'] = True
                    found = True
                    save_obj = save_data(p_type= kwargs['p_type'],model = kwargs['model'],
                                            year_end=kwargs['year_end'], comp=kwargs['pdf_obj'],
                                            pdf_obj=pdf_obj,
                                                 d_obj=kwargs['db_key_list'][loop], type='synonym',
                                                 c_name=kwargs['c_name'],pdf_type=kwargs['pdf_type'])

                    break;
            if found != True and 'i_breakdown' in db_obj and db_obj['i_breakdown']:
                found, save_obj = match_breakdown(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], obj_split=db_obj['i_breakdown'].split('##'),
                                        p_obj=kwargs['pdf_obj'],extraction=kwargs['extraction'],
                                        obj_dict=db_obj, img=kwargs['img'], pdf_key_list=kwargs['pdf_key_list'],
                                        page=kwargs['page'], d_obj=kwargs['db_key_list'][loop], c_name=kwargs['c_name'],
                                        pdf_type=kwargs['pdf_type'])

            if found != True and 'i_keyword' in db_obj and db_obj['i_keyword']:
                found, save_obj = match_breakdown(p_type= kwargs['p_type'],model = kwargs['model'],year_end=kwargs['year_end'], obj_split=db_obj['i_keyword'].split(','),
                                        p_obj=kwargs['pdf_obj'],extraction=kwargs['extraction'],
                                        pdf_key_list=kwargs['pdf_key_list'], obj_dict=db_obj, img=kwargs['img'],
                                        page=kwargs['page'], d_obj=kwargs['db_key_list'][loop], c_name=kwargs['c_name'],
                                        pdf_type=kwargs['pdf_type'])

            if save_obj:
                return True
                break;
        else:
            pass


    except Exception as e:
        import traceback
        logger.debug("error for values %s " % kwargs)
        logger.debug(traceback.format_exc())
        return e



def match_with_formula_cell(**kwargs):
    try:
        import itertools
        pnl_sec = Section.objects.filter(i_related = kwargs['save_for'])
        for s_obj in pnl_sec:
            for syn in s_obj.i_synonyms.split('##'):
                x2 = list(itertools.permutations(syn.split(), len(syn.split())))
                obj_per = [' '.join(word) for word in x2]
                if kwargs['pdf_obj'] in obj_per:
                    return True
        return False
    except Exception as e:
        import traceback
        logger.debug("error at the time of skipping formula cell for data :%s " % kwargs)
        logger.debug(traceback.format_exc())
        return e