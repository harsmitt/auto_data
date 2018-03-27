# from BalanceSheet.models import *

from PNL.models import *


class MappingDict(object):
    key_mapping_dict = {('assets', 'current assets'): 'current assets',
                    ( 'current liabilities', 'total assets'): 'current liabilities',
                    ('total current assets', 'non current assets', 'long term assets'): 'non current assets',
                    ('total current liabilities', 'long term liabilities',
                     'non current liabilities'): 'non current liabilities',
                    ('total liabilities', 'shareholders equity', 'stockholders equity','total non current liabilities','total long term liabilities','commitments and contingencies'): 'stockholders equity'}


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

    pnl_mapping_dict = {('Net revenue','Revenue','Net sales'):'Revenue',
                        ('cost of sales','Cost of Revenue'):'Cost of Revenue',
                        ('selling, general and administrative expenses','selling and general expenses'):'selling and general',
                        ('Operating expense','Expenses') :'Operating Expenses',
                        ('Operating income','other income') :'Other Operating Income',
                        ('other income expense, net','other expense'):'Non-Operating Income/(Expenses)',
                        ('Operating costs and expenses','Costs and expenses'):'opearting cost and expense',
                        ('Expenses and Other','operating expense and other'):'opearting expense and non operating',

                        }

    other_pnl_mapping = {'Revenue':'Revenue','Cost of Revenue':'Cost of Revenue','Operating Expenses':'Other Operating Expense',
                         'Other Operating Income' :'Other Operating Revenue','selling and general':'Other Operating Expense',
                         'Non-Operating Income/(Expenses)' : 'Other Non-Operating Income/(Expenses)',
                         'opearting cost and expense':'Other Operating Expense',
                         'opearting expense and non operating':'Other Operating Expense',
                         }

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

    comp_mapping_dict = {'current assets': current_assets_obj, 'non current assets': noncurrent_assets_obj,
                         'current liabilities': current_lib_obj, 'non current liabilities': noncurrent_lib_obj,
                         'stockholders equity': equity_obj,'assets':assets_obj,'liabilities':liab_obj,
                         'assets':assets_obj,'liabilities':liab_obj
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
            print (i.sector_name)
            sector_dict.update({i.sector_name:main_set})
            for sec in sec_obj:
                sec_subsec = SubSection.objects.filter(section=sec).values('i_synonyms','i_breakdown','i_keyword','item','section', 'id')
                sector_section[i.sector_name].update({sec.item: list(sec_subsec)})

            sec_subsec = SubSection.objects.filter(section__item__in=['Operating Expenses','Cost of Revenue']).values('i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                                                                       'section', 'id')

            sector_section[i.sector_name].update({'opearting cost and expense': list(sec_subsec)})
            sec_subsec = SubSection.objects.filter(section__item__in=['Operating Expenses', 'Non-Operating Income/(Expenses)']).values(
                'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                'section', 'id')

            sector_section[i.sector_name].update({'opearting expense and non operating': list(sec_subsec)})
        else:
            print (i.sector_name)
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

                opcost_exp = SectorSubSection.objects.filter(section__item__in=['Operating Expenses', 'Cost of Revenue']).values(
                    'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                    'section', 'id')

                sector_section[i.sector_name].update({'opearting cost and expense': list(opcost_exp)})
                op_nop = SectorSubSection.objects.filter(
                    section__item__in=['Operating Expenses', 'Non-Operating Income/(Expenses)']).values(
                    'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                    'section', 'id')
                sector_section[i.sector_name].update({'opearting expense and non operating': list(op_nop)})



                sell_gen = SectorSubSection.objects.filter(
                    section__item__in=['Selling & Marketing Expenses', 'General & Administrative Expenses']).values(
                    'i_synonyms', 'i_breakdown', 'i_keyword', 'item',
                    'section', 'id')

                sector_section[i.sector_name].update({'selling and general': list(sell_gen)})


            # import pdb;pdb.set_trace()
            # print (sector_dict)





bs_objs = ObjectMapping()
pnl_objs = PNLMapping()
mapping_dict = MappingDict()


