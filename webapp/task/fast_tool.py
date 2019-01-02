#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月3日 下午6:56:43
@author: yangxu
'''

from django.views.generic import TemplateView

class FastToolList(TemplateView):
    template_name = 'task/fastTool/fastToolList.html'