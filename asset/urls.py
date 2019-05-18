#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import AssetView,HostList,HostAdd,HostUpdate,HostDelete,host_import,HostDetail,\
                  get_import_result,host_refresh
from views import AccountList
from views import GroupList,GroupAdd,GroupUpdate,GroupDelete
from views import asset_connect
from views import AgentRegister,AgentHeartbeat,HostMonitor,HostStatus

urlpatterns = [
    url(r'^asset/list/$', AssetView.as_view(),name='AssetView'),
    url(r'^host/list/$', HostList.as_view(),name='HostList'),
    url(r'^host/add/$', HostAdd.as_view(),name='HostAdd'),
    url(r'^host/ssh/$',asset_connect,name='HostLogin'),
    url(r'^host/import/result/$', get_import_result),
    url(r'^host/import/$', host_import,name='HostImport'),
    url(r'^host/update/(?P<pk>.+)$', HostUpdate.as_view(),name='HostUpdate'),
    url(r'^host/refresh/$', host_refresh,name='HostRefresh'),
    url(r'^host/delete/(?P<pk>.+)$', HostDelete.as_view(),name='HostDelete'),
    url(r'^host/detail/(?P<pk>.+)$', HostDetail.as_view(),name='HostDetail'),
    url(r'^account/list/$', AccountList.as_view(),name='AccountList'),
    url(r'^group/list/$', GroupList.as_view(),name='GroupList'),
    url(r'^group/add/$', GroupAdd.as_view(),name='GroupAdd'),
    url(r'^group/update/(?P<pk>.+)$', GroupUpdate.as_view(),name='GroupUpdate'),
    url(r'^group/delete/(?P<pk>.+)$', GroupDelete.as_view(),name='GroupDelete'),
    url(r'^agent/register/$',AgentRegister.as_view()),
    url(r'^agent/heartbeat/$',AgentHeartbeat.as_view()),
    url(r'^host/monitor/$',HostMonitor.as_view()),
    url(r'^host/status/$',HostStatus.as_view())
    ]