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
from django.views.generic import TemplateView,DeleteView,FormView,ListView
from models import MesosDeployLog,MesosMaster,MesosNodeStatus,IdleHost,\
MesosMarathon,MesosHaproxy,RepositoryImage,MesosSlave
from asset.models import AssetHost
from forms import MesosMasterForm,MesosMarathonForm,MesosHaproxyForm,MesosSlaveForm
from tasks.celery_tasks import mesos_cluster_deploy_task
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
            IdleHostQuerySet = IdleHost.objects.filter(assign_status=1)
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=user_id)
            IdleHostQuerySet = IdleHost.objects.filter(Q(owner_id=user_id),Q(assign_status=1))
        context['assethosts'] = assetHostQuerySet
        context['paashosts'] = IdleHostQuerySet
        context['total_host_count'] = len(assetHostQuerySet)
        return context

class MesosIdleHostAdd(TemplateView):
    template_name = ''
    def post(self,request):
        #get-an-array-in-django-posted-via-ajax
        checked_host_list = request.POST.getlist('checked_host_array[]')
        user_id = request.session.get('_user_id')
        msg = ''
        status = True
        for host in checked_host_list:
            print host
            try:
                hostObj = AssetHost.objects.get(private_ip=host)
                IdleHost.objects.create(host=hostObj,owner_id=user_id)
            except Exception as e:
                msg = msg+str(e)
                status = False
        return JsonResponse({'status':status,'msg':msg})

class MesosIdleHostDelete(DeleteView):
    model = IdleHost
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('MesosIdleHostList')
    def post(self, request, *args, **kwargs):
        idleHostId = int(request.POST.get('pk'))
        status = True
        msg = ''
        try:
            IdleHost.objects.get(id=idleHostId).delete()
        except Exception as e:
            msg = str(e)
            status = False
        return JsonResponse({'status':status,'msg':msg})
    
class MesosAddCluster(FormView):
    form_list = [MesosMasterForm,MesosMarathonForm,MesosHaproxyForm,MesosSlaveForm]
    form_class = MesosMasterForm
    success_url = reverse_lazy('MesosList')
    template_name = 'paas/cluster/mesos/MesosAddCluster.html'
    def get_context_data(self, **kwargs):
        context = super(MesosAddCluster, self).get_context_data(**kwargs)
        user_id = self.request.session.get('_user_id')
        if user_id == 1:
            assetHostQuerySet = IdleHost.objects.filter(assign_status=1)
        else:
            assetHostQuerySet = IdleHost.objects.filter(Q(owner_id=user_id),Q(assign_status=1))
        context['hosts'] = assetHostQuerySet
        context['imgs'] = RepositoryImage.objects.filter(label=1)
        return context
    
    def post(self, *args, **kwargs):
        for formcls in self.form_list:
            self.form_class = formcls
            form = self.get_form()
            if form.is_valid():
                form.save(commit=True)
            else:
                return JsonResponse({'status':False,'msg':form.errors})
        #把各节点主机列表写入 MesosNodeStatus表
        self.insert_MesosNodeStatus()
        return JsonResponse({'status':True})
    
    def insert_MesosNodeStatus(self):
        clusterName = self.request.POST.get('clusterName')
        master_hosts_list = self.request.POST.getlist('masterDeploy')
        marathon_hosts_list = self.request.POST.getlist('marathonDeploy')
        haproxy_hosts_list = self.request.POST.getlist('haproxyDeploy')
        slave_hosts_list = self.request.POST.getlist('slaveDeploy')
        marathonID = self.request.POST.get('marathonID')
        haproxyID = self.request.POST.get('haproxyID')
        slaveLabel = self.request.POST.get('slaveLabel')
        #把IdleHost表中主机改成已分配状态
        all_hosts_list = set(master_hosts_list+marathon_hosts_list+haproxy_hosts_list+slave_hosts_list)
        set_idle_host_assign_status(all_hosts_list,2)
        #把节点信息写入MesosNodeStatus表
        insert_MesosNodeStatus_forMaster(clusterName, master_hosts_list)
        insert_MesosNodeStatus_forMarathon(clusterName, marathon_hosts_list, marathonID)
        insert_MesosNodeStatus_forHaproxy(clusterName, haproxy_hosts_list, haproxyID)
        insert_MesosNodeStatus_forSlave(clusterName, slave_hosts_list, slaveLabel)

