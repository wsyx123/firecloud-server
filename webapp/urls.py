"""firecloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from login import login,logout
from home.index import Index
# from django.contrib import admin

urlpatterns = [
#     url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(),name='dashboard'),
    url(r'^login/$',login),
    url(r'^logout/$',logout,name='logout'),
    url(r'',include('webapp.asset.urls')),
    url(r'',include('webapp.celery_task.urls')),
    url(r'',include('webapp.task.urls')),
    url(r'',include('webapp.paas.urls')),
    url(r'',include('webapp.application.urls')), 
    url(r'',include('webapp.monitor.urls')),
    url(r'',include('webapp.log_center.urls')), 
    url(r'',include('webapp.store.urls')),
    url(r'',include('webapp.sys_manage.urls')), 
]
