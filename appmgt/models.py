#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on Apr 9, 2019

@author: yangxu
'''


from __future__ import unicode_literals
from django.db import models
from sysmgt.models import SysUser
from paas.models import MesosSlave,MesosMarathon

class DockerAppInfo(models.Model):
    publish_model = (
            (1,'镜像包含'),
            (2,'卷挂载')
        )
    distribution_policy = (
            (1,'GROUP BY'),
            (2,'UNIQUE')
        )
    net_model = (
            (1,'bridge'),
            (2,'host'),
            (3,'user')
        )
    # base infomation
    app_id = models.CharField(max_length=16,verbose_name='应用ID')
    app_name = models.CharField(max_length=32,verbose_name='应用名称')
    publish_model = models.IntegerField(choices=publish_model,verbose_name='发包方式')
    #publish config
    resource_pool = models.ForeignKey(MesosSlave,verbose_name='资源池')
    publish_platform = models.ForeignKey(MesosMarathon,verbose_name='发布平台')
    distribution_policy = models.IntegerField(choices=distribution_policy,verbose_name='分布策略')
    #container specification
    image = models.CharField(max_length=128,verbose_name='应用镜像')
    net_model = models.IntegerField(choices=net_model,default=1)
    run_user = models.CharField(max_length=16,verbose_name='运行用户')
    #maintain infomation
    manufacturer = models.CharField(max_length=64,verbose_name='应用厂商')
    manager = models.CharField(max_length=32,verbose_name='应用负责人')
    tel = models.IntegerField()
    email = models.EmailField()
    owner = models.ForeignKey(SysUser)
    create_time = models.DateTimeField(auto_now_add=True)
    

class DockerAppSpec(models.Model):
    app_id = models.ForeignKey('DockerAppInfo')
    cpu = models.FloatField()
    mem = models.IntegerField()
    disk = models.IntegerField()
    instance = models.IntegerField()

class DockerAppPort(models.Model):
    map_protocol = (
            (1,'tcp'),
            (2,'udp')
        )
    app_id = models.ForeignKey('DockerAppInfo')
    host = models.IntegerField()
    container = models.IntegerField()
    protocol = models.IntegerField(choices=map_protocol)
    
class DockerAppVol(models.Model):
    read_write_model = (
            (1,'只读'),
            (2,'读写')
        )
    app_id = models.ForeignKey('DockerAppInfo')
    host = models.CharField(max_length=128)
    container = models.CharField(max_length=128)
    rw_model = models.IntegerField(choices=read_write_model)

class DockerAppEnv(models.Model):
    app_id = models.ForeignKey('DockerAppInfo')
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=64)
    
    