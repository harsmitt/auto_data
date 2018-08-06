
from DataExtraction.models import *
from PNL.models import *
from datetime import datetime
def copy_main_subsection(obj):
    sec_obj = Section.objects.filter(i_related='Profit and Loss')
    for s_obj in sec_obj:
        new_obj  = {'sector':obj.sector,'item':obj.sector.sector_name+'##'+s_obj.item,'i_synonyms':s_obj.i_synonyms,'added_date':datetime.now()}
        sector_sec = DITSectorSection(**new_obj)
        sector_sec.save()

        sub_objs = SubSection.objects.filter(section=s_obj)
        for so in sub_objs:
            new_obj = {'sector': obj.sector,'section':sector_sec, 'item': obj.sector.sector_name + '##' + so.item,
                       'i_synonyms': so.i_synonyms,'i_breakdown':so.i_breakdown,'i_keyword':so.i_keyword,
                       'i_deduction':so.i_deduction,'added_date': datetime.now()}
            sector_subsec = DITSectorSubSection(**new_obj)
            sector_subsec.save()
    return True

def remove_main_sub(obj):
    sec = SectorSection.objects.filter(sector=obj)
    for i in sec:
        subsec = SectorSubSection.objects.filter(sector=obj,section=i)

        for ob in subsec:
            ob.delete()
        i.delete()
    return True
