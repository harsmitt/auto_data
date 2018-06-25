from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings as st

from AutomationUI.views import *
# from AutomationUI.upload_pdf import *
from AutomationUI.utils import update_comp
from AutomationUI.download_excel import download_pdf
from AutomationUI.download_dump import download_dump

urlpatterns = [
    url(r'^company_list/$', CompanyListView.as_view(), name='CompanylistForm'),
    url(r'^balance-sheet/$', BalanceSheetFormView.as_view(), name='balancesheetform'),
    url(r'^profit-loss/$', PNLFormView.as_view(), name='PNLFormViewform'),
    url(r'^ajax_update_component/$', update_comp, name='updatecomp'),
    url(r'^add_row/$', add_row, name='addrow'),
    url(r'^delete_row/$', delete_row, name='deleterow'),
    # url(r'^extract/$',upload_pdf, name='upload_pdf'),
    url(r'^upload_pdf/$', UploadPDfView.as_view(), name='upload_pdf'),
    url(r'^new_company/$', NewCompanyView.as_view(), name='new_company'),
    url(r'^download-pdf/$', download_pdf, name='download_pdf'),
    url(r'^download-dump/$', download_dump, name='download_dump'),
    url(r'^pnl_last_qtr/$', pnl_last_qtr, name='pnl_last_qtr'),
    url(r'^bs_last_qtr/$', bs_last_qtr, name='bs_last_qtr'),
# get_existing_date
    url(r'^get_existing_date/$', get_existing_date, name='get_existing_date'),
    url(r'^section_list/$', section_list, name='sectionlist'),
# /automation/extract_data/
    # url(r'^save_data/$', save_data, name='save_data'),
    ]
