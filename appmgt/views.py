#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月14日

@author: yangxu
'''
from django.views.generic import TemplateView

class AppDockerList(TemplateView):
    template_name = 'application/appDockerList.html'
    def get_context_data(self, **kwargs):
        context = super(AppDockerList, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['hosts'] = [
        {'id':'portal01','name':'Portal门户','net':'bridge','cpu':'2','memory':'4','number':6,'port':31230,'status':'pub'},
        {'id':'web01','name':'bb前端','net':'bridge','cpu':'2','memory':'4','number':3,'port':31231,'status':'unpub'}]
        return context
    
class AppDockerCreate(TemplateView):
    template_name = 'application/appDockerCreate.html'
    def get_context_data(self, **kwargs):
        context = super(AppDockerCreate, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class AppDockerDetail(TemplateView):
    template_name = 'application/appDockerDetail.html'
    def get_context_data(self, **kwargs):
        context = super(AppDockerDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['appname'] = kwargs['appname']
        return context
    
class AppDaemonList(TemplateView):
    template_name = 'application/appDaemonList.html'
    def get_context_data(self, **kwargs):
        context = super(AppDaemonList, self).get_context_data(**kwargs)
        return context
    
class AppDaemonCreate(TemplateView):
    template_name = 'application/appDaemonCreate.html'
    def get_context_data(self, **kwargs):
        context = super(AppDaemonCreate, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class AppDaemonDetail(TemplateView):
    template_name = 'application/appDaemonDetail.html'
    def get_context_data(self, **kwargs):
        context = super(AppDaemonDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['appname'] = kwargs['appname']
        return context