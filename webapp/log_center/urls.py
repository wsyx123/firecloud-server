#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from log_center import  UserMgt,RoleMgt

urlpatterns = [
    url(r'^UserMgt/$',UserMgt.as_view(),name='UserMgt' ),
    url(r'^RoleMgt/$',RoleMgt.as_view(),name='RoleMgt' ),           
]
