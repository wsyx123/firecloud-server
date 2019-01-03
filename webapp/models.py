# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# import system management model 
from model.sys_mgt import SysRole,SysUser,Level1Menu,\
Level2Menu,Menu_Role_rel,HomePage,AppOpt_Role_rel

# import asset model
from model.asset import AssetHost,HostEvent,HostImport,HostAccount,HostGroup,Enterprise

# import tasks model
from model.task import ScriptModel,TaskLog,TaskHost,AnsibleModel,AnsibleLog,AnsibleHost,\
FileModel,FileLog,FileHost,FileModelExistList,FileModelForHad,FileModelForUrl,PublicFile

# import paas model
from model.paas import RepositoryHost,RepositoryImage

# Create your models here.
'''
auto_now:这个参数的默认值为false，设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改model，都会自动更新
auto_now_add:这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
'''

class PaasHost(models.Model):
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    label = models.CharField(max_length=16,verbose_name='备注')
    
    def __unicode__(self):
        return '%s' %(self.ip)
    
    
class MesosCluster(models.Model):
    c_status = (
                (1,'health'),
                (2,'warning'),
                (3,'danger')
                )
    name = models.CharField(max_length=32,verbose_name='名称')
    master_nodes = models.IntegerField(verbose_name='管理节点')
    slave_nodes = models.IntegerField(verbose_name='计算节点')
    haproxy_nodes = models.IntegerField(verbose_name='Haproxy节点')
    cpu_used = models.FloatField(verbose_name='CPU使用核数')
    cpu_total = models.FloatField(verbose_name='CPU总核数')
    memory_used = models.FloatField(verbose_name='已使用内存')
    memory_total = models.FloatField(verbose_name='内存总量')
    disk_used = models.FloatField(verbose_name='已使用存储')
    disk_total = models.FloatField(verbose_name='存储总量')
    status = models.IntegerField(choices=c_status,verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    provider = models.CharField(max_length=32,verbose_name='供应商')
    def __unicode__(self):
        return '%s' %(self.name)
    
class MesosMaster(models.Model):
    m_status = (
                (1,'health'),
                (2,'warning'),
                (3,'danger')
                )
    cluster = models.ForeignKey('MesosCluster',verbose_name='集群')
    version = models.CharField(max_length=32,verbose_name='版本')
    image = models.CharField(max_length=128,verbose_name='镜像')
    hosts = models.ManyToManyField('PaasHost',verbose_name='主机')
    leader = models.GenericIPAddressField(verbose_name='leader地址')
    port = models.IntegerField(verbose_name='端口')
    zk = models.CharField(max_length=255,verbose_name='ZK地址')
    log_dir = models.CharField(max_length=255,verbose_name='日志目录')
    work_dir = models.CharField(max_length=255,verbose_name='工作目录')
    documentation = models.CharField(max_length=255,verbose_name='参考链接')
    status = models.IntegerField(choices=m_status,verbose_name='状态')
    def hosts_list(self):
        return ', '.join([a.ip for a in self.hosts.all()])
    
    def __unicode__(self):
        return '%s' %(self.cluster)


    
    