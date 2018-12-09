#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月25日

@author: yangxu
'''

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect,HttpResponse
from webapp.models import SysUser,Level2Menu,Menu_Role_rel

class AuthLogin(MiddlewareMixin):
    def process_request(self,request):
        #未登录 请求其它页面( no session and  other url ) ->  转到login页面
        if not request.session.has_key('_user_id') and 'login' not in request.path:
            return HttpResponseRedirect('/login/')
        
        #已登录  请求登录页面( have session and login url ) ->  转到index    
        elif request.session.has_key('_user_id') and 'login' in request.path:
            return HttpResponseRedirect('/')
        
        #已登录 请求其它页面( have session and other url ) ->  url 判断->  (pass or denied)
        if request.session.has_key('_user_id') and 'logout' not in request.path:
            # url 判断
            if request.path == '/':
                pass
            elif request.session['_user_id'] != 1 and 'favicon.ico' not in request.path:
                if not url_acl(request.path, request.session['_user_id']):
                    return HttpResponse('Forbidden')
            
        ''' 未登录   请求登录页面( no session and  Login url ) 已登录  请求登出页面( no session and  Logout url ) 这两种情况都不处理，即放行
        '''
    def process_template_response(self,request,response):
        UserObj = SysUser.objects.get(id=request.session['_user_id'])
        request.session['user_id']=request.session['_user_id']
        response.context_data['username'] = UserObj.username
        response.context_data['roleid'] = UserObj.role_id
        response.context_data['path'] = request.path
        return response

    def process_response(self, request, response):
        return response

def url_acl(url,userid):
    url_list = url.split('/')
    url1 = '/'+url_list[1]+'/'
    url2 = '/'+url_list[1]+'/list/'
    level2obj1 = Level2Menu.objects.filter(url=url1)
    level2obj2 = Level2Menu.objects.filter(url=url2)
    if len(level2obj1) == 0:
        level2obj = level2obj2[0]
    else:
        level2obj = level2obj1[0]
    UserObj = SysUser.objects.get(id=userid)
    menu_role_obj = Menu_Role_rel.objects.filter(role_id=UserObj.role_id,level_2_menu_id=level2obj.id)
    if len(menu_role_obj) == 0:
        return False
    else:
        if url_list[2] == 'list' and menu_role_obj[0].view == 1:
            return True
        elif url_list[2] == 'add' and menu_role_obj[0].create == 1:
            return True
        elif url_list[2] == 'update' and menu_role_obj[0].update == 1:
            return True
        elif url_list[2] == 'delete' and menu_role_obj[0].delete == 1:
            return True
        else:
            return False
    
            
                
        
    