#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:57:13
@author: yangxu
'''
from __future__ import unicode_literals
from django.db import models

class AssetHost(models.Model):
    host_status = (
                   (1,u'在线'),
                   (2,u'离线'),
                   )
    operate_status = (
                      (1,u'运营中'),
                      (2,u'维护中'),
                      (3,u'已下线')
                      )
    asset_type = (
                  (1,'物理机'),
                  (2,'虚拟机')
                  )
    private_ip = models.GenericIPAddressField(unique=True,verbose_name='私网IP')#1L
    port = models.IntegerField(verbose_name='端口')
    host_status = models.IntegerField(choices=host_status,verbose_name='状态')
    remote_user = models.CharField(max_length=32,verbose_name='远程帐号')
    remote_passwd = models.CharField(max_length=64,verbose_name='用户密码')
    agent_is_install = models.BooleanField(default=False,verbose_name='agent已安装')
    
    type = models.IntegerField(default=1,verbose_name='资产类型')
    serial = models.CharField(max_length=64,null=True, blank=True,verbose_name='序列号')
    hostname = models.CharField(max_length=32,null=True,blank=True,verbose_name='主机名')
    public_ip = models.GenericIPAddressField(null=True, blank=True,verbose_name='公网IP')
    cpu_no = models.IntegerField(null=True, blank=True,verbose_name='CPU核数')
    cpu_model = models.CharField(max_length=128,null=True, blank=True,verbose_name='CPU型号')
    memory = models.IntegerField(null=True, blank=True,verbose_name='物理内存')
    disk = models.FloatField(null=True, blank=True,verbose_name='磁盘容量')
    os = models.CharField(max_length=64,null=True, blank=True,verbose_name='操作系统')
    kernel =models.CharField(max_length=64,null=True, blank=True,verbose_name='内核版本')
    machine_model = models.CharField(max_length=32,null=True, blank=True,verbose_name='机器型号')
    
    verdor = models.CharField(max_length=64,null=True, blank=True,verbose_name='供应商')
    position = models.CharField(max_length=64,null=True, blank=True,verbose_name='位置信息')
    group = models.ForeignKey('HostGroup',on_delete=models.PROTECT,verbose_name='主机组')
    operate_status = models.IntegerField(choices=operate_status,null=True, blank=True,verbose_name='运营状态')
    department = models.CharField(max_length=64,null=True, blank=True,verbose_name='使用部门')#21L
    owner = models.ForeignKey('SysUser')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    
    def get_maintainer(self):
        return HostGroup.objects.get(id=self.group_id).maintainer
    
    def __unicode__(self):
        return '%s' %(self.private_ip)
    
class HostDisk(models.Model):
    host = models.ForeignKey(AssetHost)
    name = models.CharField(max_length=32,verbose_name='分区名称')
    size = models.CharField(max_length=16)
    used = models.CharField(max_length=16)
    available = models.CharField(max_length=16)
    percent = models.IntegerField()
    mount = models.CharField(max_length=32)

class HostEth(models.Model):
    host = models.ForeignKey(AssetHost)
    name = models.CharField(max_length=32,verbose_name='网卡名称')
    ip = models.GenericIPAddressField()
    netmask = models.GenericIPAddressField()
    mac = models.CharField(max_length=17,null=True,blank=True)
    speed = models.IntegerField(null=True,blank=True)
    status = models.BooleanField(default=False)
      
class HostEvent(models.Model):
    actions = (
                   (1,u'代理安装'),
                   (2,u'规格信息收集'),
                   (3,u'规格信息刷新'),
                   )
    host = models.ForeignKey('AssetHost')
    action = models.IntegerField(choices=actions)
    is_succeeded = models.BooleanField(default=False)
    content = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' %(self.action)
    
class HostImport(models.Model):
    filename = models.CharField(max_length=16,verbose_name="文件名")
    total_line = models.IntegerField(default=0,verbose_name="行数")
    succeeded_line = models.IntegerField(default=0,verbose_name="处理成功")
    failure_line = models.IntegerField(default=0,verbose_name="处理失败")
    err_line = models.CharField(max_length=64,null=True,blank=True,verbose_name="错误行号")
    err_msg = models.TextField(null=True,blank=True,verbose_name="错误信息")
    is_finished = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.filename)
    
class HostAccount(models.Model):
    userStatus = (
                  (1,'正常'),
                  (2,'锁定')
                  )
    host = models.ForeignKey(AssetHost)
    account = models.CharField(max_length=16)
    passwd = models.CharField(max_length=32,null=True,blank=True)
    last_password_change = models.CharField(max_length=16,null=True,blank=True)
    password_expires = models.CharField(max_length=16,default='Never')
    account_expires = models.CharField(max_length=16,default='Never')
    status = models.IntegerField()
    msg = models.CharField(max_length=32,null=True,blank=True)


class HostGroup(models.Model):
    name = models.CharField(max_length=32,verbose_name='主机组')
    description = models.CharField(max_length=64,verbose_name='备注')
    maintainer = models.CharField(max_length=32,verbose_name='运维人员')
    tel = models.CharField(max_length=11,verbose_name='电话')
    email = models.CharField(max_length=32,verbose_name='邮箱')
    def hosts(self):
        return len(AssetHost.objects.filter(group_id=self.id))
    def __unicode__(self):
        return '%s' %(self.name)
    
class Enterprise(models.Model):
    pass