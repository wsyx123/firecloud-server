#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年11月4日

@author: yangxu
'''
from webapp.models import HomePage,SysUser,SysRole
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from get_home_page import get_home_page

class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        userid = request.session['_user_id']
        userobj = SysUser.objects.get(id=userid)
        roleid = userobj.role_id
        roleobj = SysRole.objects.get(id=roleid)
        homepageid = roleobj.home_page_id
        if homepageid:
            homepageobj = HomePage.objects.get(id=homepageid)
            self.template_name = homepageobj.template_name
            return TemplateView.get(self, request, *args, **kwargs)
        else:
            home_url = get_home_page(userid)
            return HttpResponseRedirect(home_url)
    
    
    