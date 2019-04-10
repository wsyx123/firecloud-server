#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on Mar 29, 2019

@author: yangxu
'''

from django.db import models
from sysmgt.models import SysUser

class ZabbixNode(models.Model):
    label_choices=(
            (1,'web'),
            (2,'server')
        )
    version_choices=(
            (1,'3.0.4'),
            (2,'4.0.5')
        )
    run_model_choices=(
            (1,'docker'),
            (2,'daemon')
        )
    status_choices=(
            (1,'未部署'),
            (2,'正常'),
            (2,'异常')
        )
    name = models.CharField(max_length=32)
    label = models.IntegerField(choices=label_choices)
    version = models.IntegerField(choices=version_choices)
    host = models.GenericIPAddressField()
    port = models.IntegerField()
    run_model = models.IntegerField(choices=run_model_choices)
    db_host = models.GenericIPAddressField()
    db_port = models.IntegerField()
    db_database = models.CharField(max_length=32)
    db_user = models.CharField(max_length=16)
    db_password = models.CharField(max_length=64)
    status = models.IntegerField(choices=status_choices,default=1)
    owner = models.ForeignKey(SysUser)
    create_time = models.DateTimeField(auto_now_add=True)