#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from application import AppList,AppCreate,AppDetail

urlpatterns = [
    url(r'^app/detail/(?P<appname>.+)/$',AppDetail.as_view(),name='appdetail'),
    url(r'^app/list/$',AppList.as_view(),name='applist'),
    url(r'^app/add/$',AppCreate.as_view(),name='appcreate'),
    ]