#部署完整的集群(包含master,marathon,haproxy,slave)
class MesosDeployCluster(TemplateView):
    template_name = ''
    def post(self,request):
        clusterName = request.POST.get('cluster_name')
        masterQSet = MesosMaster.objects.get(clusterName=clusterName)
        masterQSet.status = 2
        masterQSet.save()
        celery_id = mesos_cluster_deploy_task.apply_async(args=('cluster','',clusterName,'集群部署','host',True))
        return JsonResponse({'status':200,'celery_id':str(celery_id)})

class MesosOverview(TemplateView):
    template_name = 'paas/cluster/mesos/MesosClusterOverview.html'
    def get_context_data(self, **kwargs):
        context = super(MesosOverview,self).get_context_data(**kwargs)
        context['clsObj'] = MesosMaster.objects.get(clusterName=kwargs['clsname'])
        return context

#集群部署环境清理,只需要删除容器，和改变master集群的状态,其他状态不用改变如(marathon集群)
class MesosCleanCluster(TemplateView):
    template_name = ''
    def post(self,request):
        cluster_name = request.POST.get('cluster_name')
        detailObjs = MesosNodeStatus.objects.filter(Q(clusterName=cluster_name),
                                                    Q(containerStatus=1)|Q(containerStatus=2)|Q(containerStatus=3))
        for obj in detailObjs:
            try:
                sock = DockerClient(base_url=obj.host+':6071')
                sock.api.remove_container(obj.containerName, v=True, force=True)
                obj.delete()
            except Exception as e:
                msg = str(e)
                return JsonResponse({'status':400,'msg':msg})
        MesosMaster.objects.filter(clusterName=cluster_name).update(status=1)
        return JsonResponse({'status':200})

class MesosDeleteCluster(DeleteView):
    model = MesosMaster
    pk_url_kwarg = 'pk'
    template_name = ''
    #从MesosNodeStatus中获取某个master集群的所有主机（去重后的列表）
    def get_cluster_all_hosts(self,clusterName):
        hostObjs = MesosNodeStatus.objects.filter(clusterName=clusterName).values('host').distinct()
        host_list = []
        for hostobj in hostObjs:
            host_list.append(hostobj['host'])
        return host_list
    def post(self,request):
        cluster_id = int(request.POST.get('cluster_id'))
        try:
            masterObj = MesosMaster.objects.get(id=cluster_id)
            clusterName = masterObj.clusterName
            masterObj.delete()
        except Exception as e:
            status = 400
            msg = str(e)
        else:
            #释放被删集群的主机到空闲主机列表
            host_list = self.get_cluster_all_hosts(clusterName)
            set_idle_host_assign_status(host_list, 1)
            
            #删除此master集群下的所有其他组件集群
            MesosMarathon.objects.filter(clusterName=clusterName).delete()
            MesosHaproxy.objects.filter(clusterName=clusterName).delete()
            MesosSlave.objects.filter(clusterName=clusterName).delete()
            MesosNodeStatus.objects.filter(clusterName=clusterName).delete()
            status = 200
            msg = ''
        return JsonResponse({'status':status,'msg':msg})
        
