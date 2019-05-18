#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年11月4日

@author: yangxu
'''
from sysmgt.models import  HomePage,SysUser,SysRole
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect,render
from get_home_page import get_home_page
import time
import json

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

def login(request):
    error_messages = ''
    if  request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
    
        res_name_auth = SysUser.objects.filter(username=username)
        if len(res_name_auth) == 0:
            error_messages = '{} 用户不存在!'.format(username)
        elif not res_name_auth[0].role:
            error_messages = '{} 用户未分配角色!'.format(username)
        else:
            res_pass_auth = SysUser.objects.filter(username=username,password=password)
            if len(res_pass_auth) == 0:
                error_messages = '密码错误，请重新输入!'
            else:
                res_status_auth = SysUser.objects.filter(username=username,password=password,status=1)
                if len(res_status_auth) == 0:
                    error_messages = '{} 用户状态不可用!'.format(username)
                else:
                    res = SysUser.objects.get(username=username,password=password,status=1)
                    request.session['_user_id'] = res.id 
                    res.last_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    res.save()
                    return HttpResponseRedirect('/')     
    return render(request,'base/login.html',{'err_msg':error_messages})
            
    

def logout(request):
    del request.session['_user_id']
    return HttpResponseRedirect("/login")
    
    
    