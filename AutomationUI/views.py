from rest_framework.views import APIView, Response
from .forms import *
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
from .utils import *
from DataExtraction.models import *
from Login.models import *
from DataExtraction.choices import year_end,pdf_type
from django.core.cache import cache

from .tranform_data import get_data,get_delete_data

class CompanyListView(APIView):
    template_name = 'AutomationUI/index.html'

    def dispatch(self, *args, **kwargs):
        return super(CompanyListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.username:
            data=CompanyList.objects.filter(ditname_id = request.GET['dit_id']).values()
            return render(request, 'AutomationUI/index.html', locals())
        else:
            return render(request, 'AutomationUI/login.html', locals())

class BalanceSheetFormView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(BalanceSheetFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.username:
            data_list,date_list,loop_key = get_data(req_type='bsheet',c_id=request.GET['c_id'],section_type='Balance Sheet')
            p_type = 'Balance Sheet'
            c_obj = CompanyList.objects.get(id=request.GET['c_id'])
            unit = c_obj.c_y_unit.split('##')[1]
            return render(request, 'AutomationUI/bs_data.html', locals())
        else:
            return render(request, 'AutomationUI/login.html', locals())

    def post(self, request, *args, **kwargs):
        return Response({'status': 'success'})



def add_row(request):
    new_row=OrderedDict()
    g_data =dict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'][0]=='pnl' else 'Balance Sheet'
    c_obj = CompanyList.objects.filter(id=request.GET['c_id']).values_list('y_end', flat=True)
    date_objs = qtr_date(c_obj[0])
    date_objs.update(year_date(c_obj[0]))
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
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'],req_type=r_type,p_type=req_type,action_type='save')
    else:
        pass
    if 'action' in request.GET:
        x = delete_row(request)
    # data = save_data(data, request.GET['c_id'],g_data['type'][0])
    if g_data['type'][0] == 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())



def add_delete_row(**kwargs):
    data=OrderedDict()
    sec_obj = Section.objects.get(item = kwargs['section'])
    data['section']=sec_obj
    sub_obj = SubSection.objects.get(item=kwargs['subsection'])
    data['subsection']=sub_obj
    s2_obj = S2Section.objects.get(item=kwargs['s2sec']) if kwargs['s2sec'] else None
    data['s2section'] = s2_obj
    data['company_name_id'] = kwargs['c_id']
    data['page_extraction'] = kwargs['type']
    # data['quarter_date'] = kwargs['loop_key']
    # data['description'] =
    if type(kwargs['row'])==OrderedDict:
        for loop1 , loop2 in kwargs['row'][kwargs['item']].items():
            data['quarter_date'] = kwargs['loop_key'][loop1]
            exist_obj = DeleteRow.objects.filter(quarter_date =  kwargs['loop_key'][loop1],
                                                 section =sec_obj,subsection=sub_obj,s2section=s2_obj)
            if exist_obj:
                des = exist_obj[0].description +'##'+kwargs['item']+'('+str(loop2)+')'
                dict1 = {'description':des}
                x = exist_obj.update(**dict1)
            else:
                data['description']  =kwargs['item']+'('+str(loop2)+')'
                x = DeleteRow.objects.create(**data)
    else:
        for s2 in kwargs['row']:
            for  s2_k,s2_v in s2.items():
                if kwargs['item'] in s2[s2_k]:
                    for loop1, loop2 in s2[s2_k][kwargs['item']].items():
                        data['quarter_date'] = kwargs['loop_key'][loop1]
                        exist_obj = DeleteRow.objects.filter(quarter_date=kwargs['loop_key'][loop1],
                                                             section=sec_obj, subsection=sub_obj, s2section=s2_obj)
                        if exist_obj:
                            des = exist_obj[0].description + '##' + kwargs['item'] + '(' + str(loop2) + ')'
                            dict1 = {'description': des}
                            x = exist_obj.update(**dict1)
                        else:
                            data['description'] = kwargs['item'] + '(' + str(loop2) + ')'
                            x = DeleteRow.objects.create(**data)
            else:
                pass

    if x : return True
    else :return False

def delete_row(request):
    g_data = OrderedDict(request.GET)
    r_type = 'Profit and Loss' if g_data['type'] == 'pnl' else 'Balance Sheet'
    req_type = 'pnl' if g_data['type'] =='pnl' else 'bsheet'
    if cache.has_key(request.GET['c_id']) and not 'action' in request.GET:
        cache_dict = cache.get(request.GET['c_id'])
        if req_type in cache_dict:
            data_list = cache_dict[req_type]
            date_list = cache_dict['date_list']
            loop_key = cache_dict['loop_key']
        else:
            data_list, date_list, loop_key = get_data(req_type=req_type, section_type=r_type, c_id=request.GET['c_id'])
    elif not 'action' in request.GET:
        data_list, date_list, loop_key = get_data(req_type=req_type,section_type=r_type, c_id=request.GET['c_id'])

    else:
        data_list, date_list, loop_key = get_delete_data(c_id=request.GET['c_id'])

    deleted_row =False
    for data in data_list:
        if g_data['section'] in list(data.keys()) and not deleted_row:
            for i in data[g_data['section']]:
                if not deleted_row:
                    for key, val in i.items():
                        if type(val)!=list  and key == g_data['subsection'] :
                            for d_key, d_val in val.items():
                                if d_key == g_data['item']:
                                    if not 'action' in request.GET:
                                        res= add_delete_row(row = i[key],section = g_data['section'],item=g_data['item'],
                                                       subsection =g_data['subsection'],type= req_type,s2sec=None,
                                                       c_id =request.GET['c_id'],loop_key=loop_key )

                                    i[key].pop(g_data['item'])
                                    i['update'] = True
                                    deleted_row=True
                                    break;

                        elif key == g_data['subsection'] and 's2sec' in g_data:
                            for s2sec in val:
                                for s2, s2_o in s2sec.items():
                                    if s2 == g_data['s2sec']:
                                        if not 'action' in request.GET:
                                            res = add_delete_row(row=s2sec[s2], section=g_data['section'], item=g_data['item'],
                                                             subsection=g_data['subsection'], type=req_type, s2sec=g_data['s2sec'],
                                                             c_id=request.GET['c_id'], loop_key=loop_key)

                                        s2sec[s2].pop(g_data['item'])
                                        i['update'] = True
                                        deleted_row = True
                                        break;
                elif deleted_row:
                    break;

        elif deleted_row:
            break;
    data = [i for i in data_list if g_data['section'] in list(i.keys())]
    action_type = 'undo' if 'action' in request.GET else 'delete'
    if data:
        data_list, date_list, loop_key = save_data(data[0], request.GET['c_id'],req_type=r_type,action_type=action_type,p_type= req_type)
    else:
        pass
    if g_data['type']== 'pnl':
        return render(request, 'AutomationUI/pnl.html', locals())
    else:
        return render(request, 'AutomationUI/bs_data.html', locals())
    # return render(request, 'AutomationUI/bs_data.html', {'data': data})

def get_qtrs(c_obj):
    c_m= datetime.strptime(c_obj.y_end, '%B').month
    if c_m in [11,12,1]:
        q2 = 'june'
        q3 ='september'
    elif c_m in [2,3,4]:
        q2 = 'september'
        q3 ='december'
    elif c_m in [5,6,7]:
        q2 ='december'
        q3= 'march'
    else:
        q2 ='march'
        q3='june'
    return q2,q3

class PNLFormView(APIView):
    template_name = 'AutomationUI/pnl.html'
    queryset = CompanyPNLData.objects

    def dispatch(self, *args, **kwargs):
        return super(PNLFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.username:

            data=OrderedDict()
            p_type=  'Profit and Loss'
            c_obj = CompanyList.objects.get(id=request.GET['c_id'])
            q2,q3 = get_qtrs(c_obj)
            unit = c_obj.c_y_unit.split('##')[1]
            data_list, date_list, loop_key = get_data(req_type='pnl',section_type = 'Profit and Loss', c_id=request.GET['c_id'])
            return render(request, 'AutomationUI/pnl.html', locals())
        else:
            return render(request, 'AutomationUI/login.html', locals())
    def post(self, request, *args, **kwargs):
        return Response({'status': 'success'})


def get_file_sorted(files,p_type):
    try:
        if p_type == 'year':
            k_list = list(files.keys())
            f_name = y_sorting(k_list)
        else:
            k_list = list(files.keys())
            f_name = q_sorting(k_list)
            f_name = [name.replace(' ','_') for name in f_name]
        return f_name
    except Exception as e:
        return e


##Save uploaded pdf in a folder and start processing it one by one.
class UploadPDfView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = CompanyBalanceSheetData.objects

    def dispatch(self, *args, **kwargs):
        return super(UploadPDfView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.username:
            msg="Upload a File"
            status =''
            # sector_list = Sector.objects.all().values_list('sector_name',flat=True)

            c_year_end = list(year_end)
            user_obj = TeamList.objects.filter(t_user__username=request.user.username).values_list(
                'team_name__team_name', flat=True)
            sectors = Team_Sector.objects.filter(team__team_name__in=user_obj).values_list('sector_description', flat=True)
            all_dit = SectorDit.objects.filter(team_sector__sector_description__in=sectors)
            p_type = list(pdf_type)

            return render(request, 'AutomationUI/upload_pdf.html', locals())
        else:
            return render(request, 'AutomationUI/login.html', locals())

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            # sector_list = Sector.objects.all().values_list('sector_name', flat=True)
            status =[]
            c_year_end = list(year_end)
            user_obj = TeamList.objects.filter(t_user__username=request.user.username).values_list(
                'team_name__team_name', flat=True)
            sectors = Team_Sector.objects.filter(team__team_name__in=user_obj).values_list('sector_description',
                                                                                           flat=True)
            all_dit = SectorDit.objects.filter(team_sector__sector_description__in=sectors)
            c_year_end = list(year_end)
            p_type = list(pdf_type)
            files= get_file_sorted(files= request.FILES,p_type=request.POST['pdf_type'])
            import multiprocessing
            from multiprocessing import Process,Queue,Pool
            # pool =Pool(10)
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            jobs=[]
            for file_name in files:
                f_name= request.FILES[str(file_name)]
                # result = upload(f_name,request.POST['company_name'],f_name.name,request.POST)
                # status.append(result)
                p = Process(target = upload,args=(f_name,request.POST['company_name'],f_name.name,request.POST,return_dict))
                p.start()
                p.join()
            print (return_dict)

            return render(request, 'AutomationUI/upload_pdf.html', locals())


def upload(f_name,c_name,name,post_data,return_dict):
    from .upload_pdf import upload_pdf
    from DataExtraction.store_data import pdf_detail
    #function save pdf into uploads folder
    res, path = upload_pdf(file_1=f_name, c_name=c_name, file_n=str(name))
    if res:
        data_dict = copy.deepcopy(post_data)
        data_dict = dict(data_dict)
        sector_name= SectorDit.objects.get(dit_name= post_data['dit_name'])
        if not 'override' in data_dict:
            data_dict['override'] = []
        page_num = OrderedDict({'bs_num':post_data['bs_pnum'],'pnl_num':post_data['pnl_pnum']})

        # calling this function to extract the pdf
        # file_status = OrderedDict()


        result = pdf_detail(c_name=post_data['company_name'], sector=sector_name.sector.sector_name,
                            year_end=post_data['year_end'],dit_name= post_data['dit_name'],
                            file=path, pdf_type=post_data['pdf_type'],page_num=page_num,
                            override=data_dict['override']
                            )
        if len(result)==2:
            msg = "Uploaded"
        elif len(result) ==1:
            if 'pnl'in result:
                msg="Balance sheet not extracted"
            else:
                msg="pnl not extracted"
        else:
            msg="Error in File Uploading"

        return_dict[name]=msg
        # return file_status

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
            try:
                res = test(c_name = request.POST['company_name'],
                       year_end = request.POST['year_end'],c_ticker = request.POST['company_ticker']
                             )
                from twisted.internet import reactor, defer
                if reactor.running:reactor.stop()
            except Exception as e:
                import traceback
                print (traceback.format_exc())
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
    from django.db.models import Q
    c_obj = CompanyList.objects.filter(company_name=request.GET['c_name'])
    if c_obj:
        q_date = list(quarter_data.objects.filter(Q(company_name=c_obj), ~Q(q1=0)).values_list('quarter_date',
                                                                                          flat=True).distinct())
        q_date = '##'.join(q_date)
        return HttpResponse(q_date)
    else:
        return HttpResponse("This is a new company")


def section_list(request):
    r_type = "Balance Sheet" if request.GET['type'] =='balance-sheet' else 'Profit and Loss'
    section = Section.objects.filter(i_related=r_type)
    comp=''
    for ind , sec in enumerate(section):
        subsection = SubSection.objects.filter(section=sec)
        s2sec = S2Section.objects.filter(subsection__in=subsection)
        comp += '##'.join(list(subsection.filter(s2section=None).values_list('item', flat=True)))+'##' + '##'.join(list(
        s2sec.values_list('item', flat=True)))
        if ind+1 < len(section):
            comp+='##'
    return HttpResponse(comp)


# def DeletedRows(request):



class DeletedRowsFormView(APIView):
    template_name = 'AutomationUI/bs_data.html'
    queryset = DeleteRow.objects

    def dispatch(self, *args, **kwargs):
        return super(DeletedRowsFormView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        delete_objs = DeleteRow.objects.filter(company_name_id=request.GET['c_id'])
        data_list, date_list, loop_key = get_delete_data(c_id=request.GET['c_id'])
        p_type = 'Balance Sheet'
        c_obj = CompanyList.objects.filter(id=request.GET['c_id'])[0]
        return render(request, 'AutomationUI/delete_rows.html', locals())
        # return render(request, 'AutomationUI/delte.html', locals())

    def post(self, request, *args, **kwargs):
        return Response({'status': 'success'})