class MesosClusterList(ListView):
    model = MesosMaster
    context_object_name = 'cluster_list'
    template_name = 'paas/cluster/mesos/MesosClusterList.html'
    def count_cluster_node_num(self):
        clusterInfo = {}
        nodeInfor = {}
        masterQuerysets = MesosMaster.objects.all()
        for queryset in masterQuerysets:
            clusterName = queryset.clusterName
            clusterInfo[clusterName] = {'marathon':0,'haproxy':0,'slave':0}
            nodeInfor[clusterName] = {'marathon':0,'haproxy':0,'slave':0}
            marathonQuerysets = MesosMarathon.objects.filter(clusterName=clusterName)
            haproxyQuerysets = MesosHaproxy.objects.filter(clusterName=clusterName)
            slaveQuerysets = MesosSlave.objects.filter(clusterName=clusterName)
            queryset_dict = {'marathon':marathonQuerysets,'haproxy':haproxyQuerysets,'slave':slaveQuerysets}
            clusterInfo[clusterName]['marathon'] = len(marathonQuerysets)
            clusterInfo[clusterName]['haproxy'] = len(haproxyQuerysets)
            clusterInfo[clusterName]['slave'] = len(slaveQuerysets)
            for key,qss in queryset_dict.items():
                node_count = 0
                for qs in qss:
                    if key == 'marathon':
                        nodeName = qs.marathonID
                    elif key == 'haproxy':
                        nodeName = qs.haproxyID
                    else:
                        nodeName = qs.slaveLabel
                    node = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=nodeName))
                    node_count = node_count + len(node)
                nodeInfor[clusterName][key] = node_count
        return {'clusterCount':clusterInfo,'nodeCount':nodeInfor}
    
    def get_context_data(self, **kwargs):
        context = super(MesosClusterList,self).get_context_data(**kwargs)
        info_dict = self.count_cluster_node_num()
        context['clusterCount']=info_dict['clusterCount']
        context['nodeCount']=info_dict['nodeCount']
        return context
    
class MesosMasterDetail(TemplateView):
    template_name = 'paas/cluster/mesos/detail/MesosMasterDetail.html'
    def get_context_data(self, **kwargs):
        clusterName = kwargs['clsname']
        context = super(MesosMasterDetail,self).get_context_data(**kwargs)
        masterObj = MesosMaster.objects.get(clusterName=clusterName)
        context['masterObj'] = masterObj
        context['masterNodes'] = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=clusterName))
        context['zookeeperNodes'] = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName='zookeeper'))
        context['clusterEnv'] = MesosDeployLog.objects.filter(cluster_name=clusterName).order_by('-start_time')
        return context
    
class MesosMarathonDetail(TemplateView):
    template_name = 'paas/cluster/mesos/detail/MesosMarathonDetail.html'
    def get_context_data(self, **kwargs):
        clusterName = kwargs['clsname']
        masterObj = MesosMaster.objects.get(clusterName=clusterName)
        context = super(MesosMarathonDetail,self).get_context_data(**kwargs)
        #获取某master集群下N套marathon集群
        marathonObjs = MesosMarathon.objects.filter(clusterName=clusterName)
        context['marathonObj'] = marathonObjs
        #获取一套marathon集群的所有queryset,  nodeName= marathonID
        marathonNodeDict = {}
        for marathonObj in marathonObjs:
            nodeName = marathonObj.marathonID
            marathonNodeDict[nodeName]= MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=nodeName))
        context['marathonNodes'] = marathonNodeDict
        context['masterObj'] = masterObj
        return context
    
class MesosHaproxyDetail(TemplateView):
    template_name = 'paas/cluster/mesos/detail/MesosHaproxyDetail.html'
    def get_context_data(self, **kwargs):
        clusterName = kwargs['clsname']
        masterObj = MesosMaster.objects.get(clusterName=clusterName)
        context = super(MesosHaproxyDetail,self).get_context_data(**kwargs)
        haproxyObjs = MesosHaproxy.objects.filter(clusterName=clusterName)
        context['haproxyObj'] = haproxyObjs
        #获取一套marathon集群的所有queryset,  nodeName= marathonID
        haproxyNodeDict = {}
        for haproxyObj in haproxyObjs:
            nodeName = haproxyObj.haproxyID
            haproxyNodeDict[nodeName]= MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=nodeName))
        context['haproxyNodes'] = haproxyNodeDict
        context['masterObj'] = masterObj
        return context

class MesosSlaveDetail(TemplateView):
    template_name = 'paas/cluster/mesos/detail/MesosSlaveDetail.html'
    def get_context_data(self, **kwargs):
        clusterName = kwargs['clsname']
        masterObj = MesosMaster.objects.get(clusterName=clusterName)
        context = super(MesosSlaveDetail,self).get_context_data(**kwargs)
        #获取master下所有slave 集群
        slaveObjs = MesosSlave.objects.filter(clusterName=clusterName)
        context['slaveObj'] = slaveObjs
        #获取一套marathon集群的所有queryset,  nodeName= marathonID
        slaveNodeDict = {}
        for slaveObj in slaveObjs:
            nodeName = slaveObj.slaveLabel
            slaveNodeDict[nodeName]= MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=nodeName))
        context['slaveNodes'] = slaveNodeDict
        context['masterObj'] = masterObj
        return context


