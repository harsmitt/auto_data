from DataExtraction.models import *

mapping_dict ={('assets','current assets'):'current assets',
               ('LIABILITIES AND'.lower(),'current liabilities','total assets'):'current liabilities',
               ('total current assets','non current assets','long term assets'):'non current assets',
               ('total current liabilities','long term liabilities','non current liabilities'):'non current liabilities',
               ('total liabilities','shareholders equity','stockholders equity'):'stockholders equity'}

class KeywordsPool(object):

    c_asset_s1sec_map_dict = list(SubSection.objects.filter(section_id=1).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))
    nc_asset_s1sec_map_dict =list(SubSection.objects.filter(section_id=2).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))

    c_asset_s2sec_map_dict = list(S2Section.objects.filter(subsection_id=5).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id'))
    nc_asset_s2sec_map_dict =list(S2Section.objects.filter(subsection_id=12).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id'))

    c_asset = c_asset_s1sec_map_dict + c_asset_s2sec_map_dict
    nc_asset = nc_asset_s1sec_map_dict + nc_asset_s2sec_map_dict


    c_lib_s1sec_map_dict = list(SubSection.objects.filter(section_id=3).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))
    nc_lib_s1sec_map_dict =list(SubSection.objects.filter(section_id=4).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))

    c_lib_s2sec_map_dict = list(S2Section.objects.filter(subsection_id=16).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id'))
    nc_lib_s2sec_map_dict =list(S2Section.objects.filter(subsection_id=19).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id'))

    pnl_map_dict = list(SubSection.objects.filter(section_id__in=[6,7,8,9,10]).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))

    equity_map_dict = list(SubSection.objects.filter(section_id=5).values('i_synonyms','i_breakdown','i_keyword','item','section','id'))

    c_lib = c_lib_s1sec_map_dict+ c_lib_s2sec_map_dict
    nc_lib = nc_lib_s1sec_map_dict+nc_lib_s2sec_map_dict

    comp_mapping_dict = {'current assets':c_asset,'non current assets':nc_asset,
                    'current liabilities':c_lib,'non current liabilities':nc_lib,
                    'equity':equity_map_dict
                    }

    other_dict = {'current assets':['Other Current Assets (not listed above)','Other Current Liabilities Deduction'],
                  'non current assets':['Other Non-Current Assets (not listed above)','Other Non-Current Assets Deduction'],
                  'current liabilities':['Other Current Liabilities (not listed above)','Other Current Liabilities Deduction'],
                  'non current liabilities':['Other Non-Current Liabilities (not listed above)','Other Non-Current Liabilities Deduction'],
                  'equity':['Other Equity','Other Equity Deduction']
                  }

keywords_relation = KeywordsPool()