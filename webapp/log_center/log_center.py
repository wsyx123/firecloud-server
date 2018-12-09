#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.views.generic import TemplateView

class UserMgt(TemplateView):
    template_name = 'sys_manage/UserMgt.html'
    
class RoleMgt(TemplateView):
    template_name = 'sys_manage/RoleMgt.html'