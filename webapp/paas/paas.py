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
from webapp.models import AssetHost,PaasHost,MesosDeployLog,MesosCluster,MesosClusterOverview,\
MesosClusterDetail
from .forms import MesosClusterForm
from webapp.tasks import mesos_cluster_deploy_task
from docker import DockerClient

class Kubernetes(TemplateView):
    template_name = 'paas/cluster/kubernetes/kubernetes.html'
   
class K8sOverview(TemplateView):
    template_name = 'paas/cluster/kubernetes/k8sOverview.html'
    
    
class K8sDetail(TemplateView):
    template_name = 'paas/cluster/kubernetes/k8sDetail.html'
   
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

class MesosClusterList(ListView):
    model = MesosCluster
    context_object_name = 'cluster_list'
    template_name = 'paas/cluster/mesos/MesosClusterList.html'

class MesosOverview(TemplateView):
    template_name = 'paas/cluster/mesos/MesosClusterOverview.html'
    def get_context_data(self, **kwargs):
        context = super(MesosOverview,self).get_context_data(**kwargs)
        context['clsObj'] = MesosClusterOverview.objects.get(clusterName=kwargs['clsname'])
        return context

class MesosClsDetail(TemplateView):
    template_name = 'paas/cluster/mesos/MesosClusterDetail.html'
    def get_context_data(self, **kwargs):
        context = super(MesosClsDetail,self).get_context_data(**kwargs)
        clsname = kwargs['clsname']
        context['clusterObj'] = MesosCluster.objects.get(clusterName=clsname)
        context['masterNodes'] = MesosClusterDetail.objects.filter(Q(clusterName=clsname),Q(nodeType=1))
        context['zookeeperNodes'] = MesosClusterDetail.objects.filter(Q(clusterName=clsname),Q(nodeType=2))
        context['marathonNodes'] = MesosClusterDetail.objects.filter(Q(clusterName=clsname),Q(nodeType=3))
        context['haproxyNodes'] = MesosClusterDetail.objects.filter(Q(clusterName=clsname),Q(nodeType=4))
        context['slaveNodes'] = MesosClusterDetail.objects.filter(Q(clusterName=clsname),Q(nodeType=5))
        return context

def cluster_docker_log(request):
    if request.method == "POST":
        line = int(request.POST.get('line'))
        host = request.POST.get('host')
        containerName = request.POST.get('container')
        containerID = MesosClusterDetail.objects.get(Q(host=host,containerName=containerName)).containerID
        sock = DockerClient(base_url='http://{}:6071'.format(host))
        log = sock.api.logs(containerID,timestamps=False,tail=line)
        log = log.replace('\r\n','<br />')
        # info
        log = log.replace('\x1b[34m','<span class="blue"> ')
        log = log.replace('\x1b[0;39m',' </span>')
        # error
        log = log.replace('\x1b[1;31m','<span class="red"> ')
        log = log.replace('\x1b[0;39m',' </span>')
        return JsonResponse({"data":log})
    
def cluster_docker_update(request):
    if request.method == "POST":
        host = request.POST.get('host')
        containerName = request.POST.get('container')
        action = request.POST.get('action')
        containerObj = MesosClusterDetail.objects.get(Q(host=host,containerName=containerName))
        sock = DockerClient(base_url='http://{}:6071'.format(host))
        status = 400
        msg = ''
        if action == 'start':
            try:
                sock.api.start(containerObj.containerID)
            except Exception as e:
                msg = str(e)
            else:
                containerObj.containerStatus = 1
                containerObj.save()
                status = 200
        elif action == 'stop':
            sock.api.stop(containerObj.containerID)
            containerObj.containerStatus = 2
            containerObj.save()
            status = 200
        else:
            msg = 'the action {} is not support!'.format(action)
        return JsonResponse({'code':status,'msg':msg})
    
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
        form = self.get_form()
        clusterName = request.POST.get('clusterName')
        if form.is_valid():
            status = True
            form.save(commit=True)
            MesosClusterOverview.objects.create(clusterName=clusterName)
        else:
            status = False
        return JsonResponse({'status':status,'msg':form.errors})

def mesos_cluster_deploy(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
        clusterObj = MesosCluster.objects.get(id=cluster_id)
        clusterObj.status = 2
        clusterObj.save()
        mesos_cluster_deploy_task.apply_async(args=(clusterObj,MesosDeployLog,MesosClusterDetail))
    return JsonResponse({'status':200})

def mesos_cluster_start(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
    return JsonResponse({'status':200})

def mesos_cluster_stop(request):
    if request.method == 'POST':
        cluster_id = request.POST.get('cluster_id')
    return JsonResponse({'status':200})

def mesos_cluster_clean(request):
    if request.method == 'POST':
        cluster_name = request.POST.get('cluster_name')
        detailObjs = MesosClusterDetail.objects.filter(clusterName=cluster_name)
        for obj in detailObjs:
            try:
                sock = DockerClient(base_url=obj.host+':6071')
                sock.api.remove_container(obj.containerName, v=True, force=True)
                obj.delete()
            except Exception as e:
                msg = str(e)
                return JsonResponse({'status':400,'msg':msg})
        MesosCluster.objects.filter(clusterName=cluster_name).update(status=1)
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
    