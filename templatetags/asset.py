#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年2月12日 下午4:35:14
@author: yangxu
'''
from django import template

register = template.Library()

@register.inclusion_tag('asset/host/_MonitorView.html')
def hostMonitorView():
    return

@register.inclusion_tag('asset/host/_HostInfo.html')
def hostInfoView(detailhost,DiskQuerySet,EthQuerySet):
    return {'detailhost':detailhost,'DiskQuerySet':DiskQuerySet,'EthQuerySet':EthQuerySet}

@register.inclusion_tag('asset/host/_AgentInfo.html')
def AgentInfoView(agent_is_install,agent_status):
    return {'agent_is_install':agent_is_install,'agent_status':agent_status}