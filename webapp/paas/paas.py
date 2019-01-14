#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月9日

@author: yangxu
'''
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.forms.models import model_to_dict
import json
from django.views.generic import TemplateView,DeleteView,FormView,ListView
from webapp.models import AssetHost,PaasHost,MesosDeployLog,MesosCluster
from .forms import MesosClusterForm
from webapp.tasks import mesos_cluster_deploy_task

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
            assetHostQuerySet = AssetHost.objects.all()
            paasHostQuerySet = PaasHost.objects.all()
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=user_id)
            paasHostQuerySet = PaasHost.objects.filter(owner_id=user_id)
        context['assethosts'] = assetHostQuerySet
        context['paashosts'] = paasHostQuerySet
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

class MesosMasterDetail(TemplateView):
    template_name = 'paas/cluster/mesos/MesosMasterDetail.html'   
    
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

def mesos_cluster_deploy(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
        deployOption = request.POST.get('deployOption')
        if deployOption == 'yes':
            print deployOption
        clusterObj = MesosCluster.objects.get(id=cluster_id)
        clusterObj.status = 2
        clusterObj.save()
        mesos_cluster_deploy_task.apply_async(args=(clusterObj,MesosDeployLog))
    return JsonResponse({'status':200})

def mesos_cluster_start(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
    return JsonResponse({'status':200})

def mesos_cluster_stop(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
    return JsonResponse({'status':200})

def mesos_cluster_delete(request):
    if request.method == 'POST':
        cluster_id = int(request.POST.get('cluster_id'))
        try:
            MesosCluster.objects.get(id=cluster_id).delete()
        except Exception as e:
            status = 400
            msg = str(e)
        else:
            status = 200
            msg = ''
    return JsonResponse({'status':status,'msg':msg})

class MesosClusterDeployResult(TemplateView):
    template_name = 'paas/cluster/mesos/MesosClusterDeployResult.html'
    def get_context_data(self, **kwargs):
        cluster_id = self.request.GET.get('cluster_id')
        clusterObj = MesosCluster.objects.get(id=cluster_id)
        cluster_dict = model_to_dict(clusterObj)
        kwargs['cluster'] = cluster_dict
        return TemplateView.get_context_data(self, **kwargs)
    
    def post(self,request):
        clusterName = self.request.POST.get('clusterName')
        #first: to get the record of status=3 (finished)
        successObj = MesosDeployLog.objects.filter(Q(cluster_name=clusterName),Q(is_read=False),Q(status=3))
        runObj = MesosDeployLog.objects.filter(Q(cluster_name=clusterName),Q(status=2))
        failObj = MesosDeployLog.objects.filter(Q(cluster_name=clusterName),Q(status=4))
        if len(successObj) != 0:
            status = 'running'
            oneObj = successObj[0]
            oneObj.is_read = True
            oneObj.save()
            data = model_to_dict(oneObj)
        elif len(runObj) != 0:
            status = 'running'
            data = model_to_dict(runObj[0])
        elif len(failObj) != 0:
            status = 'finished'
            data = model_to_dict(failObj[0])
        else:
            status = 'finished'
            data = ''
        return JsonResponse({'status':status,'data':data})
        
    
class MesosAddNode(TemplateView):
    template_name = 'paas/cluster/mesos/MesosAddNode.html'
      
    
class ListNetwork(TemplateView):
    template_name = 'paas/resource/network.html'
   
    
class ListStorage(TemplateView):
    template_name = 'paas/resource/storage.html'
    