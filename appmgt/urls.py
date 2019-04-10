#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import AppDockerList,AppDockerCreate,AppDockerDetail
from views import AppDaemonList,AppDaemonCreate,AppDaemonDetail

urlpatterns = [
    url(r'^appDocker/detail/(?P<appname>.+)/$',AppDockerDetail.as_view(),name='AppDockerDetail'),
    url(r'^appDocker/list/$',AppDockerList.as_view(),name='AppDockerList'),
    url(r'^appDocker/add/$',AppDockerCreate.as_view(),name='AppDockerCreate'),
    
    url(r'^appDaemon/detail/(?P<appname>.+)/$',AppDaemonDetail.as_view(),name='AppDaemonDetail'),
    url(r'^appDaemon/list/$',AppDaemonList.as_view(),name='AppDaemonList'),
    url(r'^appDaemon/add/$',AppDaemonCreate.as_view(),name='AppDaemonCreate'),
    ]