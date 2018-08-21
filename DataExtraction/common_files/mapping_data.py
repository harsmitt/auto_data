# from BalanceSheet.models import *

from PNL.models import *


class MappingDict(object):

    key_mapping_dict = {('assets', 'current assets'): 'current assets',
                    ( 'current liabilities','liabilities','total assets','liabilities and equity','current and accrued liabilities'): 'current liabilities',
                    ('total current assets', 'non current assets', 'long term assets'): 'non current assets',
                    ('total current liabilities', 'long term liabilities',
                     'non current liabilities'): 'non current liabilities',
                    ('total liabilities','capitalization and liabilities',
                     'equity and liabilities','shareholders equity','capital and reserves',
                     'equity','stockholders equity','total non current liabilities',
                     'total long term liabilities','commitments and contingencies'): 'stockholders equity'}


    other_mapping_dict = {'current assets': {'other_asset':'Other Current Assets (not listed above)',
                                             'deduction':'Other Current Liabilities Deduction'},
                  'non current assets': {'other_asset':'Other Non-Current Assets (not listed above)',
                                         'deduction':'Other Non-Current Assets Deduction'},
                  'current liabilities': {'other_asset':'Other Current Liabilities (not listed above)',
                                          'deduction':'Other Current Liabilities Deduction'},
                  'non current liabilities': {'other_asset':'Other Non-Current Liabilities (not listed above)',
                                              'deduction':'Other Non-Current Liabilities Deduction'},
                  'stockholders equity': {'other_asset':'Other Equity', 'deduction':'Other Equity Deduction'}
                  }

    pnl_mapping_dict = {('Net revenue','Revenue','Net sales','revenues from operations',
                         'operating revenues','Turnover'):'Revenue',
                        ('cost of sales','cost of revenue','cost of goods sold'):'Cost of Revenue',
                        ('Operating expenses','Operating cost'):'Operating Expenses',
                        ('selling, general and administrative expenses','selling and general expenses'):'selling and general',
                        ('other income expense, net','other income expense , net','other income expense'):'nonop and income tax',
                                                }

    other_pnl_mapping = {'Revenue':'Revenue',
                         'Cost of Revenue':'Cost of Revenue',
                         'Operating Expenses':'Other Operating Expense',
                         'selling and general':'Other Operating Expense',
                         'Non-Operating Income/(Expenses)' : 'Other Non-Operating Income/(Expenses)',
                         'opearting cost and expense and nonop':'Extra PNL Keywords',
                         'nonop and income tax': 'Extra PNL Keywords',

                         # 'opearting expense and non operating':'Other Operating Expense',
                         }

    #todo create mapping dict for expense and income
    # pnl2_mapping_dict = {('Operating expense','Expenses') :'opearting cost and expense and nonop',
    #
    #                      # ('Operating costs and expenses', 'Costs and expenses','Expenses and Other', 'operating expense and other'): 'opearting cost and expense and nonop',
    #                      # (): 'opearting expense and non operating',
    #                      }

