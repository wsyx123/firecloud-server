#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:41:23
@author: yangxu
'''

from __future__ import unicode_literals

from django.db import models

class RepositoryHost(models.Model):
    apiType = (
               (1,'Docker Hub'),
               (2,'VMware Harbor')
               )
    repoVersion = (
                   (1,'v1.0'),
                   (2,'v2.0')
                   )
    repoLabel = (
                 (1,'系统镜像仓库'),
                 (2,'应用镜像仓库'),
                 (3,'其它镜像仓库')
                 )
    hostStatus = (
                  (1,'在线'),
                  (2,'离线')
                  )
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    api_type = models.IntegerField(choices=apiType)
    version = models.IntegerField(choices=repoVersion)
    image_num = models.IntegerField()
    label = models.IntegerField(choices=repoLabel)
    status = models.IntegerField(choices=hostStatus)
    create_time = models.DateTimeField(auto_now_add=True)
    
class RepositoryImage(models.Model):
    repoLabel = (
                 (1,'系统镜像仓库'),
                 (2,'应用镜像仓库'),
                 (3,'其它镜像仓库')
                 )
    image_name = models.CharField(max_length=128)
    image_id = models.CharField(max_length=12)
    docker_version = models.CharField(max_length=16)
    ip_port = models.CharField(max_length=32)
    label = models.IntegerField(choices=repoLabel)
    image_size = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    