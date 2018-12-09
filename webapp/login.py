# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import SysUser
from django.shortcuts import HttpResponseRedirect,render
import time
# Create your views here.

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
        

