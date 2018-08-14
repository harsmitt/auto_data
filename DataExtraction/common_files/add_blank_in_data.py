from DataExtraction.models import *
from BalanceSheet.models import *
from PNL.models import *
from DataExtraction.logger_config import logger

import os
import errno
import re
from .utils import *

from wand.display import display
from wand.image import Image

DEFAULT_DATA_PATH = '/home/mahima/DataAutomation/images/'


def make_directory(company_name):
    # Making the directory to save comapny filings
    try:
        path = os.path.join(DEFAULT_DATA_PATH, company_name.split()[0])

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
    except Exception as e:
        logger.debug("error in make directory %s " % e)
        logger.debug(traceback.format_exc())




def save_image(path, page, company_name):
    try:
        import os
        path1 = path + str([int(page) - 1])
        make_directory(company_name)
        with Image(filename=path1) as img:
            # img.transform(resize="%dx%d>" % (width, height))
            img_path = os.path.join(DEFAULT_DATA_PATH, company_name.split()[0])
            img_path = img_path + '/' + path.split('/')[-1].split('.')[0] + '.png'
            import os.path
            if not os.path.exists(img_path):
                img.save(filename=img_path)
        return img_path
    except Exception as e:
        logger.debug("error in save_image %s " % e)
        logger.debug(traceback.format_exc())
        return e


def add_quarter(path, page, qtr_dict,c_obj,subsection,section,s2section):
    try:
        q_dict = {}
        qtr_obj = quarter_data.objects.filter(subsection=subsection, section=section, gbc_name=c_obj,
                                                         s2section=s2section)
        if not qtr_obj:
            for k, v in qtr_dict.items():
                key_dict = {'gbc_name': c_obj, 'section': section,'description': '',
                            'quarter_date': v, 'q1': 0,'subsection':subsection,'s2section':s2section,
                            'pdf_page': page,
                            'pdf_image_path': path}
                query1 = quarter_data(**key_dict)
                query1.save()
                q_dict[k] = query1
            return q_dict
    except Exception as e:
        logger.debug("error in add_quarter %s " % e)
        logger.debug(traceback.format_exc())
        return e

def add_gbc(img_path, page, c_name,year_end, c_obj, sec, sub_obj=None, s2_obj=None,pdf_page = None):
    try:
        qtr_dict = qtr_date(year_end=year_end)
        year_dict = year_date(year_end)
        qtr_dict.update(year_dict)
        q_dict = {}

        qtr_obj = quarter_data.objects.filter(subsection=sub_obj, section=sec, company_name=c_obj,
                                              s2section=s2_obj)

        pdf_extraction = 'bsheet' if pdf_page != 'pnl' else 'pnl'
        if not qtr_obj:
            for k, v in qtr_dict.items():
                key_dict = {'company_name': c_obj, 'section': sec, 'description': '',
                            'page_extraction':pdf_extraction,
                            'quarter_date': v, 'q1': 0, 'subsection': sub_obj, 's2section': s2_obj,
                            'pdf_page': page,
                            'pdf_image_path': img_path}
                query1 = quarter_data(**key_dict)
                query1.save()
                q_dict[k] = query1
            return False
        return True

    except Exception as e:
        logger.debug("error in add gbc %s " % e)
        logger.debug(traceback.format_exc())
        return e

def Create_blank_sheet(c_name, path, page,year_end,dit_name):
    try:
        c_obj = CompanyList.objects.filter(company_name = c_name,ditname__dit_name=dit_name)
        if not c_obj:
            dit_id = SectorDit.objects.get(dit_name=dit_name)
            c_dict = {'company_name': c_name,'ditname_id':dit_id.id,'y_end':year_end}
            c_obj = CompanyList(**c_dict)
            c_obj.save()
        else:
            c_obj = c_obj[0]

        sec_obj = Section.objects.filter(i_related='Balance Sheet')

        img_path = save_image(path, page, c_name)
        for sec in sec_obj:
            import time
            time.sleep(5)
            exist = add_gbc(img_path, page, c_name,year_end, c_obj, sec)
            if not exist:
                sub_obj = SubSection.objects.filter(section=sec)
                for sub in sub_obj:
                    x = add_gbc(img_path, page, c_name,year_end, c_obj, sec, sub_obj=sub)
                    s2_obj = S2Section.objects.filter(subsection=sub)
                    if s2_obj:
                        for s2 in s2_obj:
                            x = add_gbc(img_path, page, c_name,year_end, c_obj, sec, sub_obj=sub, s2_obj=s2)
            else:
                break;
        return img_path,c_obj.company_name

    except Exception as e:
        logger.debug("error in create balance sheet blank data %s " % e)
        logger.debug(traceback.format_exc())
        return e

def Create_pnl(c_name,path,page,year_end,dit_name):
    try:
        c_obj = CompanyList.objects.filter(company_name = c_name,ditname__dit_name=dit_name)
        if not c_obj:
            dit_id = SectorDit.objects.get(dit_name=dit_name)
            c_dict = {'company_name': c_name,'ditname_id':dit_id.id,'y_end':year_end}
            c_obj = CompanyList(**c_dict)
            c_obj.save()
        else:
            c_obj = c_obj[0]
        sector_name = SectorDit.objects.get(dit_name = c_obj.ditname)
        if not sector_name.sector.copy_main:
            sec_obj = SectorSection.objects.filter(sector = sector_name.sector)
        else:
            sec_obj = Section.objects.filter(i_related='Profit and Loss')
        img_path = save_image(path, page, c_name)
        for sec in sec_obj:
            sectorsec_item = sec.item.split('##')[-1]
            section = Section.objects.get(item = sectorsec_item)
            exist =add_gbc(img_path, page, c_name,year_end,c_obj, section,pdf_page='pnl')
            if not exist:
                sub_obj = SubSection.objects.filter(section=sec) if sector_name.sector.copy_main else\
                            SectorSubSection.objects.filter(section=sec)
                if sub_obj:
                    for sub in sub_obj:
                        sectorsubsec_item = sub.item.split('##')[-1]
                        subsec = SubSection.objects.get(item=sectorsubsec_item)
                        x=add_gbc(img_path, page, c_name,year_end, c_obj,section,sub_obj=subsec,pdf_page='pnl')

            else:
                break;
        return img_path,c_obj.company_name

    except Exception as e:
        logger.debug("error in create blank pnl %s " % e)
        logger.debug(traceback.format_exc())
        return e