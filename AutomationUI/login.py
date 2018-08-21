from Login.models import *
from DataExtraction.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_dit_list(request,*args):
    if request.method=='POST' and 'username' in request.POST:
        user_obj = TeamList.objects.filter(t_user__username = request.POST['username']).values_list('team_name__team_name',flat=True)

    else:
        user_obj = TeamList.objects.filter(t_user__username=request.user.username).values_list(
            'team_name__team_name', flat=True)
    sectors = Team_Sector.objects.filter(team__team_name__in = user_obj).values_list('sector_description',flat=True)
    all_dit = SectorDit.objects.filter(team_sector__sector_description__in = sectors).values_list('id',flat=True)
    data_exists = CompanyList.objects.filter(ditname_id__in = all_dit).values_list('ditname_id',flat=True).distinct()
    dit_list = SectorDit.objects.filter(id__in=data_exists)
    return TemplateResponse(request, 'AutomationUI/dit_list.html', locals())


@csrf_exempt
def user_login(request):
    print (request.POST)
    if request.method == "POST":
        user_info = User.objects.filter(username = request.POST['username'])
        if user_info:
            user = authenticate(username=user_info[0].username, password=request.POST['password'])
        else:
            return TemplateResponse(request, 'AutomationUI/login.html', locals())

        if user is not None:
            login(request, user)
            request.session['user'] = request.POST['username']
            return HttpResponseRedirect(reverse('get_dit_list'))

        else:
            errors ='Please enter a valid password'
            authentication_error = True

    return TemplateResponse(request, 'AutomationUI/login.html', locals())
from django.core.urlresolvers import reverse

@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('uilogin'))



def dit_list(request):
    print (request.GET['sector'])
    sector_list = list(SectorDit.objects.filter(sector__sector_name = request.GET['sector']).values_list('dit_name',flat=True))
    sector_list = ('##').join(sector_list)

    return HttpResponse(sector_list)



def change_password(request,user_name=None):
    flag=1
    if request.method =='POST':
        user = User.objects.get(username=request.user.username)
        if user.check_password(request.POST['old_password']):
            if request.POST['new_password'] == request.POST['confirm_password']:
                user.set_password(request.POST['new_password'])
                user.save()
                # get_dit_list(request)
                return HttpResponseRedirect(reverse('uilogin'))
            else:
                flag = 0
    return TemplateResponse(request, 'AutomationUI/change_password.html', locals())