#添加marathon,haproxy,slave集群, slave单点    
class MesosAddNode(FormView):
    formClsDict = {'marathon':MesosMarathonForm,'haproxy':MesosHaproxyForm,'slave':MesosSlaveForm}
    form_class = MesosSlaveForm
    #使用master主机 集群名，为marathon注册master生成  masterZK  url
    def gen_masterZK_for_marathon(self,zk_hosts,clusterName):
        master_zk = 'zk://'
        for i in range(len(zk_hosts)):
            if i == len(zk_hosts) - 1:
                master_zk = master_zk + zk_hosts[i]+':2181/'+clusterName
            else:
                master_zk = master_zk + zk_hosts[i]+':2181,'
        return master_zk
    
    #使用某集群下的所有marathon集群，为bamboo注册marathon生成 marathonZK url
    def gen_marathonZK_for_haproxy(self,marathonObj):
        nodeName = marathonObj.marathonID
        clusterName = marathonObj.clusterName
        marathon_hosts = []
        querysets = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=nodeName))
        for queryset in querysets:
            marathon_hosts.append(queryset.host)
        marathon_zk = ''
        for i in range(len(marathon_hosts)):
            if i == len(marathon_hosts) - 1:
                marathon_zk = marathon_zk+'http://{}:{}'.format(marathon_hosts[i],marathonObj.marathonPort)
            else:
                marathon_zk = marathon_zk+'http://{}:{},'.format(marathon_hosts[i],marathonObj.marathonPort)
        return marathon_zk
    
    #批量保存添加的slave 节点
    def save_node(self,clusterName,poolName,hosts):
        slave_list = []
        for host in hosts:
            slave_list.append(MesosNodeStatus(clusterName=clusterName,nodeName=poolName,host=host,containerName='mesos-slave'))
        try:
            MesosNodeStatus.objects.bulk_create(slave_list)
        except Exception as e:
            return {'status':False,'msg':e.message}
        else:
            return {'status':True}
    
    def save_node_cluster(self,clusterName,nodeType):
        msg = ''
        if nodeType == 'marathon':
            marathonID = self.request.POST.get('marathonID')
            hosts_list = self.request.POST.getlist('marathonDeploy')
            try:
                insert_MesosNodeStatus_forMarathon(clusterName, hosts_list, marathonID)
            except Exception as e:
                msg = e.message
            else:
                status = True
            poolName = marathonID
            
        elif nodeType == 'haproxy':
            haproxyID = self.request.POST.get('haproxyID')
            hosts_list = self.request.POST.getlist('haproxyDeploy')
            try:
                insert_MesosNodeStatus_forHaproxy(clusterName, hosts_list, haproxyID)
            except Exception as e:
                msg = e.message
            else:
                status = True
            poolName = haproxyID
            
        elif nodeType == 'slave':
            slaveLabel = self.request.POST.get('slaveLabel')
            hosts_list = self.request.POST.getlist('slaveDeploy')
            try:
                insert_MesosNodeStatus_forSlave(clusterName, hosts_list, slaveLabel)
            except Exception as e:
                msg = e.message
            else:
                status = True
            poolName = slaveLabel
            
        stepName = '添加{}集群'.format(poolName)
        return {'status':status,'msg':msg,'poolName':poolName,'hosts':hosts_list,'stepName':stepName}
        
    def get_context_data(self, **kwargs):
        context = super(MesosAddNode,self).get_context_data(**kwargs)
        clusterName = self.request.GET.get('name')
        masterObj = MesosMaster.objects.get(clusterName=clusterName)
        marathonObjs = MesosMarathon.objects.filter(clusterName=clusterName)
        #获取集群zk所有主机IP
        querysets_zk = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=clusterName))
        zk_hosts = []
        for queryset_zk in querysets_zk:
            zk_hosts.append(queryset_zk.host)
        
        nodeType = self.request.GET.get('type')
        if nodeType == 'marathon' or nodeType == 'slave':
            master_zk = self.gen_masterZK_for_marathon(zk_hosts,clusterName)
            slaveObjs = MesosSlave.objects.filter(clusterName=clusterName)
            context['slaveObjs'] = slaveObjs
            context['master_zk'] = master_zk
        elif nodeType == 'haproxy':
            marathonEndpoint_list = []
            for marathonObj in marathonObjs:
                marathon_zk = self.gen_marathonZK_for_haproxy(marathonObj)
                marathonEndpoint_list.append(marathon_zk)
            context['marathonEndpoint_list'] = marathonEndpoint_list
            
        self.template_name = 'paas/cluster/mesos/add/{}_add.html'.format(nodeType)
        context['masterObj'] = masterObj
        context['hosts'] = IdleHost.objects.filter(assign_status=1)
        context['imgs'] = RepositoryImage.objects.filter(label=1)
        return context
    
    def post(self,request, *args, **kwargs):
        nodeType = request.POST.get('nodeType')
        clusterName = request.POST.get('clusterName')
        #这里需要如果是添加slave，需要判断是添加新资源池还是单节点
        if nodeType == 'slave':
            addType = request.POST.get('addType')
            if addType == 'singleNode':
                slaveDeploy = request.POST.getlist('slaveDeploy')
                poolName = request.POST.get('poolName')
                saveRes = self.save_node(clusterName,poolName,slaveDeploy)
                if saveRes['status']:
                    set_idle_host_assign_status(slaveDeploy, 2)
                    mesos_cluster_deploy_task.apply_async(args=(nodeType,poolName,clusterName,poolName+'池添加节点',slaveDeploy,False))
                    return JsonResponse({'code':200})
                else:
                    return JsonResponse({'code':400,'msg':saveRes['msg']})
        self.form_class = self.formClsDict[nodeType]
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            save_res = self.save_node_cluster(clusterName,nodeType)
            if save_res['status']:
                poolName = save_res['poolName']
                hosts = save_res['hosts']
                set_idle_host_assign_status(hosts, 2)
                stepName = save_res['stepName']
                mesos_cluster_deploy_task.apply_async(args=(nodeType,poolName,clusterName,stepName,hosts,False))
                return JsonResponse({'code':200})
            else:
                return JsonResponse({'code':400,'msg':save_res['msg']})
        else:
            return JsonResponse({'code':400,'msg':form.errors})

