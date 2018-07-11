from .basic_functions import *
from DataExtraction.models import *

def get_last_qtr_pnl(**kwargs):
    date_objs = qtr_date_pnl()
    date_objs.update(year_date(kwargs['year_end']))
    years = year_date(kwargs['year_end'])
    qtrs = qtr_date_pnl()
    qtr_list = list(qtrs.values())
    for year in years:
        p_qtrs = []
        qtr = kwargs['year_end'].lower()+' '+str(date_objs[year])
        last_m, next_m = next_last_month(qtr)
        match_qtr = qtr.lower() if qtr.lower() in qtr_list else last_m if last_m.lower() in qtr_list \
            else next_m if next_m.lower() in qtr_list else ''
        if match_qtr:
            q_key = (list(qtrs.keys())[list(qtrs.values()).index(str(match_qtr).lower())])
            if get_digit(q_key) >=4:
                p_qtrs.append('q'+str(get_digit(q_key)-1))
                p_qtrs.append('q' + str(get_digit(q_key) - 2))
                p_qtrs.append('q' + str(get_digit(q_key) - 3))
                update_last_qtr(p_qtrs = p_qtrs,end_qtr = q_key,year =year,date_objs=date_objs,name= kwargs['company_name'])
            else:
                print ("data is not available")




def update_last_qtr(**kwargs):
    #
    # all_objs = quarter_data.objects.filter(company_name__comapny_name=kwargs['name'], page_extraction='pnl')
    p_1 = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['p_qtrs'][0]])
    p_2 = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['p_qtrs'][1]])
    p_3 = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['p_qtrs'][2]])
    ending_q = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['end_qtr']])
    y_obj = quarter_data.objects.filter(company_name__company_name=kwargs['name'], page_extraction='pnl',quarter_date = kwargs['date_objs'][kwargs['year']])
    for obj in ending_q:
        val =0
        p1 = p_1.get(section=obj.section,subsection=obj.subsection,s2section=obj.s2section)
        val+= float(p1.q1) if '.' in str(p1.q1) else int(p1.q1)
        p2 = p_2.get(section=obj.section, subsection=obj.subsection, s2section=obj.s2section)
        val += float(p2.q1) if '.' in str(p2.q1) else int(p2.q1)
        p3 = p_3.get(section=obj.section, subsection=obj.subsection, s2section=obj.s2section)
        val += float(p3.q1) if '.' in str(p3.q1) else int(p3.q1)
        y1 = y_obj.get(section=obj.section, subsection=obj.subsection, s2section=obj.s2section)
        val = (float(y1.q1) if '.' in str(y1.q1) else int(y1.q1)) - val
        obj.description= 'calculate '+str(val)
        obj.q1 = val
        obj.save()


def get_last_bs_qtr(**kwargs):
    qtr_dict = qtr_date_pnl()
    year_dict= year_date(kwargs['year_end'])
    date_objs = qtr_date_pnl()
    qtr_list = list(qtr_date_pnl().values())
    date_objs.update(year_date(kwargs['year_end']))
    year_list= list(year_date(kwargs['year_end']).values())
    for year in year_list:
        qtr = kwargs['year_end']+' '+str(year)
        last_m,next_m = next_last_month(qtr)
        match_qtr = qtr.lower() if qtr.lower() in qtr_list else last_m if last_m.lower() in qtr_list\
                    else next_m if next_m.lower() in qtr_list else ''
        if match_qtr :
            y_key = (list(year_dict.keys())[list(year_dict.values()).index(int(year))])
            print (qtr_dict)
            print (str(match_qtr).lower())

            q_key = (list(qtr_dict.keys())[list(qtr_dict.values()).index(str(match_qtr).lower())])  # Prints george
            save_yending_qtr = copy_year_data(year_end =kwargs['year_end'],c_name =kwargs['c_name'],y_key = y_key,q_key = q_key)
        else:
            pass

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