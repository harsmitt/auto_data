from DataExtraction.models import *
from DataExtraction.common_files.basic_functions import *
from DataExtraction.common_files.utils import *

# from BalanceSheet.models import CompanyBalanceSheetData


def copy_year_data(**kwargs):
    date_objs = qtr_date_pnl()
    date_objs.update(year_date(kwargs['year_end']))
    y_objs = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'],page_extraction='bsheet',quarter_date = date_objs[kwargs['y_key']])
    q_objs = quarter_data.objects.filter(company_name__company_name=kwargs['c_name'],page_extraction='bsheet',quarter_date = date_objs[kwargs['q_key']])
    for obj in y_objs:
        q_o = q_objs.get(section=obj.section,subsection=obj.subsection,s2section=obj.s2section)
        q_o.description = obj.description
        q_o.q1 = obj.q1
        q_o.save()
    return True
