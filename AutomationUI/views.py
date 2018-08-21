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

        data=OrderedDict()
        section = Section.objects.filter(i_related ='Balance Sheet')
        subsection =SubSection.objects.filter(section__in =section)
        s2sec = S2Section.objects.filter(subsection__in=subsection)
        gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=request.GET['c_id'])
        comp = list(subsection.filter(s2section=None).values_list('item',flat=True))+ list(s2sec.values_list('item',flat=True))
        data = get_company_data(gbc_data,req_type='Balance Sheet')

        return render(request, 'AutomationUI/bs_data.html', locals())

    def post(self, request, *args, **kwargs):
        arg = self.args
        data = dict(request.POST)
        new_data =OrderedDict()

        new_data['section']=remake_dict('section','sec_',data)
        new_data['subsection'] = remake_dict('subsection','s1_',data)
        new_data['s2section'] = remake_dict('s2section', 's2_', data)
        gbc_data =CompanyBalanceSheetData.objects.filter(gbc_name_id=1)
        return Response({'status': 'success'})

def add_row(request):
    new_row=OrderedDict()
    g_data =dict(request.GET)

    r_type = 'Profit and Loss' if g_data['type'][0]=='pnl' else 'Balance Sheet'
    l1 =['q1','q2','q3','q4','y1','y2','y3','y4']
    if g_data['type'][0] != 'pnl':
        gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=request.GET['c_id'])
    else:
        gbc_data = CompanyPNLData.objects.filter(gbc_name_id=request.GET['c_id'])

    data = get_company_data(gbc_data,req_type=r_type)
    new_data = g_data['new_row[]']
    new_row[new_data[0]]=OrderedDict(zip(l1, new_data[1:]))
    data[g_data['section'][0]][g_data['subsection'][0]].update(new_row)
    data = save_data(data, request.GET['c_id'],g_data['type'][0])
    if g_data['type'][0] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())

def delete_row(request):
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'
    if g_data['type'] != 'pnl':
        gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=request.GET['c_id'])
    else:
        gbc_data = CompanyPNLData.objects.filter(gbc_name_id=request.GET['c_id'])

    # gbc_data = CompanyBalanceSheetData.objects.filter(gbc_name_id=request.GET['c_id'])
    data = get_company_data(gbc_data,req_type=r_type)
    data[g_data['section']][g_data['subsection']].pop(g_data['item'])
    data = save_data(data, request.GET['c_id'],req_type=g_data['type'])
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
        section = Section.objects.filter(i_related ='Profit and Loss')
        subsection =SubSection.objects.filter(section__in =section)
        gbc_data = CompanyPNLData.objects.filter(gbc_name_id=request.GET['c_id'])
        comp = list(subsection.filter(s2section=None).values_list('item',flat=True))
        data = get_company_data(gbc_data,req_type='Profit and Loss')
        return render(request, 'AutomationUI/pnl.html', locals())

    def post(self, request, *args, **kwargs):
        arg = self.args
        data = dict(request.POST)
        new_data =OrderedDict()

        new_data['section']=remake_dict('section','sec_',data)
        new_data['subsection'] = remake_dict('subsection','s1_',data)
        new_data['s2section'] = remake_dict('s2section', 's2_', data)
        gbc_data =CompanyBalanceSheetData.objects.filter(gbc_name_id=1)
        return Response({'status': 'success'})



class UploadPDfView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(UploadPDfView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        sector_list = Sector.objects.all().values_list('sector_name',flat=True)
        c_year_end = list(year_end)
        p_type = list(pdf_type)

        return render(request, 'AutomationUI/upload_pdf.html', locals())

    def post(self, request, *args, **kwargs):
        from .upload_pdf import upload_pdf
        from DataExtraction.store_data import pdf_detail

        if request.method == 'POST':
            res,path= upload_pdf(request.FILES['file'], str(request.FILES['file']))
            if res:
                pdf_detail(c_name = request.POST['company_name'],sector = request.POST['sector'],year_end = request.POST['year_end'],
                           file = path,pdf_type =request.POST['pdf_type']
                           )
            else:
                return HttpResponse("Failed")
            return render(request, 'AutomationUI/upload_pdf.html', locals())


