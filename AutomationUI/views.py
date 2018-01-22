from rest_framework.views import APIView, Response
from DataExtraction.models import *
from .forms import *
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
from .utils import *

class CompanyListView(APIView):
    template_name = 'AutomationUI/index.html'

    def dispatch(self, *args, **kwargs):
        return super(CompanyListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        data=CompanyList.objects.all().values()
        return render(request, 'AutomationUI/index.html', locals())

class BalanceSheetFormView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = GbcData.objects

    def dispatch(self, *args, **kwargs):
        return super(BalanceSheetFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        data=OrderedDict()
        section = Section.objects.filter(i_related ='Balance Sheet')
        subsection =SubSection.objects.filter(section__in =section)
        s2sec = S2Section.objects.filter(subsection__in=subsection)
        gbc_data = GbcData.objects.filter(gbc_name_id=request.GET['c_id'])
        comp = list(subsection.filter(s2section=None).values_list('item',flat=True))+ list(s2sec.values_list('item',flat=True))
        data = get_company_data(gbc_data)

        return render(request, 'AutomationUI/bs_data.html', locals())

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        arg = self.args
        data = dict(request.POST)
        new_data =OrderedDict()

        new_data['section']=remake_dict('section','sec_',data)
        new_data['subsection'] = remake_dict('subsection','s1_',data)
        new_data['s2section'] = remake_dict('s2section', 's2_', data)
        gbc_data =GbcData.objects.filter(gbc_name_id=1)
        return Response({'status': 'success'})

def add_row(request):
    new_row=OrderedDict()
    g_data =dict(request.GET)
    l1 =['q1','q2','q3','q4','y1','y2','y3','y4']
    gbc_data = GbcData.objects.filter(gbc_name_id=request.GET['c_id'])
    data = get_company_data(gbc_data)
    new_data = g_data['new_row[]']
    new_row[new_data[0]]=OrderedDict(zip(l1, new_data[1:]))
    data[g_data['section'][0]][g_data['subsection'][0]].update(new_row)
    data = save_data(data, request.GET['c_id'])
    return render(request, 'AutomationUI/bs_data.html', locals())

def delete_row(request):
    g_data = OrderedDict(request.GET)
    gbc_data = GbcData.objects.filter(gbc_name_id=request.GET['c_id'])
    data = get_company_data(gbc_data)
    data[g_data['section']][g_data['subsection']].pop(g_data['item'])
    data = save_data(data, request.GET['c_id'])
    return render(request, 'AutomationUI/bs_data.html', {'data': data})




