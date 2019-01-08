#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:41:23
@author: yangxu
'''

from __future__ import unicode_literals

from django.db import models

class PaasHost(models.Model):
    assignStatus = (
                  (1,'未分配'),
                  (2,'已分配')
                  )
    host = models.ForeignKey('AssetHost')
    assign_status = models.IntegerField(choices=assignStatus,default=1)
    owner = models.ForeignKey('SysUser')
    create_time = models.DateTimeField(auto_now_add=True)
     
    def __unicode__(self):
        return '%s' %(self.ip)
    
class MesosCluster(models.Model):
    clusterStatus = (
                     (1,'还未部署'),
                     (2,'正在部署'),
                     (3,'部署失败'),
                     (4,'集群正常'),
                     (5,'集群错误'),
                     (6,'集群异常')
                     )
    #master
    clusterName = models.CharField(max_length=32,unique=True)
    masterNodeNum = models.IntegerField()
    masterPort = models.IntegerField()
    masterImage = models.CharField(max_length=128)
    zkImage = models.CharField(max_length=128)
    masterDeploy = models.CharField(max_length=256)
    #marathon
    marathonID = models.CharField(max_length=32)
    marathonPort = models.IntegerField()
    marathonZK = models.CharField(max_length=128)
    marathonImage = models.CharField(max_length=128)
    marathonDeploy = models.CharField(max_length=256)
    #haprox
    haproxyID = models.CharField(max_length=32)
    servicePort = models.IntegerField()
    statusPort = models.IntegerField()
    bambooPort = models.IntegerField()
    haproxyMarathon = models.CharField(max_length=128)
    haproxImage = models.CharField(max_length=128)
    haproxyDeploy = models.CharField(max_length=256)
    #slave
    slaveLabel = models.CharField(max_length=32)
    slavePort = models.IntegerField()
    slaveZK = models.CharField(max_length=128)
    slaveImage = models.CharField(max_length=128)
    slaveDeploy = models.CharField(max_length=256)
    #other info
    owner = models.ForeignKey('SysUser')
    status = models.IntegerField(choices=clusterStatus,default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    

    
class MesosCluster1(models.Model):
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
    