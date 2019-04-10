#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import ListTask,AddTask,UpdateTask,DeleteTask,FlowerMonitor
from views import ListCrontab,AddCrontab,UpdateCrontab,DeleteCrontab
from views import ListInterval,AddInterval,UpdateInterval,DeleteInterval

urlpatterns = [
    url(r'^task/flower/$',FlowerMonitor.as_view(),name='FlowerMonitor'),
    url(r'^task/list/$',ListTask.as_view(),name='ListTask'),
    url(r'^task/add/$',AddTask.as_view(),name='AddTask'),
    url(r'^task/update/(?P<pk>.+)$',UpdateTask.as_view(),name='UpdateTask'),
    url(r'^task/delete/(?P<pk>.+)$',DeleteTask.as_view(),name='DeleteTask'),
    url(r'^crontab/list/$',ListCrontab.as_view(),name='ListCrontab'),
    url(r'^crontab/add/$',AddCrontab.as_view(),name='AddCrontab'),
    url(r'^crontab/update/(?P<pk>.+)$',UpdateCrontab.as_view(),name='UpdateCrontab'),
    url(r'^crontab/delete/(?P<pk>.+)$',DeleteCrontab.as_view(),name='DeleteCrontab'),
    url(r'^interval/list/$',ListInterval.as_view(),name='ListInterval'),
    url(r'^interval/add/$',AddInterval.as_view(),name='AddInterval'),
    url(r'^interval/update/(?P<pk>.+)$',UpdateInterval.as_view(),name='UpdateInterval'),
    url(r'^interval/delete/(?P<pk>.+)$',DeleteInterval.as_view(),name='DeleteInterval')
    ]