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
                  6:'label-warning'
                  }
    return status_map[int(status_num)]

@register.inclusion_tag('paas/cluster/mesos/_opp_td.html')
def opp_td(status_num):
    return {'status':status_num}
    
    