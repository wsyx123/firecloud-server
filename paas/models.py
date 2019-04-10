#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:41:23
@author: yangxu
'''

from __future__ import unicode_literals

from django.db import models
from sysmgt.models import SysUser
from asset.models import AssetHost

class IdleHost(models.Model):
    assignStatus = (
                  (1,'未分配'),
                  (2,'已分配')
                  )
    # OneToOne has the same effect as to Setting unique=True on a ForeignKey
    host = models.OneToOneField(AssetHost,related_name='host_AssetHost')  
    assign_status = models.IntegerField(choices=assignStatus,default=1)
    owner = models.ForeignKey(SysUser,related_name='IdleHost_owner')
    create_time = models.DateTimeField(auto_now_add=True)
     
    def __unicode__(self):
        return '%s' %(self.ip)
    
class MesosMaster(models.Model):
    clusterStatus = (
                     (1,'还未部署'),
                     (2,'正在部署'),
                     (3,'部署失败'),
                     (4,'集群正常'),
                     (5,'集群异常'),
                     (6,'集群错误')
                     )
    status = (
            (1,'health'),
            (2,'warning'),
            (3,'danger'),
            (4,'unknown')
            )
    #master
    clusterName = models.CharField(max_length=32,unique=True)
    masterNodeNum = models.IntegerField()
    masterPort = models.IntegerField()
    masterImage = models.CharField(max_length=128)
    zkImage = models.CharField(max_length=128)
    #other info
    vendor = models.CharField(max_length=16,null=True,blank=True,default='Apache Mesos')
    version = models.CharField(max_length=16,null=True,blank=True,default='v1.6.1-rc2')
    leader = models.GenericIPAddressField(null=True,blank=True)
    total_container = models.IntegerField(null=True,blank=True,default=0)
    cpu_used = models.IntegerField(null=True,blank=True,default=0)
    cpu_total = models.IntegerField(null=True,blank=True,default=0)
    memory_used = models.FloatField(null=True,blank=True,default=0)
    memory_total = models.FloatField(null=True,blank=True,default=0)
    disk_used = models.FloatField(null=True,blank=True,default=0)
    disk_total = models.FloatField(null=True,blank=True,default=0)
    #status
    master_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    zookeeper_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    marathon_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    haproxy_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    bamboo_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    slave_status = models.IntegerField(choices=status,null=True,blank=True,default=4)
    owner = models.ForeignKey(SysUser,related_name='MesosMaster_owner')
    status = models.IntegerField(choices=clusterStatus,null=True,blank=True,default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s' %(self.clusterName)
    
class MesosMarathon(models.Model):
    clusterStatus = (
             (1,'还未部署'),
             (2,'正在部署'),
             (3,'部署失败'),
             (4,'集群正常'),
             (5,'集群异常'),
             (6,'集群错误')
             )
    clusterName = models.CharField(max_length=32)
    marathonID = models.CharField(max_length=32,unique=True)
    marathonPort = models.IntegerField(default=8080)
    #marathonZK 指向mesos master的  zk node
    marathonZK = models.CharField(max_length=128)
    marathonImage = models.CharField(max_length=128)
    status = models.IntegerField(choices=clusterStatus,null=True,blank=True,default=1)
    is_master = models.BooleanField(default=True)

class MesosHaproxy(models.Model):
    clusterStatus = (
             (1,'还未部署'),
             (2,'正在部署'),
             (3,'部署失败'),
             (4,'集群正常'),
             (5,'集群异常'),
             (6,'集群错误')
             )
    clusterName = models.CharField(max_length=32)
    haproxyID = models.CharField(max_length=32,unique=True)
    servicePort = models.IntegerField()
    statusPort = models.IntegerField()
    bambooPort = models.IntegerField()
    haproxyMarathon = models.CharField(max_length=128)
    haproxyImage = models.CharField(max_length=128)
    status = models.IntegerField(choices=clusterStatus,null=True,blank=True,default=1)
    is_master = models.BooleanField(default=True)

class MesosSlave(models.Model):
    clusterStatus = (
             (1,'还未部署'),
             (2,'正在部署'),
             (3,'部署失败'),
             (4,'集群正常'),
             (5,'集群异常'),
             (6,'集群错误')
             )
    clusterName = models.CharField(max_length=32)
    slaveLabel = models.CharField(max_length=32,unique=True)
    slavePort = models.IntegerField(default=5051)
    #slaveZK 指向mesos master的  zk node
    slaveZK = models.CharField(max_length=128)
    slaveImage = models.CharField(max_length=128)
    status = models.IntegerField(choices=clusterStatus,null=True,blank=True,default=1)
    is_master = models.BooleanField(default=True)
    
class MesosDeployLog(models.Model):
    deployStatus = (
                    (1,'等待中'),
                    (2,'进行中'),
                    (3,'成功'),
                    (4,'失败')
                    )
    celery_id = models.CharField(max_length=64)
    name = models.CharField(max_length=32,default="集群部署")
    cluster_name = models.CharField(max_length=32)
    step_name = models.CharField(max_length=32)
    start_time = models.DateTimeField(null=True,blank=True)
    finished_time = models.DateTimeField(null=True,blank=True)
    status = models.IntegerField(choices=deployStatus,default=1)
    is_read = models.BooleanField(default=False)
    msg = models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return '%s' %(self.cluster_name)

    
class MesosNodeStatus(models.Model):
    status = (
              (1,'运行'),
              (2,'停止'),
              (3,'创建'),
              (4,'未创建')
              )
    clusterName = models.CharField(max_length=32)
    #nodeName 对于marathon,haproxy,slave 就等于 marathonID, haproxyID, slaveLabel
    #对于master 和zookeeper是固定的 因为一个mesos集群只能有一个master
    nodeName = models.CharField(max_length=32)#eg: master,zookeeper,marathon01
    host = models.GenericIPAddressField()
    containerID = models.CharField(max_length=64,null=True,blank=True)
    containerName = models.CharField(max_length=32)
    containerRunTime = models.CharField(max_length=32,default='1秒')
    containerStatus = models.IntegerField(choices=status,default=4)
    serviceStatus = models.IntegerField(choices=status,default=4)
    class Meta:
        #Django model中设置多个字段联合唯一约束
        unique_together = ('nodeName', 'host')
 
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
    