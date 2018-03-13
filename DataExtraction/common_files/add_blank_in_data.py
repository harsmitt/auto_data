from DataExtraction.models import *
from BalanceSheet.models import *
from PNL.models import *

import os
import errno
import re
from .utils import *

DEFAULT_DATA_PATH = '/home/administrator/DataAutomation/images/'


def make_directory(company_name):
    # Making the directory to save comapny filings
    path = os.path.join(DEFAULT_DATA_PATH, company_name.split()[0])

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


from wand.display import display
from wand.image import Image


def save_image(path, page, company_name):
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


def add_quarter(path, page, company_name,year_end):
    q_dict = {}
    qtr_dict = qtr_date(year_end=year_end)
    for k, v in qtr_dict.items():
        key_dict = {'description': '', 'quarter_date': v, 'q1': 0,
                    'pdf_page': page,
                    'pdf_image_path': path}
        query1 = quarter_data(**key_dict)
        query1.save()
        q_dict[k] = query1
    return q_dict


def add_year(path, page, c_name,year_end):
    y_dict = {}
    year_dict = year_date(year_end)
    for k, v in year_dict.items():
        key_dict = {'description': '', 'year_date': v, 'y1': 0,
                    'pdf_page': page,
                    'pdf_image_path': path}
        query1 = year_data(**key_dict)
        query1.save()
        y_dict[k] = query1
    return y_dict


def add_gbc(img_path, page, c_name,year_end, c_obj, sec, sub_obj=None, s2_obj=None,pdf_page = None):
    q_dict = add_quarter(img_path, page, c_name,year_end)
    y_dict = add_year(img_path, page, c_name,year_end)
    if not pdf_page:
        gbc_obj = CompanyBalanceSheetData.objects.filter(subsection=sub_obj, section=sec, gbc_name=c_obj, s2section=s2_obj)
    else:

        gbc_obj = CompanyPNLData.objects.filter(subsection=sub_obj, section=sec, gbc_name=c_obj,
                                                         s2section=s2_obj)
    if not gbc_obj:
        gbc_dict = {'gbc_name': c_obj, 'section': sec, 'q1': q_dict['q1'],
                    'q2': q_dict['q2'], 'q3': q_dict['q3'], 'q4': q_dict['q4'],
                    'lrq': q_dict['lrq'], 'y1': y_dict['y1'], 'y2': y_dict['y2'], 'y3': y_dict['y3'],
                    'y4': y_dict['y4'],
                    }

        if sub_obj and s2_obj:
            gbc_dict['subsection'] = sub_obj
            gbc_dict['s2section'] = s2_obj

        elif sub_obj and not s2_obj:
            gbc_dict['subsection'] = sub_obj
        query1 = CompanyBalanceSheetData(**gbc_dict) if not pdf_page else CompanyPNLData(**gbc_dict)
        query1.save()
        return False

    return True


def Create_blank_sheet(c_name, path, page,year_end):
    c_obj = CompanyList.objects.filter(company_name__icontains=c_name)
    if not c_obj:
        c_dict = {'company_name': c_name,'ditname_id':214}
        c_obj = CompanyList(**c_dict)
        c_obj.save()
    else:
        c_obj = c_obj[0]
    sec_obj = Section.objects.filter(i_related='Balance Sheet')

    img_path = save_image(path, page, c_name)
    for sec in sec_obj:
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

def Create_pnl(c_name,path,page,year_end):
    c_obj = CompanyList.objects.filter(company_name__icontains=c_name)
    if not c_obj:
        c_dict = {'company_name': c_name,'ditname_id':214}
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
        sectorsec_item = sec.item.split('##')[1]
        section = Section.objects.get(item = sectorsec_item)
        exist =add_gbc(img_path, page, c_name,year_end,c_obj, section,pdf_page='pnl')
        print(sec)
        if not exist:
            sub_obj = SubSection.objects.filter(section=sec) if sector_name.sector.copy_main else\
                        SectorSubSection.objects.filter(section=sec)

            for sub in sub_obj:
                sectorsubsec_item = sub.item.split('##')[1]
                subsec = SubSection.objects.get(item=sectorsubsec_item)
                x=add_gbc(img_path, page, c_name,year_end, c_obj,section,sub_obj=subsec,pdf_page='pnl')

        else:
            break;
    return img_path,c_obj.company_name