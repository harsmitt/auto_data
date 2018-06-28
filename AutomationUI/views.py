from rest_framework.views import APIView, Response
from BalanceSheet.models import CompanyBalanceSheetData
from PNL.models import CompanyPNLData
from .forms import *
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
from .utils import *
from DataExtraction.models import Sector
from DataExtraction.choices import year_end,pdf_type
from django.core.cache import cache

from .tranform_data import get_data

class CompanyListView(APIView):
    template_name = 'AutomationUI/index.html'

    def dispatch(self, *args, **kwargs):
        return super(CompanyListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        data=CompanyList.objects.all().values()
        return render(request, 'AutomationUI/index.html', locals())

class BalanceSheetFormView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(BalanceSheetFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if cache.has_key(request.GET['c_id']):
            cache_dict = cache.get(request.GET['c_id'])
            if 'bsheet' in cache_dict:
                data_list = cache_dict['bsheet']
                date_list = cache_dict['date_list']
                loop_key = cache_dict['loop_key']
            else:
                data_list, date_list, loop_key = get_data(req_type='bsheet', c_id=request.GET['c_id'],
                                                          section_type='Balance Sheet')
        else:
            data_list,date_list,loop_key = get_data(req_type='bsheet',c_id=request.GET['c_id'],section_type='Balance Sheet')
        p_type = 'Balance Sheet'
        c_obj = CompanyList.objects.filter(id=request.GET['c_id'])[0]
        print (c_obj.company_name)
        return render(request, 'AutomationUI/bs_data.html', locals())

    def post(self, request, *args, **kwargs):
        return Response({'status': 'success'})



def add_row(request):
    new_row=OrderedDict()
    g_data =dict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'][0]=='pnl' else 'Balance Sheet'
    date_objs =qtr_date_pnl()
    date_objs.update(year_date('December'))
    date_keys = list(date_objs.keys())
    req_type = 'pnl' if g_data['type'][0]=='pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type,c_id=request.GET['c_id'])
    data= data_list
    new_data = g_data['new_row[]']
    new_row[g_data['item'][0]]=OrderedDict(zip(date_keys, new_data))

    added_row = False

    for data in data_list:
        if g_data['section'][0] in list(data.keys()) and not added_row:
            for i in data[g_data['section'][0]]:
                if not added_row:
                    for key, val in i.items():
                            if type(val) == OrderedDict and key == g_data['subsection'][0]:
                                i[key].update(new_row)
                                i['update']=True
                                added_row = True
                                break;
                            elif key == g_data['subsection'][0] and 's2sec' in g_data:
                                for s2sec in val:
                                    for s2,s2_o in s2sec.items():
                                        if s2 == g_data['s2sec'][0]:
                                            s2sec[s2].update(new_row)
                                            i['update'] = True
                                            added_row = True
                                            break;
                elif added_row:
                    break;
        elif added_row:
            break;

    data = [i for i in data_list if g_data['section'][0] in list(i.keys())]
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'],req_type=r_type,p_type=req_type)
    else:
        pass
    # data = save_data(data, request.GET['c_id'],g_data['type'][0])
    if g_data['type'][0] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())

def delete_row(request):
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'
    req_type = 'pnl' if g_data['type'] =='pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']):
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    else:
        data_list, date_list, loop_key = get_data(req_type=req_type,section_type=r_type, c_id=request.GET['c_id'])

    deleted_row =False

    for data in data_list:
        if g_data['section'] in list(data.keys()) and not deleted_row:
            for i in data[g_data['section']]:
                if not deleted_row:
                    for key, val in i.items():
                        if type(val)!=list  and key == g_data['subsection'] :
                            for d_key, d_val in val.items():
                                if d_key == g_data['item']:
                                    i[key].pop(g_data['item'])
                                    i['update'] = True
                                    deleted_row=True
                                    break;
                        elif key == g_data['subsection'] and 's2sec' in g_data:
                            for s2sec in val:
                                for s2, s2_o in s2sec.items():
                                    if s2 == g_data['s2sec']:
                                        s2sec[s2].pop(g_data['item'])
                                        i['update'] = True
                                        deleted_row = True
                                        break;
                elif deleted_row:
                    break;

        elif deleted_row:
            break;
    data = [i for i in data_list if g_data['section'] in list(i.keys())]
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'],req_type=r_type,action_type='delete',p_type= req_type)
    else:
        pass
    if g_data['type']== 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())
    # return render(request, 'AutomationUI/bs_data.html', {'data': data})


