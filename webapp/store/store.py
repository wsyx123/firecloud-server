#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月22日

@author: yangxu
'''
from django.views.generic import TemplateView

class ListWeb(TemplateView):
    template_name = 'store/web.html'
    
class ListLogic(TemplateView):
    template_name = 'store/logic.html'
    
class ListStorage(TemplateView):
    template_name = 'store/storage.html'