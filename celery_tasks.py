#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月23日

@author: yangxu
'''

from celery import Celery


app = Celery('celery_tasks', broker='redis://:root@192.168.10.1:6379/0')

app.send_task('test_celery')