#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月9日

@author: yangxu
'''
from django.views.generic import TemplateView

class Kubernetes(TemplateView):
    template_name = 'paas/cluster/kubernetes/kubernetes.html'
    def get_context_data(self, **kwargs):
        context = super(Kubernetes, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clusters'] = [
{'name':'k8s01','createtime':'2018-05-01 14:36:49','manager':3,'node':3,'status':'unreachable','cpu':{'use':0.4,'total':2,'percent':22},'memory':{'use':0.4,'total':2,'percent':28}},
        ]
        return context
    
class K8sOverview(TemplateView):
    template_name = 'paas/cluster/kubernetes/k8sOverview.html'
    def get_context_data(self, **kwargs):
        context = super(K8sOverview, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clsinfo'] = {'clsname':kwargs['clsname'],'provide':'kubernetes','version':'v1.10.1','node':3}
        return context
    
class K8sDetail(TemplateView):
    template_name = 'paas/cluster/kubernetes/k8sDetail.html'
    def get_context_data(self, **kwargs):
        context = super(K8sDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clsinfo'] = {'clsname':kwargs['clsname'],'provide':'kubernetes','version':'v1.10.1','node':3}
        return context
   

class Mesos(TemplateView):
    template_name = 'paas/cluster/mesos/mesos.html'
    def get_context_data(self, **kwargs):
        context = super(Mesos, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clusters'] = [{'name':'mesos01','createtime':'2018-05-01 14:36:49',
                                'manager':3,'node':3,'haproxy':3,
                                'status':'unreachable',
                                'cpu':{'use':0.4,'total':2,'percent':22},
                                'memory':{'use':0.4,'total':2,'percent':28}},
        ]
        return context

class MesosOverview(TemplateView):
    template_name = 'paas/cluster/mesos/mesosOverview.html'
    def get_context_data(self, **kwargs):
        context = super(MesosOverview, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clsname'] = kwargs['clsname']
        return context

class MesosDetail(TemplateView):
    template_name = 'paas/cluster/mesos/mesosDetail.html'
    def get_context_data(self, **kwargs):
        context = super(MesosDetail, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['clsname'] = kwargs['clsname']
        return context
    
class MesosCreate(TemplateView):
    template_name = 'paas/cluster/mesos/mesosCreate.html'
    def get_context_data(self, **kwargs):
        context = super(MesosCreate, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context
    
class MesosAdd(TemplateView):
    template_name = 'paas/cluster/mesos/nodeAdd.html'
    def get_context_data(self, **kwargs):
        context = super(MesosAdd, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context     
    
class ListNetwork(TemplateView):
    template_name = 'paas/resource/network.html'
    def get_context_data(self, **kwargs):
        context = super(ListNetwork, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context  
    
class ListStorage(TemplateView):
    template_name = 'paas/resource/storage.html'
    def get_context_data(self, **kwargs):
        context = super(ListStorage, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context  
    
class RepoHost(TemplateView):
    template_name = 'paas/repository/repohost.html'
    def get_context_data(self, **kwargs):
        context = super(RepoHost, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context  
    
class RepoImage(TemplateView):
    template_name = 'paas/repository/repoimage.html'
    def get_context_data(self, **kwargs):
        context = super(RepoImage, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        return context  