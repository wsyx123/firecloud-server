#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import AppMonitorList,AppMonitorDetail,AppMonitorFullScreen,HostMonitorList,HostMonitorDetail,\
EventList,AlertPolicyList,AlertPolicyAdd,ReceiveGroupList,ReceiveGroupAdd,ThirdComponentList,\
ThirdComponentZabbixAdd,ThirdComponentDeploy,ThirdComponentDetail

urlpatterns = [
    url(r'thirdComponent/list/$',ThirdComponentList.as_view(),name='thirdComponentList'),
    url(r'thirdComponent/zabbix/add/$',ThirdComponentZabbixAdd.as_view(),name='zabbixAdd'),
    url(r'thirdComponent/deploy/$',ThirdComponentDeploy),
    url(r'thirdComponent/detail/(?P<pk>.+)$',ThirdComponentDetail.as_view(),name='thirdComponentDetail'),
    
    url(r'appMonitor/list/(?P<appname>.+)/$',AppMonitorDetail.as_view(),name='appmonitordetail'),
    url(r'appMonitor/list/$',AppMonitorList.as_view(),name='appmonitor'),
    url(r'fullscreen/$',AppMonitorFullScreen.as_view(),name='fullscreen'),
    
    url(r'hostMonitor/list/(?P<hostname>.+)/$',HostMonitorDetail.as_view(),name='hostmonitordetail'),
    url(r'hostMonitor/list/$',HostMonitorList.as_view(),name='hostmonitor'),
    
    url(r'receiveGroup/list/$',ReceiveGroupList.as_view(),name='receivegrouplist'),
    url(r'receiveGroup/add/$',ReceiveGroupAdd.as_view(),name='receivegroupadd'),
    url(r'event/list/$',EventList.as_view(),name='eventlist'),
    url(r'alertPolicy/list/$',AlertPolicyList.as_view(),name='alertpolicylist'),
    url(r'alertPolicy/add/$',AlertPolicyAdd.as_view(),name='alertpolicyadd'),
    ]