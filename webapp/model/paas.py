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
                     (6,'集群异常'),
                     (7,'还未启动')
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
    haproxyImage = models.CharField(max_length=128)
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
    
    def __unicode__(self):
        return '%s' %(self.clusterName)
    
class MesosDeployLog(models.Model):
    deployStatus = (
                    (1,'等待中'),
                    (2,'进行中'),
                    (3,'成功'),
                    (4,'失败')
                    )
    celery_id = models.CharField(max_length=64)
    cluster_name = models.CharField(max_length=32)
    step_name = models.CharField(max_length=32)
    start_time = models.DateTimeField(null=True,blank=True)
    status = models.IntegerField(choices=deployStatus,default=1)
    is_read = models.BooleanField(default=False)
    msg = models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return '%s' %(self.cluster_name)

class MesosClusterOverview(models.Model):
    status = (
            (1,'health'),
            (2,'warning'),
            (3,'danger'),
            (4,'unknown')
            )
    clusterName = models.CharField(max_length=32,unique=True)
    vendor = models.CharField(max_length=16,default='Apache Mesos')
    version = models.CharField(max_length=16,default='v1.6.1-rc2')
    leader = models.GenericIPAddressField(null=True,blank=True)
    total_container = models.IntegerField(default=0)
    cpu_use = models.IntegerField(default=0)
    memory_use = models.IntegerField(default=0)
    disk_use = models.IntegerField(default=0)
    master_status = models.IntegerField(choices=status,default=4)
    zookeeper_status = models.IntegerField(choices=status,default=4)
    marathon_status = models.IntegerField(choices=status,default=4)
    haproxy_status = models.IntegerField(choices=status,default=4)
    bamboo_status = models.IntegerField(choices=status,default=4)
    slave_status = models.IntegerField(choices=status,default=4)
    
class MesosClusterDetail(models.Model):
    nodetype = (
                (1,'master'),
                (2,'zookeeper'),
                (3,'marathon'),
                (4,'haproxy'),
                (5,'slave')
                )
    status = (
              (1,'运行'),
              (2,'停止')
              )
    
    clusterName = models.CharField(max_length=32,unique=True)
    nodeType = models.IntegerField(choices=nodetype)
    host = models.GenericIPAddressField()
    containerName = models.CharField(max_length=32)
    containerStatus = models.IntegerField(choices=status,default=1)
    serviceStatus = models.IntegerField(choices=status,default=1)
 
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
    