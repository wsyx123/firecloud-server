#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年3月8日 下午1:59:20
@author: yangxu
'''

from __future__ import unicode_literals
from django.db import models

class MonitorHost(models.Model):
    ip = models.GenericIPAddressField()
    status = models.IntegerField()
    