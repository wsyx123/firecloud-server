#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月19日

@author: yangxu
'''
from django.views.generic import TemplateView

class AppMonitor(TemplateView):
    template_name = 'monitor/app/AppMonitor.html'
    def get_context_data(self, **kwargs):
        context = super(AppMonitor, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class AppMonitorDetail(TemplateView):
    template_name = 'monitor/app/AppMonitorDetail.html'
    def get_context_data(self, **kwargs):
        context = super(AppMonitorDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['appname'] = kwargs['appname']
        return context
    
class AppMonitorFullScreen(TemplateView):
    template_name = 'monitor/app/AppMonitorDetailFullScreen.html'
    
class HostMonitor(TemplateView):
    template_name = 'monitor/host/HostMonitor.html'
    def get_context_data(self, **kwargs):
        context = super(HostMonitor, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['hostinfo'] = [
        {'serial':'E5248D38-72C3','hostname':'192.168.130.103','cpu':'0.4/2 Cores','memory':'0.4/2 GiB','disk':'0.4/2 GiB','status':'','maintainer':'杨旭','email':'18508503875@139.com','tel':'18508503875'},
        {'serial':'E5248D38-72C4','hostname':'192.168.130.104','cpu':'0.4/2 Cores','memory':'0.4/2 GiB','disk':'0.4/2 GiB','status':'','maintainer':'杨旭','email':'18508503875@139.com','tel':'18508503875'},
                               ]
        return context

class HostMonitorDetail(TemplateView):
    template_name = 'monitor/host/HostMonitorDetail.html'
    def get_context_data(self, **kwargs):
        context = super(HostMonitorDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['hostname'] = kwargs['hostname']
        return context
    
class EventList(TemplateView):
    template_name = 'monitor/event/EventList.html'
    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class AlertPolicyList(TemplateView):
    template_name = 'monitor/policy/AlertPolicyList.html'
    def get_context_data(self, **kwargs):
        context = super(AlertPolicyList, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context

class AlertPolicyAdd(TemplateView):
    template_name = 'monitor/policy/AlertPolicyAdd.html'
    def get_context_data(self, **kwargs):
        context = super(AlertPolicyAdd, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class ReceiveGroupList(TemplateView):
    template_name = 'monitor/policy/ReceiveGroupList.html'
    def get_context_data(self, **kwargs):
        context = super(ReceiveGroupList, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
class ReceiveGroupAdd(TemplateView):
    template_name = 'monitor/policy/ReceiveGroupAdd.html'
    def get_context_data(self, **kwargs):
        context = super(ReceiveGroupAdd, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context