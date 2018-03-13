"""DataAutomation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve
# from django.contrib import admin
from django.conf.urls.static import static
from django.contrib import admin
# from DataExtraction.admin import show_image,submit
from django.conf import settings as st

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #     {'document_root': st.MEDIA_ROOT}),
    #
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #     {'document_root': st.STATIC_ROOT}),

    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': st.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': st.STATIC_ROOT}),
    url(r'^automation/', include('AutomationUI.urls')),
    # url(r'^show_image/', show_image),

    # url(r'^submit/', submit),


]+ static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