class ObjectMapping(object):
    c_assets_sec = Section.objects.filter(item = 'Current Assets').values()
    c_assets_subsec = SubSection.objects.filter(section_id__in=c_assets_sec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
    c_assets_s2sec = S2Section.objects.filter(subsection_id__in=c_assets_subsec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id')


    nc_assets_sec = Section.objects.filter(item = 'Non-Current Assets').values()
    nc_assets_subsec = SubSection.objects.filter(section_id__in = nc_assets_sec.values_list('id',flat=True) ).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
    nc_assets_s2sec = S2Section.objects.filter(subsection_id__in=nc_assets_subsec.values_list('id',flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id')

    c_lib_sec = Section.objects.filter(item='Current Liabilities').values()
    c_lib_subsec = SubSection.objects.filter(section_id__in=c_lib_sec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
    c_lib_s2sec = S2Section.objects.filter(subsection_id__in=c_lib_subsec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id')

    nc_lib_sec = Section.objects.filter(item='Non-Current Liabilities').values()
    nc_lib_subsec = SubSection.objects.filter(section_id__in=nc_lib_sec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
    nc_lib_s2sec = S2Section.objects.filter(subsection_id__in=nc_lib_subsec.values_list('id', flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','subsection','subsection__section','id')

    equity_sec = Section.objects.filter(item ='Shareholder Equity').values()
    equity_subsec = SubSection.objects.filter(section_id__in= equity_sec.values_list('id',flat=True)).values('i_synonyms','i_breakdown','i_keyword','item','section','id')

    current_assets_obj = list(c_assets_sec)+list(c_assets_subsec)+list(c_assets_s2sec)
    noncurrent_assets_obj = list(nc_assets_sec)+list(nc_assets_subsec)+list(nc_assets_s2sec)

    current_lib_obj = list(c_lib_sec)+list(c_lib_subsec)+list(c_lib_s2sec)
    noncurrent_lib_obj = list(nc_lib_sec)+list(nc_lib_subsec)+list(nc_lib_s2sec)

    equity_obj =list(equity_sec)+list(equity_subsec)

    assets_obj = current_assets_obj+noncurrent_assets_obj
    liab_obj = current_lib_obj+noncurrent_lib_obj
    bsheet = current_assets_obj+noncurrent_lib_obj+current_lib_obj+noncurrent_assets_obj

    comp_mapping_dict = {'current assets': current_assets_obj, 'non current assets': noncurrent_assets_obj,
                         'current liabilities': current_lib_obj, 'non current liabilities': noncurrent_lib_obj,
                         'stockholders equity': equity_obj,'assets':assets_obj,'liabilities':liab_obj,
                         'assets':assets_obj,'liabilities':liab_obj,'bsheet':bsheet
                         }

class PNLMapping(object):
    sector_dict={}
    sector_section={}
    sec_obj = Section.objects.filter(i_related='Profit and Loss')
    subsec_obj =SubSection.objects.filter(section__in= sec_obj).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
    # same_dict = SectorSection.objects.filter(copy_main=True).values_list('sector_name')
    sector_obj = Sector.objects.all()
    main_set = list(sec_obj.values())+list(subsec_obj)

    for i in sector_obj:
        sector_section[i.sector_name]={}
        if i.copy_main:
            sector_dict.update({i.sector_name:main_set})
            for sec in sec_obj:
                sec_subsec = SubSection.objects.filter(section=sec).values('i_synonyms','i_breakdown','i_keyword','item','section', 'id')
                sector_section[i.sector_name].update({sec.item: list(sec_subsec)})

            sec_subsec = SubSection.objects.filter(section__item__in=['Operating Expenses','Cost of Revenue','Non-Operating Income/(Expenses)','Income Tax Expense','Profit/(Loss) from Discontinued Operations']).values('i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                                                                       'section', 'id')

            sector_section[i.sector_name].update({'opearting cost and expense and nonop': list(sec_subsec)})

            sec_subsec = SubSection.objects.filter(
                section__item__in=['Non-Operating Income/(Expenses)','Other Operating Income',
                                   'Income Tax Expense', 'Profit/(Loss) from Discontinued Operations']).values(
                'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                'section', 'id')

            sector_section[i.sector_name].update({'nonop and income tax': list(sec_subsec)})


        else:
            sectorsec = SectorSection.objects.filter(sector = i)
            sector_subsec = SectorSubSection.objects.filter(sector=i,section__in = sectorsec).values('i_synonyms','i_breakdown','i_keyword','item','section','id')
            sector_list = list(sectorsec.values())+list(sector_subsec)
            sector_dict.update({i.sector_name: sector_list})
            for sec in sectorsec:
                sec_subsec = SectorSubSection.objects.filter(sector=i, section=sec).values('i_synonyms','i_breakdown',
                                                                                                        'i_keyword',
                                                                                                        'item',
                                                                                                        'section', 'id')
                key =sec.item.split('##')[-1]
                sector_section[i.sector_name].update({key:list(sec_subsec)})

            sectorsection_name = [i.sector_name+'##Non-Operating Income/(Expenses)',i.sector_name+'##Operating Expenses',\
                                  i.sector_name+'##Cost of Revenue',i.sector_name+'##Income Tax Expense',i.sector_name+'##Other Operating Income',\
                                  i.sector_name+'##Profit/(Loss) from Discontinued Operations']

            opcost_exp = SectorSubSection.objects.filter(section__item__in=sectorsection_name).values(
                'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                'section', 'id')

            # sector_section[i.sector_name].update({'opearting cost and expense': list(opcost_exp)})
            sector_section[i.sector_name].update({'opearting cost and expense and nonop': list(opcost_exp)})
            # op_nop = SectorSubSection.objects.filter(
            #     section__item__in=['Operating Expenses', 'Non-Operating Income/(Expenses)']).values(
            #     'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
            #     'section', 'id')
            # sector_section[i.sector_name].update({'opearting expense and non operating': list(op_nop)})

            sell_gen = SectorSubSection.objects.filter(
                section__item__in=['Selling & Marketing Expenses', 'General & Administrative Expenses']).values(
                'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                'section', 'id')

            sector_section[i.sector_name].update({'selling and general': list(sell_gen)})
    print ("done mapping")


bs_objs = ObjectMapping()
pnl_objs = PNLMapping()
mapping_dict = MappingDict()

##keywords list

toc =['table of content','index','content','page no']

b_keywords = ['balance sheet','financial position']#,'condensed consolidated balance sheet',
              # 'consolidated balance sheet','consolidated statement of financial position',
              # 'consolidated statement of balance sheet']

p_keywords = ['statement of income','statement of operation','statement of profit and loss',
              # 'consolidated statement of income','consolidated statement of operation',
              'statements of earnings','statement of comprehensive loss',
#               'consolidated statement of comprehensive income',
#               'statement of income','statement of operation'
              ]

stop_words =  ['of', 'on', 'at', 'a', 'an','to','the','are','from','and']

k_list = {'toc':toc,'bsheet':b_keywords,'pnl':p_keywords}

import itertools

qtr_combinations=[('three months ended','six months ended'),('three months ended','nine months ended'),
                  ('3 months ended','6 months ended'),('3 months ended','9 months ended'),('13 weeks ended','26 weeks ended'),
                    ('13 weeks ended','39 weeks ended'),('12 weeks ended','40 weeks months ended'),('12 weeks ended','28 weeks months ended'),
                    ('twelve weeks ended','forty weeks months ended'),('twelve weeks ended','twenty eight weeks months ended'),
                    ('twelve weeks ended','twenty four weeks months ended'),('12 weeks ended','24 weeks months ended'),
                    ('twelve weeks ended','thirty six weeks months ended'),('12 weeks ended','36 weeks months ended'),
                    ('three months ended',), ('3 months ended',), ('13 weeks ended',),('sixteen week ended ',),('16 week ended ',
                    ('twelve weeks ended ',),('12 weeks ended ',),('note'))]

i_list_comb = ['group', 'company', 'note','parent']#]+qtr_combinations

balance_sheet_keys = ['current assets','non current assets','current liabilities','non current liabilities','stockholders equity']

i_list_1 =['note','3 months ended','three months ended']
ignore_index_list = list(itertools.permutations(i_list_comb,2))+list(itertools.permutations(i_list_comb,3))\
                    + list(itertools.permutations(i_list_1,1))

