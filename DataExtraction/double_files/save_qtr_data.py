from .models import *
from .mapping_data import keywords_relation
from .common_functions import *
from .save_data_qtr import place_keyword
import copy
import re

def match_keyword_qtr(**kwargs):
    for keyword in kwargs['data']:
        if keyword.lower() in equity_key_list :
            c_lib = copy.deepcopy(keywords_relation.equity_map_dict)
            img_path = save_image(path, page,company_name)
            for comp in data[keyword]:

                print (comp)
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
        else:
            keyword_data = copy.deepcopy(keywords_relation.comp_mapping_dict[keyword])
            img_path = save_image(kwargs['path'], kwargs['page'], kwargs['company_name'])
            for comp in kwargs['data'][keyword]:
                print (comp)
                if 'total' not in comp.lower():
                    obj_save = place_keyword(comp, kwargs['data'][keyword], keyword_data, img_path, kwargs['page'], c_name=kwargs['company_name'])

                    if not obj_save:

                        if any(i in comp.lower() for i in d_keywords):
                            other_obj = SubSection.objects.get(item=[i for i in keywords_relation.other_dict[keyword] if 'deduction' in i.lower()][0])
                            save_data(comp, data[keyword][comp], img_path, page,
                                      other_obj.id,
                                      other_obj.section.id, other_obj.item,
                                      sec='s1sec',
                                      type='breakdown', c_name=company_name)
                        else:
                            other_obj = other_obj = S2Section.objects.get(
                                item=[i for i in keywords_relation.other_dict[keyword] if 'deduction' not in i.lower()][0])
                            save_obj = save_data(comp, data[keyword][comp], img_path, page, other_obj.id,
                                                 other_obj.subsection.section.id, other_obj.item,
                                                 sec='s1sec',
                                                 type='breakdown', c_name=company_name,
                                                 subsec=other_obj.subsection.id)
