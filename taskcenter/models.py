#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午1:25:31
@author: yangxu
'''
from __future__ import unicode_literals
from django.db import models
from sysmgt.models import SysUser

class ScriptModel(models.Model):
    scriptType = (
                  (1,'bash'),
                  (2,'python'),
                  (3,'perl')
                  )
    scriptFrom = (
                  (1,'手动录入'),
                  (2,'本地导入'),
                  (3,'已有脚本')
                  )
    name = models.CharField(unique=True,max_length=64)
    script_type = models.IntegerField(choices=scriptType,default=1)
    script_from = models.IntegerField(choices=scriptFrom,default=1)
    script_file = models.CharField(max_length=64)
    owner = models.ForeignKey(SysUser,related_name='ScriptModel_owner')
    total_run_count = models.IntegerField(default=0,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
#ScriptLog    
class TaskLog(models.Model):
    taskType = (
                (1,'脚本执行'),
                (2,'Ansible'),
                (3,'快速工具')
                )
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    task_name = models.CharField(max_length=32,verbose_name='名称')
    task_type = models.IntegerField(choices=taskType,verbose_name='类型')
    host_no = models.IntegerField(verbose_name='主机数量')
    finish_no = models.IntegerField(verbose_name='已完成')
    failure_no = models.IntegerField(verbose_name='失败')
    execute_owner = models.ForeignKey(SysUser,related_name='TaskLog_owner')
    script_file = models.CharField(max_length=64)
    execute_time = models.DateTimeField(auto_now=True,verbose_name='执行时间')
#ScriptHost
class TaskHost(models.Model):
    executeStatus = (
                     (1,'成功'),
                     (2,'失败')
                     )
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    host_ip = models.GenericIPAddressField(verbose_name='主机IP')
    host_account = models.CharField(max_length=10,verbose_name='帐号')
    execute_status = models.IntegerField(choices=executeStatus)
    
class AnsibleModel(models.Model):
    name = models.CharField(unique=True,max_length=64)
    total_role_count = models.IntegerField(null=True,blank=True)
    total_task_count = models.IntegerField(null=True,blank=True)
    dir_name = models.CharField(max_length=32,verbose_name='保存目录',null=True,blank=True)
    owner = models.ForeignKey(SysUser,related_name='AnsibleModel_owner')
    total_run_count = models.IntegerField(default=0,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
class AnsibleLog(models.Model):
    executeStatus = (
                     (1,'完成'),
                     (2,'未完成'),
                     (3,'异常')
                     )
    task_id = models.CharField(unique=True,max_length=8)
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(SysUser,related_name='AnsibleLog_owner')
    total_task_count = models.IntegerField(null=True,blank=True)
    status = models.IntegerField(choices=executeStatus,default=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True,blank=True)
    total_time = models.IntegerField(null=True,blank=True)
    msg = models.TextField(null=True,blank=True)
    
class AnsibleHost(models.Model):
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    step = models.CharField(max_length=32)
    task = models.CharField(max_length=32)
    host = models.GenericIPAddressField(verbose_name='主机IP')
    status = models.BooleanField()
    msg = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)
    
class FileModel(models.Model):
    fileFrom = (
              (1,'本地上传'),
              (2,'已有文件'),
              (3,'文件地址')
              )
    sendModel = (
                 (1,'ansible'),
                 (2,'murder p2p')
                 )
    name = models.CharField(unique=True,max_length=64)
    remote_path = models.CharField(max_length=32)
    file_from = models.IntegerField(choices=fileFrom,default=1)
    send_model = models.IntegerField(choices=sendModel,default=1)
    owner = models.ForeignKey(SysUser,related_name='FileModel_owner')
    total_run_count = models.IntegerField(default=0,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

class FileLog(models.Model):
    executeStatus = (
                     (1,'完成'),
                     (2,'未完成'),
                     (3,'异常')
                     )
    fileFrom = (
              (1,'本地上传'),
              (2,'已有文件'),
              (3,'文件地址')
              )
    sendModel = (
                 (1,'ansible'),
                 (2,'murder p2p')
                 )
    task_id = models.CharField(unique=True,max_length=8)
    name = models.CharField(max_length=32)
    file_from = models.IntegerField(choices=fileFrom,default=1)
    send_model = models.IntegerField(choices=sendModel,default=1)
    owner = models.ForeignKey(SysUser,related_name='FileLog_owner')
    total_file = models.IntegerField()
    total_host = models.IntegerField()
    status = models.IntegerField(choices=executeStatus,default=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True,blank=True)
    total_time = models.IntegerField(null=True,blank=True)
    msg = models.TextField(null=True,blank=True)
    
class FileHost(models.Model):
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    task = models.CharField(max_length=32)
    host = models.GenericIPAddressField(verbose_name='主机IP')
    status = models.BooleanField()
    msg = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)

class FileModelExistList(models.Model):
    file_name = models.CharField(max_length=32)
    file_path = models.CharField(max_length=128)
    file_size = models.CharField(max_length=8)
    task_name = models.CharField(max_length=32)
    owner = models.ForeignKey(SysUser,related_name='FileModelExistList_owner')
    file_type = models.CharField(max_length=8,default="private")
    
class FileModelForHad(models.Model):
    task_name = models.CharField(max_length=32)
    file_path = models.CharField(max_length=128)

class FileModelForUrl(models.Model):
    task_name = models.CharField(max_length=32,unique=True)
    url = models.CharField(max_length=128)

class PublicFile(models.Model):
    file_name = models.CharField(max_length=32)
    file_path = models.CharField(max_length=128)
    file_size = models.CharField(max_length=8)
    owner = models.ForeignKey(SysUser,related_name='PublicFile_owner')
    create_time = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=8,default="public")