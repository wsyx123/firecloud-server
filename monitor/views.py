#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月19日

@author: yangxu
'''
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView,FormView,ListView,DetailView
from forms import ZabbixNodeForm
from models import ZabbixNode

class ThirdComponentList(ListView):
    model = ZabbixNode
    context_object_name = 'ZabbixNodes'
    template_name = 'monitor/compose/ThirdComponentList.html'
    
class ThirdComponentZabbixAdd(FormView):
    form_class = ZabbixNodeForm
    template_name = 'monitor/compose/ThirdComponentZabbixAdd.html'
    success_url = reverse_lazy('thirdComponentList')
    def post(self, request, *args, **kwargs): 
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def ThirdComponentDeploy(request):
    if request.method == 'POST':
        print request.POST
        return JsonResponse({"code":200})
    else:
        return JsonResponse({"code":400})

class ThirdComponentDetail(DetailView):
    model = ZabbixNode
    pk_url_kwarg = 'pk'
    context_object_name = 'detailhost' #QuerySet 变量名
    template_name = 'monitor/compose/ThirdComponentList.html'
    def get_context_data(self, **kwargs):
        context = super(ThirdComponentDetail,self).get_context_data(**kwargs)
        nodeType = self.request.GET.get('nodeType')
        nodeName = self.request.GET.get('nodeName')
        print nodeType
        print nodeName
        return context

class AppMonitorList(TemplateView):
    template_name = 'monitor/app/AppMonitor.html'
    def get_context_data(self, **kwargs):
        context = super(AppMonitorList, self).get_context_data(**kwargs)
        return context
    
class AppMonitorDetail(TemplateView):
    template_name = 'monitor/app/AppMonitorDetail.html'
    def get_context_data(self, **kwargs):
        context = super(AppMonitorDetail, self).get_context_data(**kwargs)
        context['appname'] = kwargs['appname']
        return context
    
class AppMonitorFullScreen(TemplateView):
    template_name = 'monitor/app/AppMonitorDetailFullScreen.html'
    
class HostMonitorList(TemplateView):
    template_name = 'monitor/host/HostMonitor.html'
    def get_context_data(self, **kwargs):
        context = super(HostMonitorList, self).get_context_data(**kwargs)
        return context

class HostMonitorDetail(TemplateView):
    template_name = 'monitor/host/HostMonitorDetail.html'
    def get_context_data(self, **kwargs):
        context = super(HostMonitorDetail, self).get_context_data(**kwargs)
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