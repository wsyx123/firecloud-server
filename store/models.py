#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:57:13
@author: yangxu
'''
from __future__ import unicode_literals
from django.db import models
from sysmgt.models import SysUser

class WebApp(models.Model):
    res_type = (
            (1,'docker'),
            (2,'tar'),
            (3,'zip'),
            (4,'rpm')
        )
    name = models.CharField(max_length=32,verbose_name='应用名称')
    description = models.CharField(max_length=128)
    version = models.CharField(max_length=16)
    logo_addr = models.CharField(max_length=128)
    res_type = models.IntegerField(choices=res_type,default=1,verbose_name='资源形式')
    res_addr = models.CharField(max_length=128,verbose_name='资源地址')
    create_time = models.DateTimeField(auto_now_add=True)
    
class WebAppInstance(models.Model):
    use_model = (
            (1,'epoll'),
            (2,'select')
        )
    sendfile = (
            (1,'on'),
            (2,'off')
        )
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    deploy_host = models.GenericIPAddressField()
    user = models.CharField(max_length=16)
    worker_processes = models.IntegerField()
    use = models.IntegerField(choices=use_model)
    worker_connections = models.IntegerField()
    sendfile = models.IntegerField(choices=sendfile)
    keepalive_timeout = models.IntegerField()
    manufacturer = models.CharField(max_length=64,verbose_name='应用厂商')
    manager = models.CharField(max_length=32,verbose_name='应用负责人')
    tel = models.IntegerField()
    email = models.EmailField()
    owner = models.ForeignKey(SysUser)
    create_time = models.DateTimeField(auto_now_add=True)

class NginxServer(models.Model):
    instance = models.ForeignKey(WebAppInstance)
    listen = models.IntegerField()
    server_name = models.CharField(max_length=32)

class NginxLocation(models.Model):
    server = models.ForeignKey(NginxServer)
    name = models.CharField(max_length=16)

class LocationItem(models.Model):
    location = models.ForeignKey(NginxLocation)
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=64)