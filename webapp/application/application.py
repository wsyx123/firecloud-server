#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月14日

@author: yangxu
'''
from django.views.generic import TemplateView

class AppList(TemplateView):
    template_name = 'application/appList.html'
    def get_context_data(self, **kwargs):
        context = super(AppList, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['hosts'] = [
        {'id':'portal01','name':'Portal门户','net':'bridge','cpu':'2','memory':'4','number':6,'port':31230,'status':'pub'},
        {'id':'web01','name':'bb前端','net':'bridge','cpu':'2','memory':'4','number':3,'port':31231,'status':'unpub'}]
        return context
    
class AppCreate(TemplateView):
    template_name = 'application/appCreate.html'
    def get_context_data(self, **kwargs):
        context = super(AppCreate, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class AppDetail(TemplateView):
    template_name = 'application/appDetail.html'
    def get_context_data(self, **kwargs):
        context = super(AppDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['appname'] = kwargs['appname']
        return context