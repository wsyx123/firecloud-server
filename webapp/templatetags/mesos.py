#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月9日 下午5:38:04
@author: yangxu
'''

from django import template

register = template.Library()

#统计集群数量  count marathon cluster number
@register.simple_tag(name='countNode')
def count_node(Count,clusterName,nodeType):
    return Count[clusterName][nodeType]

@register.filter(name='returnClass')
def return_class(status_num):
    status_map = {
                  1:'label-default',
                  2:'label-info',
                  3:'label-danger',
                  4:'label-success',
                  5:'label-warning',
                  6:'label-danger',
                  7:'label-default'
                  }
    return status_map[int(status_num)]

@register.inclusion_tag('paas/cluster/mesos/_overview_status.html')
def return_overview_div(status_num,name):
    return {'status':status_num,'name':name}

@register.inclusion_tag('paas/cluster/mesos/_cluster_action_buttons.html')
def cluster_action_buttons(status_num,clusterName):
    if status_num in [1,3]:
        status_num = 1
    if status_num in [4,5,6]:
        status_num = 4
    return {'status':status_num,'clusterName':clusterName}

@register.inclusion_tag('paas/cluster/mesos/detail/_master_detail.html')
def master_detail(masterObj,masterNodes):
    return {'masterObj':masterObj,'masterNodes':masterNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_zookeeper_detail.html')
def zookeeper_detail(clusterObj,zookeeperNodes):
    return {'clusterObj':clusterObj,'zookeeperNodes':zookeeperNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_marathon_detail.html')
def marathon_detail(marathonObj,marathonNodes):
    return {'marathonObj':marathonObj,'marathonNodes':marathonNodes[marathonObj.marathonID]}

@register.inclusion_tag('paas/cluster/mesos/detail/_haproxy_detail.html')
def haproxy_detail(haproxyObj,haproxyNodes):
    return {'haproxyObj':haproxyObj,'haproxyNodes':haproxyNodes[haproxyObj.haproxyID]}

@register.inclusion_tag('paas/cluster/mesos/detail/_slave_detail.html')
def slave_detail(slaveObj,slaveNodes):
    return {'slave':slaveObj,'slaveNodes':slaveNodes[slaveObj.slaveLabel]}

@register.inclusion_tag('paas/cluster/mesos/detail/_node_status.html')
def node_status(nodeObj):
    return {'node':nodeObj}

#计算集群cpu,内存,磁盘利用率
@register.simple_tag(name='resource_percent')
def resource_percent(used,total):
    percent = int(round(float(used)/(total+1)*100,0))
    return percent


    
    