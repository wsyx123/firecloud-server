#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月22日

@author: yangxu
'''
from django.views.generic import TemplateView

class WebList(TemplateView):
    template_name = 'store/web/webList.html'

class WebCreate(TemplateView):
    template_name = 'store/web/webCreate.html'
    def get(self, request, *args, **kwargs):
        print request.GET.get('type')
        return TemplateView.get(self, request, *args, **kwargs)

class WebDetail(TemplateView):
    template_name = 'store/web/webDetail.html'
    
class LogicList(TemplateView):
    template_name = 'store/logic/logicList.html'
    
class StorageList(TemplateView):
    template_name = 'store/storage/storageList.html'