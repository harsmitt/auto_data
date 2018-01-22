from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings as st

from AutomationUI.views import *
from AutomationUI.utils import update_comp

urlpatterns = [
    url(r'^company_list/$', CompanyListView.as_view(), name='CompanylistForm'),
    url(r'^balance-sheet/$', BalanceSheetFormView.as_view(), name='balancesheetform'),
    url(r'^ajax_update_component/$', update_comp, name='updatecomp'),
    url(r'^add_row/$', add_row, name='addrow'),
    url(r'^delete_row/$', delete_row, name='deleterow'),
    # url(r'^save_data/$', save_data, name='save_data'),
    ]