#删除marathon,haproxy,slave集群, slave单点    
class MesosDeleteNode(TemplateView):
    template_name = ''
    def del_docker(self,NodeObjs):
        for obj in NodeObjs:
            if obj.containerStatus in (1,2,3):
                try:
                    sock = DockerClient(base_url='http://{}:6071'.format(obj.host))
                    sock.api.remove_container(obj.containerName, v=True, force=True)
                except Exception as e:
                    return {'status':False,'msg':str(e.message)}
                else:
                    set_idle_host_assign_status([obj.host,], 1)
                    obj.delete()
            else:
                obj.delete()
                set_idle_host_assign_status([obj.host,], 1)
        return {'status':True}
    
    def del_node_for_cluster(self,request,del_type):
        clusterName = request.POST.get('clusterName')
        poolName = request.POST.get('poolName')
        NodeObjs = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(nodeName=poolName))
        del_res = self.del_docker(NodeObjs)
        #如果MesosNodeStatus中记录, 主机上容器都删除成功，开始删除集群记录
        if del_res['status']:
            if del_type == 'marathon':
                MesosMarathon.objects.filter(Q(clusterName=clusterName),Q(marathonID=poolName)).delete()
            elif del_type == 'haproxy':
                MesosHaproxy.objects.filter(Q(clusterName=clusterName),Q(haproxyID=poolName)).delete()
            else:
                MesosSlave.objects.filter(Q(clusterName=clusterName),Q(slaveLabel=poolName)).delete()
        return del_res
    
    def del_node_for_slave_single(self,request):
        host = request.POST.get('host')
        poolName = request.POST.get('poolName')
        obj = MesosNodeStatus.objects.get(Q(host=host),Q(nodeName=poolName))
        del_res = self.del_docker([obj,])
        return del_res
    
    def post(self,request):
        del_type = request.POST.get('type')
        if del_type == 'slaveSingleNode':
            res = self.del_node_for_slave_single(request)
        else:
            res = self.del_node_for_cluster(request,del_type)
        if res['status']:
            return JsonResponse({'code':200})
        else:
            return JsonResponse({'code':400,'msg':res['msg']})