class PNLFormView(APIView):
    template_name = 'AutomationUI/pnl.html'
    queryset = CompanyPNLData.objects

    def dispatch(self, *args, **kwargs):
        return super(PNLFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        data=OrderedDict()
        p_type=  'Profit and Loss'
        c_obj = CompanyList.objects.filter(id=request.GET['c_id'])[0]
        print (c_obj.company_name)
        # # if cache.has_key(request.GET['c_id']):
        # #     cache_dict = cache.get(request.GET['c_id'])
        #     if 'pnl' in cache_dict:
        #         data_list = cache_dict['pnl']
        #         date_list = cache_dict['date_list']
        #         loop_key = cache_dict['loop_key']
        #     else:
        #         data_list, date_list, loop_key = get_data(req_type='pnl', section_type='Profit and Loss',
        #                                                   c_id=request.GET['c_id'])
        # else:
        data_list, date_list, loop_key = get_data(req_type='pnl',section_type = 'Profit and Loss', c_id=request.GET['c_id'])
        return render(request, 'AutomationUI/pnl.html', locals())

    def post(self, request, *args, **kwargs):
        return Response({'status': 'success'})



class UploadPDfView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(UploadPDfView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        msg="Upload a File"
        sector_list = Sector.objects.all().values_list('sector_name',flat=True)
        c_year_end = list(year_end)
        p_type = list(pdf_type)

        return render(request, 'AutomationUI/upload_pdf.html', locals())

    def post(self, request, *args, **kwargs):
        from .upload_pdf import upload_pdf
        from DataExtraction.store_data import pdf_detail

        if request.method == 'POST':
            sector_list = Sector.objects.all().values_list('sector_name', flat=True)
            c_year_end = list(year_end)
            p_type = list(pdf_type)

            res,path= upload_pdf(file_1= request.FILES['file'],c_name = request.POST['company_name'], file_n = str(request.FILES['file']))
            if res:
                data_dict = copy.deepcopy(request.POST)
                data_dict = dict(data_dict)
                if not 'override' in data_dict:
                    data_dict['override']=[]
                result = pdf_detail(c_name = request.POST['company_name'],sector = request.POST['sector'],year_end = request.POST['year_end'],
                           file = path,pdf_type =request.POST['pdf_type'],override = data_dict['override']
                           )
                if result:
                    msg = "upload successfully"
                else:
                    msg = "error in uploading file"
            else:
                return HttpResponse("Failed")
            return render(request, 'AutomationUI/upload_pdf.html', locals())



class NewCompanyView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(NewCompanyView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        sector_list = Sector.objects.all().values_list('sector_name', flat=True)
        c_year_end = list(year_end)
        p_type = list(pdf_type)

        return render(request, 'AutomationUI/NewCompany.html', locals())

    def post(self, request, *args, **kwargs):
        from .upload_pdf import upload_pdf
        from DataExtraction.store_data import LoopPdfDir,test

        if request.method == 'POST':
            sector_list = Sector.objects.all().values_list('sector_name', flat=True)
            c_year_end = list(year_end)
            p_type = list(pdf_type)

            # res,path= upload_pdf(request.FILES['file'], str(request.FILES['file']))
            # if res:
            try:
                res = test(c_name = request.POST['company_name'],
                       year_end = request.POST['year_end'],c_ticker = request.POST['company_ticker']
                             )
                from twisted.internet import reactor, defer
                if reactor.running:reactor.stop()
            except Exception as e:
                import traceback
                print (traceback.format_exc())
                print (e)
            res = LoopPdfDir(fix_path='/home/administrator/DataAutomation/company_pdf/',\
                             company_list=[request.POST['company_name']],c_ticker = request.POST['company_ticker'],
                             sector = request.POST['sector'],year_end = request.POST['year_end']
                            )

            return render(request, 'AutomationUI/NewCompany.html', locals())


def pnl_last_qtr(request):
    from DataExtraction.common_files.get_last_qtr_pnl import get_last_qtr_pnl
    c_obj = CompanyList.objects.get(id=request.GET['c_id'])
    get_last_qtr_pnl(year_end=c_obj.y_end, company_name=c_obj.company_name)
    data = OrderedDict()
    section = Section.objects.filter(i_related='Profit and Loss')
    subsection = SubSection.objects.filter(section__in=section)
    comp = list(subsection.filter(s2section=None).values_list('item', flat=True))
    data_list, date_list, loop_key = get_data(req_type='pnl', section_type='Profit and Loss', c_id=request.GET['c_id'])
    return render(request, 'AutomationUI/pnl.html', locals())



def bs_last_qtr(request):
    from DataExtraction.common_files.get_last_qtr_pnl import get_last_bs_qtr
    c_obj = CompanyList.objects.get(id=request.GET['c_id'])
    get_last_bs_qtr(year_end=c_obj.y_end, c_name=c_obj.company_name)
    data = OrderedDict()
    section = Section.objects.filter(i_related='Balance Sheet')
    subsection = SubSection.objects.filter(section__in=section)
    comp = list(subsection.filter(s2section=None).values_list('item', flat=True))

    data_list, date_list, loop_key = get_data(req_type='bsheet', section_type='Balance Sheet', c_id=request.GET['c_id'])
    return render(request, 'AutomationUI/bs_data.html', locals())


def get_existing_date(request):
    print ("hello")
    from django.db.models import Q
    c_obj = CompanyList.objects.filter(company_name=request.GET['c_name'])
    if c_obj:
        q_date = list(quarter_data.objects.filter(Q(company_name=c_obj), ~Q(q1=0)).values_list('quarter_date',
                                                                                          flat=True).distinct())
        q_date = '##'.join(q_date)
        print (q_date)
        return HttpResponse(q_date)
    else:
        return HttpResponse("This is a new company")


def section_list(request):
    r_type = "Balance Sheet" if request.GET['type'] =='balance-sheet' else 'Profit and Loss'
    section = Section.objects.filter(i_related=r_type)
    subsection = SubSection.objects.filter(section__in=section)
    s2sec = S2Section.objects.filter(subsection__in=subsection)
    comp = '##'.join(list(subsection.filter(s2section=None).values_list('item', flat=True))) + '##'.join(list(
        s2sec.values_list('item', flat=True)))
    return HttpResponse(comp)
