from .basic_functions import *
from .utils import *
from DataExtraction.models import *
from django.shortcuts import render
from AutomationUI.tranform_data import get_data
from AutomationUI.views import get_qtrs
from DataExtraction.logger_config import logger


def cal_qtr_pnl(request):
    try:
        prev_q =[]
        c_obj = CompanyList.objects.get(id=request.GET['c_id'])

        date_objs = qtr_date(c_obj.y_end)
        date_objs.update(year_date(c_obj.y_end))
        years = year_date(c_obj.y_end)
        qtrs = qtr_date(c_obj.y_end)
        qtr_list = list(qtrs.values())

        q_val = request.GET['q_val']
        q_key = (list(qtrs.keys())[list(qtrs.values()).index(str(request.GET['q_val']).lower())])
        if get_digit(q_key) >= 2 and request.GET['cal_qtr'] == 'Cal_q2':
            prev_q.append('q' + str(get_digit(q_key) - 1)) if get_digit(q_key) !=0 else prev_q.append('q' + str(get_digit(q_key)))
        else:
            prev_q.append('q' + str(get_digit(q_key) - 2)) if get_digit(q_key) !=0 else prev_q.append('q' + str(get_digit(q_key)))
            prev_q.append('q' + str(get_digit(q_key) - 1)) if get_digit(q_key) !=0 else prev_q.append('q' + str(get_digit(q_key)))
        x = get_qtr(p_qtrs=prev_q, end_qtr=q_key,date_objs=date_objs, name=c_obj.company_name)
        p_type = 'Profit and Loss'
        # c_obj = CompanyList.objects.filter(id=request.GET['c_id'])[0]
        q2, q3 = get_qtrs(c_obj)
        data_list, date_list, loop_key = get_data(req_type='pnl', section_type='Profit and Loss', c_id=request.GET['c_id'])

        return render(request, 'AutomationUI/pnl.html', locals())

    except Exception as e:
        logger.debug("error in cal_qtr_pnl for company %s " % c_obj)
        logger.debug(traceback.format_exc())

def get_qtr(**kwargs):
    for i in kwargs['p_qtrs']:
        p_1 = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][i])
        ending_q = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['end_qtr']])
        # y_obj = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['year']])
        for obj in ending_q:
            val =0
            p1 = p_1.get(section=obj.section,subsection=obj.subsection,s2section=obj.s2section)
            val+= float(p1.q1) if '.' in str(p1.q1) else int(p1.q1)
            six_months = ending_q.get(section=obj.section, subsection=obj.subsection, s2section=obj.s2section)
            val = (float(six_months.q1) if '.' in str(six_months.q1) else int(six_months.q1)) - val
            obj.description= obj.description.split('(')[0] +'('+str(val)+')'
            obj.q1 = val
            obj.save()
    return True