def cluster_node_log(request):
    if request.method == "POST":
        line = int(request.POST.get('line'))
        host = request.POST.get('host')
        containerName = request.POST.get('container')
        containerID = MesosNodeStatus.objects.get(Q(host=host),Q(containerName=containerName)).containerID
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
    
def cluster_node_update(request):
    if request.method == "POST":
        host = request.POST.get('host')
        containerName = request.POST.get('container')
        action = request.POST.get('action')
        containerObj = MesosNodeStatus.objects.get(Q(host=host,containerName=containerName))
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



#设置空闲主机状态, hosts 是list,status值为1(未分配) 或 2(已分配)
def set_idle_host_assign_status(hosts,status):
    for host in hosts:
        assetObj = AssetHost.objects.get(private_ip=host)
        IdleHost.objects.filter(host_id=assetObj.id).update(assign_status=status)

class MesosClusterDeployResult(TemplateView):
    template_name = 'paas/cluster/mesos/MesosClusterDeployResult.html'
    def get_context_data(self, **kwargs):
        cluster_id = self.request.GET.get('cluster_id')
        celery_id = self.request.GET.get('celery_id')
        clusterObj = MesosMaster.objects.get(id=cluster_id)
        cluster_dict = model_to_dict(clusterObj)
        kwargs['cluster'] = cluster_dict
        kwargs['celery_id'] = celery_id
        return TemplateView.get_context_data(self, **kwargs)
    
    def post(self,request):
        celery_id = self.request.POST.get('celery_id')
        #first: to get the record of status=3 (finished)
        totalObj = MesosDeployLog.objects.filter(celery_id=celery_id)
        successObj = MesosDeployLog.objects.filter(Q(celery_id=celery_id),Q(is_read=False),Q(status=3))
        runObj = MesosDeployLog.objects.filter(Q(celery_id=celery_id),Q(status=2))
        failObj = MesosDeployLog.objects.filter(Q(celery_id=celery_id),Q(status=4))
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
            if len(totalObj) != 7:
                status ='running'
                data = ''
            else:
                status ='finished'
                data = ''
        return JsonResponse({'status':status,'data':data})
      
    
class ListNetwork(TemplateView):
    template_name = 'paas/resource/network.html'
   
    
class ListStorage(TemplateView):
    template_name = 'paas/resource/storage.html'
    
    
def insert_MesosNodeStatus_forMaster(clusterName,hosts_list):
    queryset_list = []
    for host in hosts_list:
        queryset_list.append(MesosNodeStatus(clusterName=clusterName,nodeName=clusterName,
                                             host=host,containerName='mesos-master'))
        queryset_list.append(MesosNodeStatus(clusterName=clusterName,nodeName='zookeeper',
                                             host=host,containerName='mesos-zookeeper'))
    MesosNodeStatus.objects.bulk_create(queryset_list)

def insert_MesosNodeStatus_forMarathon(clusterName,hosts_list,marathonID):
    queryset_list = []
    for host in hosts_list:
        queryset_list.append(MesosNodeStatus(clusterName=clusterName,nodeName=marathonID,
                                             host=host,containerName='mesos-marathon'))
    MesosNodeStatus.objects.bulk_create(queryset_list)

def insert_MesosNodeStatus_forHaproxy(clusterName,hosts_list,haproxyID):
    queryset_list = []
    for host in hosts_list:
        queryset_list.append(MesosNodeStatus(clusterName=clusterName,nodeName=haproxyID,
                                             host=host,containerName='haproxy-bamboo'))
    MesosNodeStatus.objects.bulk_create(queryset_list)
    
def insert_MesosNodeStatus_forSlave(clusterName,hosts_list,slaveLabel):
    queryset_list = []
    for host in hosts_list:
        queryset_list.append(MesosNodeStatus(clusterName=clusterName,nodeName=slaveLabel,
                                             host=host,containerName='mesos-slave'))
    MesosNodeStatus.objects.bulk_create(queryset_list)
    