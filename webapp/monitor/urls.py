#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from monitor import AppMonitor,AppMonitorDetail,AppMonitorFullScreen,HostMonitor,HostMonitorDetail,\
EventList,AlertPolicyList,AlertPolicyAdd,ReceiveGroupList,ReceiveGroupAdd

urlpatterns = [
    url(r'appMonitor/(?P<appname>.+)/$',AppMonitorDetail.as_view(),name='appmonitordetail'),
    url(r'appMonitor/$',AppMonitor.as_view(),name='appmonitor'),
    url(r'fullscreen/$',AppMonitorFullScreen.as_view(),name='fullscreen'),
    
    url(r'hostMonitor/(?P<hostname>.+)/$',HostMonitorDetail.as_view(),name='hostmonitordetail'),
    url(r'hostMonitor/$',HostMonitor.as_view(),name='hostmonitor'),
    
    url(r'receiveGroup/list/$',ReceiveGroupList.as_view(),name='receivegrouplist'),
    url(r'receiveGroup/add/$',ReceiveGroupAdd.as_view(),name='receivegroupadd'),
    url(r'event/list/$',EventList.as_view(),name='eventlist'),
    url(r'alertPolicy/list/$',AlertPolicyList.as_view(),name='alertpolicylist'),
    url(r'alertPolicy/add/$',AlertPolicyAdd.as_view(),name='alertpolicyadd'),
    ]