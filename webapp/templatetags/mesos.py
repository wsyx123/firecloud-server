#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月9日 下午5:38:04
@author: yangxu
'''

from django import template

register = template.Library()

@register.filter(name='countNode')
def count_node(deployhoststr):
    host_list = deployhoststr.split(',')
    return len(host_list)

@register.filter(name='returnClass')
def return_class(status_num):
    status_map = {
                  1:'label-default',
                  2:'label-info',
                  3:'label-danger',
                  4:'label-success',
                  5:'label-danger',
                  6:'label-warning',
                  7:'label-default'
                  }
    return status_map[int(status_num)]

@register.inclusion_tag('paas/cluster/mesos/_overview_status.html')
def return_overview_div(status_num,name):
    return {'status':status_num,'name':name}

@register.inclusion_tag('paas/cluster/mesos/_opp_td.html')
def opp_td(status_num,clusterName):
    if status_num in [1,3]:
        status_num = 1
    if status_num in [4,5,6]:
        status_num = 4
    return {'status':status_num,'clusterName':clusterName}

@register.inclusion_tag('paas/cluster/mesos/detail/_master_detail.html')
def master_detail(clusterObj,masterNodes):
    return {'clusterObj':clusterObj,'masterNodes':masterNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_zookeeper_detail.html')
def zookeeper_detail(clusterObj,zookeeperNodes):
    return {'clusterObj':clusterObj,'zookeeperNodes':zookeeperNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_marathon_detail.html')
def marathon_detail(clusterObj,marathonNodes):
    return {'clusterObj':clusterObj,'marathonNodes':marathonNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_haproxy_detail.html')
def haproxy_detail(clusterObj,haproxyNodes):
    return {'clusterObj':clusterObj,'haproxyNodes':haproxyNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_slave_detail.html')
def slave_detail(clusterObj,slaveNodes):
    return {'clusterObj':clusterObj,'slaveNodes':slaveNodes}

@register.inclusion_tag('paas/cluster/mesos/detail/_button.html')
def detail_button():
    return {'status':True}

@register.inclusion_tag('paas/cluster/mesos/detail/_node_status.html')
def node_status(nodeObj):
    return {'node':nodeObj}
    
    