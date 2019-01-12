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
    