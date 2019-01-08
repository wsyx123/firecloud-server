#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月9日

@author: yangxu
'''
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
import json
from django.views.generic import TemplateView,DeleteView,FormView,ListView
from webapp.models import AssetHost,PaasHost,MesosCluster
from .forms import MesosClusterForm

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
   
class MesosIdleHostList(TemplateView):
    template_name = 'paas/cluster/mesos/MesosIdleHostList.html'
    def get_context_data(self, **kwargs):
        context = super(MesosIdleHostList, self).get_context_data(**kwargs)
        user_id = self.request.session.get('_user_id')
        if user_id == 1:
            assetHostQuerySet = PaasHost.objects.all()
        else:
            assetHostQuerySet = PaasHost.objects.filter(owner_id=user_id)
        context['hosts'] = assetHostQuerySet
        context['total_host_count'] = len(assetHostQuerySet)
        return context

def mesos_idle_host_add(request):
    if request.method == 'POST':
        checked_host_array = str(request.POST.get('checked_host_array'))
        user_id = request.session.get('_user_id')
        checked_host_list = json.loads(checked_host_array)
        msg = ''
        status = True
        for host in checked_host_list:
            try:
                hostObj = AssetHost.objects.get(private_ip=host)
                PaasHost.objects.create(host=hostObj,owner_id=user_id)
            except Exception as e:
                msg = msg+str(e)
                status = False
    return JsonResponse({'status':status,'msg':msg})

class MesosIdleHostDelete(DeleteView):
    model = PaasHost
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('MesosIdleHostList')
    def post(self, request, *args, **kwargs):
        idleHostId = int(request.POST.get('pk'))
        status = True
        msg = ''
        try:
            PaasHost.objects.get(id=idleHostId).delete()
        except Exception as e:
            msg = str(e)
            status = False
        return JsonResponse({'status':status,'msg':msg})

class MesosList(ListView):
    model = MesosCluster
    context_object_name = 'cluster_list'
    template_name = 'paas/cluster/mesos/MesosList.html'

class MesosOverview(TemplateView):
    template_name = 'paas/cluster/mesos/MesosOverview.html'
   

class MesosDetail(TemplateView):
    template_name = 'paas/cluster/mesos/MesosDetail.html'
   
    
class MesosAddCluster(FormView):
    form_class = MesosClusterForm
    success_url = reverse_lazy('MesosList')
    template_name = 'paas/cluster/mesos/MesosAddCluster.html'
    def get_context_data(self, **kwargs):
        context = super(MesosAddCluster, self).get_context_data(**kwargs)
        user_id = self.request.session.get('_user_id')
        if user_id == 1:
            assetHostQuerySet = PaasHost.objects.all()
        else:
            assetHostQuerySet = PaasHost.objects.filter(Q(owner_id=user_id),Q(assign_status=1))
        context['hosts'] = assetHostQuerySet
        return context
    
    def post(self, request, *args, **kwargs):
        status = int(request.POST.get('status'))
        form = self.get_form()
        if form.is_valid():
            status = True
            form.save(commit=True)
        else:
            status = False
        return JsonResponse({'status':status,'msg':form.errors})
        
        
    
class MesosAddNode(TemplateView):
    template_name = 'paas/cluster/mesos/MesosAddNode.html'
      
    
class ListNetwork(TemplateView):
    template_name = 'paas/resource/network.html'
   
    
class ListStorage(TemplateView):
    template_name = 'paas/resource/storage.html'
    