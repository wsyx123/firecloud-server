#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from sys_manage import UserMgt,RoleMgt,RoleAdd,UserAdd,UserUpdate,UserDelete,RoleUpdate,RoleDelete

urlpatterns = [
    url(r'^UserMgt/list/$',UserMgt.as_view(),name='UserMgt' ),
    url(r'^UserMgt/add/$',UserAdd.as_view(),name='UserAdd' ),
    url(r'^UserMgt/update/(?P<pk>.+)$',UserUpdate.as_view(),name='UserUpdate' ),
    url(r'^UserMgt/delete/(?P<pk>.+)$',UserDelete.as_view(),name='UserDelete' ),
    url(r'^RoleMgt/list/$',RoleMgt.as_view(),name='RoleMgt' ), 
    url(r'^RoleMgt/add/$',RoleAdd.as_view(),name='RoleAdd' ),
    url(r'^RoleMgt/update/(?P<pk>.+)$',RoleUpdate.as_view(),name='RoleUpdate' ),
    url(r'^RoleMgt/delete/(?P<pk>.+)$',RoleDelete.as_view(),name='RoleDelete' ),
]
