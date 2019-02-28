#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月23日

@author: yangxu
'''
from __future__ import absolute_import
from celery import task
import traceback
import requests
from webapp.models import HostImport,AssetHost,HostEvent,MesosMaster,MesosNodeStatus,\
MesosMarathon,MesosHaproxy,MesosSlave,MesosDeployLog,HostDisk,HostEth
from utils.ansibleAdHoc import myadhoc
from utils.ansibleplaybook import myplaybook
from utils.callback import CollectAssetInfoCallback
from utils.mesos_deploy import create_container,gen_zookeeper_env,gen_master_env,\
gen_marathon_env,gen_haproxy_env,gen_slave_env,check_docker_6071,gen_zookeeper_volume,\
gen_master_volume,gen_marathon_volume,gen_haproxy_volume,gen_slave_volume
import xlrd
from django.core.validators import validate_ipv4_address
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
import time
from docker import DockerClient

def override_ceel_value(value,typeobj):
    temp_value = str(value).strip()
    if len(temp_value) == 0:
        return None
    else:
        return typeobj(value)
    
    
def get_assets_data(full_filename):
    bk = xlrd.open_workbook(full_filename,encoding_override='utf-8')
    dataList = []
    try:
        sheet = bk.sheet_by_index(0)
        for i in range(2,sheet.nrows):
            asset = {}
            asset['private_ip'] = override_ceel_value(sheet.cell(i,0).value, str)
            asset['port'] = override_ceel_value(sheet.cell(i,1).value, int)
            asset['host_status'] = override_ceel_value(sheet.cell(i,2).value, int)
            asset['remote_user'] = override_ceel_value(sheet.cell(i,3).value, str)
            asset['remote_passwd'] = override_ceel_value(sheet.cell(i,4).value, str)
            asset['group_id'] = override_ceel_value(sheet.cell(i,5).value, int)
            asset['agent_is_install'] = override_ceel_value(sheet.cell(i,6).value, int)
            asset['serial'] = override_ceel_value(sheet.cell(i,7).value, str)
            asset['hostname'] = override_ceel_value(sheet.cell(i,8).value, str)
            asset['public_ip'] = override_ceel_value(sheet.cell(i,9).value, str)
            asset['cpu_no'] = override_ceel_value(sheet.cell(i,10).value, int)
            asset['cpu_model'] = override_ceel_value(sheet.cell(i,11).value, str)
            asset['memory'] = override_ceel_value(sheet.cell(i,12).value, int)
            asset['disk'] = override_ceel_value(sheet.cell(i,13).value, float)
            asset['os'] = override_ceel_value(sheet.cell(i,14).value, str)
            asset['kernel'] = override_ceel_value(sheet.cell(i,15).value, str)
            asset['machine_model'] = override_ceel_value(sheet.cell(i,16).value, str)
            asset['position'] = override_ceel_value(sheet.cell(i,17).value, str)
            asset['operate_status'] = override_ceel_value(sheet.cell(i,18).value, int)
            asset['department'] = override_ceel_value(sheet.cell(i,19).value, str)
            asset['owner_id'] = override_ceel_value(sheet.cell(i,20).value, int)
            dataList.append(asset)
    except Exception,e:
        print e
        return []
    return dataList

''' 
check required field whether Null 
check private_ip field whether valid
check port,host_stauts,group_id field where int type
'''
def asset_format_check(import_id,datalist):
    check_result = {'status':False,
                    'result':{
                            'private_ip':None,
                            'port':None,
                            'host_status':None,
                            'remote_user':None,
                            'remote_passwd':None,
                            'group_id':None
                              }
                    }
    def field_has_null(data):
            has_null = False
            if data['private_ip'] is None:
                has_null = True
                check_result['result']['private_ip'] = 'private_ip is required'
            if data['port'] is None:
                has_null = True
                check_result['result']['port'] = 'port is required'
            if data['host_status'] is None:
                has_null = True
                check_result['result']['host_status'] = 'host_status is required'
            if data['remote_user'] is None:
                has_null = True
                check_result['result']['remote_user'] = 'user is required'
            if data['remote_passwd'] is None:
                has_null = True
                check_result['result']['remote_passwd'] = 'password is required'
            if data['group_id'] is None:
                has_null = True
                check_result['result']['group_id'] = 'group_id is required'
            return has_null
    for index,data in enumerate(datalist):
        if not field_has_null(data):
            try:
                validate_ipv4_address(data['private_ip'])
            except ValidationError:
                check_result['status'] = False
                check_result['result']['private_ip'] = 'Enter a valid IPv4 address'
                update_import_status(import_id, datalist, False, index+1)
            else:
                if isinstance(int(data['port']),int)\
                        and isinstance(data['host_status'],int)\
                        and isinstance(data['group_id'],int):
                    AssetHost.objects.create(**data)
                    update_import_status(import_id, datalist, True, index+1)
                else:
                    update_import_status(import_id, datalist, False, index+1)
        else:
            update_import_status(import_id, datalist, False, index+1)
                    
            
def update_import_status(import_id,datalist,line_type,line_no):
    queryobj = HostImport.objects.get(id=import_id)
    if line_type:
        queryobj.succeeded_line = line_no
    else:
        queryobj.failure_line = line_no
        old_err_line_str = queryobj.err_line
        if old_err_line_str is None:
            new_err_line_str = str(line_no)
        else:
            new_err_line_str = old_err_line_str+','+str(line_no)
        queryobj.err_line = new_err_line_str
    if len(datalist) == line_no:
            queryobj.is_finished = True
    queryobj.save()
    
       

@task(name='process_asset_import_task')
def process_asset_import_task(import_id,full_filename):
    datalist = get_assets_data(full_filename)
    asset_format_check(import_id,datalist)

def save_ansible_mounts(mount_list,host_queryset):
    HostDisk.objects.filter(host=host_queryset).delete()
    querylist = []
    for mount in mount_list:
        mount['host'] = host_queryset
        querylist.append(HostDisk(**mount))
    HostDisk.objects.bulk_create(querylist)

def save_ansible_ethernet(eth_list,host_queryset):
    HostEth.objects.filter(host=host_queryset).delete()
    querylist = []
    for one_eth in eth_list:
        one_eth['host'] = host_queryset
        querylist.append(HostEth(**one_eth))
    HostEth.objects.bulk_create(querylist)
    
        
@task(name='collect_host_info_task')
def collect_host_info_task(asset_id,private_ip,port,user,password,action_num):
    tasks = [dict(action=dict(module='setup', args=''),register='shell_out'),]
    group = 'all'
    my=myadhoc(tasks,group,private_ip+',',port,user,password,CollectAssetInfoCallback)
    my.run()
    queryset = AssetHost.objects.get(id=asset_id)
    collect_result = my.results_callback._result
    if collect_result['status'] == 'ok':
        queryset.serial = collect_result['result']['serial']
        queryset.hostname = collect_result['result']['hostname']
        queryset.public_ip = collect_result['result']['public_ip']
        queryset.cpu_no = collect_result['result']['cpu_no']
        queryset.cpu_model = collect_result['result']['cpu_model']
        queryset.memory = collect_result['result']['memory']
        queryset.disk = collect_result['result']['disk']
        queryset.os = collect_result['result']['os']
        queryset.kernel = collect_result['result']['kernel']
        queryset.machine_model = collect_result['result']['machine_model']
        queryset.save()
        save_ansible_ethernet(collect_result['result']['eth_list'], queryset)
        save_ansible_mounts(collect_result['result']['mounts'], queryset)
        HostEvent.objects.create(host_id=queryset.id,action=action_num,is_succeeded=True)
    elif collect_result['status'] == 'failed':
        HostEvent.objects.create(host_id=queryset.id,action=action_num,is_succeeded=False,
                                 content=u'认证失败')
    elif collect_result['status'] == 'unreachable':
        HostEvent.objects.create(host_id=queryset.id,action=action_num,is_succeeded=False,
                                 content=u'主机不可达')
@task(name='playbook_execute_task')
def playbook_execute_task(task_id,playbook_full_name,playbook_full_host,callback,model):
    my=myplaybook(playbook_full_name,playbook_full_host,callback,task_id)
    execute_host_count = my.run()
    if isinstance(execute_host_count, int):
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        obj = model.objects.get(task_id=task_id)
        obj.end_time = end_time
        end_time_seconds = time.mktime(time.strptime(str(end_time),'%Y-%m-%d %H:%M:%S'))
        start_time_seconds = time.mktime(time.strptime(str(obj.start_time),'%Y-%m-%d %H:%M:%S'))
        obj.total_time = int(end_time_seconds - start_time_seconds)
        obj.status = 1
        obj.save()
    else:
        model.objects.get(task_id=task_id)
        obj.status = 3
        obj.msg = execute_host_count # exception msg
        obj.save()
        
#检查部署mesos集群的所有主机6071端口是否连通
def is_connect(celery_id,clusterName,hosts,name):
    #log_model == MesosDeployLog
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj = MesosDeployLog.objects.create(celery_id=celery_id,cluster_name=clusterName,name=name,
                                              step_name='checkCon',start_time=start_time,status=2)
    status = True
    res = check_docker_6071(hosts)
    if res['status']:
        log_obj.status = 3
    else:
        log_obj.status = 4
        log_obj.msg = res['msg']
        status = False
    log_obj.finished_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj.save()
    return status

def deploy_node(hosts,img,env,volumes,containerName,celery_id,clusterName,name,step_name,nodeName,masterQSet):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj = MesosDeployLog.objects.create(celery_id=celery_id,cluster_name=clusterName,name=name,
                                       step_name=step_name,start_time=start_time,status=2)
    for host in hosts:
        res = create_container(host, img, env[host], volumes, containerName)
        if res['status']:
            containerObj = res['containerObj']
            containerID = containerObj.id
            #改变节点容器的状态记录--状态为"创建", 写入containerID
            NodeStatusObj = MesosNodeStatus.objects.get(clusterName=clusterName,nodeName=nodeName,host=host,containerName=containerName)
            NodeStatusObj.containerID=containerID
            NodeStatusObj.containerStatus=3
            NodeStatusObj.save()
            try:
                containerObj.start()
            except Exception as e:
                msg = str(e)
                #如果容器启动失败,记录失败日志并返回
                log_obj.status = 4
                log_obj.msg = msg
                log_obj.save()
                return {'status':False}
            else:
                #启动节点成功，更改容器的状态记录--状态为"运行" 
                NodeStatusObj.containerStatus = 1
                NodeStatusObj.save()
        else:
            #如果容器创建失败,记录失败日志并返回
            log_obj.status = 4
            log_obj.msg = res['msg']
            log_obj.save()
            return {'status':False}
    #如果当前步骤如 deployZK,所有主机都部署成功（创建，启动）,更改状态为成功并返回 True
    log_obj.status = 3
    log_obj.finished_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj.save()
    return {'status':True}


def gen_env_volumes_containerName(querySet,zk_hosts,clusterName,step_name,hosts):
    #生成env dict(以主机为key) volumes dict, containerName
    if step_name == 'deployZK':
        containerName = 'mesos-zookeeper'
        env = gen_zookeeper_env(hosts)
        volumes = gen_zookeeper_volume()
    elif step_name == 'deployMaster':
        containerName = 'mesos-master'
        env = gen_master_env(hosts, clusterName, querySet.masterPort)
        volumes = gen_master_volume()
    elif step_name == 'deployMT':
        containerName = 'mesos-marathon'
        env = gen_marathon_env(hosts, querySet.marathonID, querySet.marathonZK)
        volumes = gen_marathon_volume()
    elif step_name == 'deployHA':
        containerName = 'haproxy-bamboo'
        env = gen_haproxy_env(hosts, querySet.haproxyID, querySet.bambooPort, zk_hosts, querySet.haproxyMarathon)
        volumes = gen_haproxy_volume()
    elif step_name == 'deploySlave':
        containerName = 'mesos-slave'
        env = gen_slave_env(hosts, querySet.slaveZK, querySet.slaveLabel)
        volumes = gen_slave_volume()
    else:
        return False
    return {'env':env,'volumes':volumes,'containerName':containerName}

def get_node_hosts(clusterName,nodeName):
    #从MesosNodeStatus表中 获取对应集群的主机，如获取clusterName=mesos01 & nodeName=haproxy01的主机
    objs = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                          Q(nodeName=nodeName))
    hosts_list = []
    for obj in objs:
        hosts_list.append(obj.host)
    return hosts_list

def gen_step_img_hosts_list(nodeType,nodeName,clusterName,is_master):
    #生成部署信息
    masterQst = MesosMaster.objects.get(clusterName=clusterName)
    masterHosts = get_node_hosts(clusterName, clusterName)
    if nodeType == 'cluster':
        info_list = [{'step':'deployZK','img':'','hosts':[],'queryset':''},
                 {'step':'deployMaster','img':'','hosts':[],'queryset':''},
                 {'step':'deployMT','img':'','hosts':[],'queryset':''},
                 {'step':'deployHA','img':'','hosts':[],'queryset':''},
                 {'step':'deploySlave','img':'','hosts':[],'queryset':''},
                ]
        marathonQst = MesosMarathon.objects.get(Q(clusterName=clusterName),Q(is_master=is_master))
        haproxyQst = MesosHaproxy.objects.get(Q(clusterName=clusterName),Q(is_master=is_master))
        slaveQst = MesosSlave.objects.get(Q(clusterName=clusterName),Q(is_master=is_master))
        marathonHosts = get_node_hosts(clusterName, marathonQst.marathonID)
        haproxyHosts = get_node_hosts(clusterName, haproxyQst.haproxyID)
        slaveHosts = get_node_hosts(clusterName, slaveQst.slaveLabel)
        info_list[0]['img'] = masterQst.zkImage
        info_list[0]['hosts'] = masterHosts
        info_list[0]['queryset'] = masterQst
        
        info_list[1]['img'] = masterQst.masterImage
        info_list[1]['hosts'] = masterHosts
        info_list[1]['queryset'] = masterQst
        
        info_list[2]['img'] = marathonQst.marathonImage
        info_list[2]['hosts'] = marathonHosts
        info_list[2]['queryset'] = marathonQst
        
        info_list[3]['img'] = haproxyQst.haproxyImage
        info_list[3]['hosts'] = haproxyHosts
        info_list[3]['queryset'] = haproxyQst
        
        info_list[4]['img'] = slaveQst.slaveImage
        info_list[4]['hosts'] = slaveHosts
        info_list[4]['queryset'] = slaveQst
        
    elif nodeType == 'marathon':
        info_list = [{'step':'deployMT','img':'','hosts':[],'queryset':''},]
        marathonQst = MesosMarathon.objects.get(Q(clusterName=clusterName),Q(marathonID=nodeName))
        marathonHosts = get_node_hosts(clusterName, marathonQst.marathonID)
        info_list[0]['img'] = marathonQst.marathonImage
        info_list[0]['hosts'] = marathonHosts
        info_list[0]['queryset'] = marathonQst
    elif nodeType == 'haproxy':
        info_list = [{'step':'deployHA','img':'','hosts':[],'queryset':''},]
        haproxyQst = MesosHaproxy.objects.get(Q(clusterName=clusterName),Q(haproxyID=nodeName))
        haproxyHosts = get_node_hosts(clusterName, haproxyQst.haproxyID)
        info_list[0]['img'] = haproxyQst.haproxyImage
        info_list[0]['hosts'] = haproxyHosts
        info_list[0]['queryset'] = haproxyQst
    elif nodeType == 'slave':
        info_list = [{'step':'deploySlave','img':'','hosts':[],'queryset':''},]
        slaveQst = MesosSlave.objects.get(Q(clusterName=clusterName),Q(slaveLabel=nodeName))
        slaveHosts = get_node_hosts(clusterName, slaveQst.slaveLabel)
        info_list[0]['img'] = slaveQst.slaveImage
        info_list[0]['hosts'] = slaveHosts
        info_list[0]['queryset'] = slaveQst
    else:
        return False
    
    return info_list

def get_all_hosts(deploy_info):
    #为连通性检查生成集群所有主机列表(set去重)
    hosts_list = []
    for oneInfo in deploy_info:
        hosts_list = hosts_list+oneInfo['hosts']
    return set(hosts_list)

def get_nodeName_for_cluster(clusterName,step_name,oneInfo):
    #获取nodeName , 只有当当nodeType = cluster时，nodeName是空才需要获取,部署某个组件集群时，nodeName是提供的
    #在部署完成某一步后，如deployMT,需要nodeName去设置被部署的marathon集群状态
    if step_name == 'deployMT':
        nodeName = oneInfo['queryset'].marathonID
    elif step_name == 'deployHA':
        nodeName = oneInfo['queryset'].haproxyID
    elif step_name == 'deploySlave':
        nodeName = oneInfo['queryset'].slaveLabel
    elif step_name == 'deployZK':
        nodeName = 'zookeeper'
    else:
        nodeName = clusterName
    return nodeName

def set_cluster_status(clusterName,nodeName,step_name,status):
    #这里必须使用实体对象进行状态改变，使用引用的queryset对象设置会不成功
    if step_name == 'deployMT':
        obj = MesosMarathon.objects.get(Q(clusterName=clusterName),Q(marathonID=nodeName))
    elif step_name == 'deployHA':
        obj = MesosHaproxy.objects.get(Q(clusterName=clusterName),Q(haproxyID=nodeName))
    elif step_name == 'deploySlave':
        obj = MesosSlave.objects.get(Q(clusterName=clusterName),Q(slaveLabel=nodeName))
    else:
        return True
    obj.status = status
    obj.save()
    
@task(name='mesos_cluster_deploy_task',bind=True)
def mesos_cluster_deploy_task(self,nodeType,nodeName,clusterName,name,hosts,is_master):
    #nodeType可传递: cluster(nodeName=None),
    #marathon(nodeName=marathonID),haproxy(nodeName=haproxyID),slave(nodeName=slaveLabel)
    celery_id = self.request.id
    masterQSet = MesosMaster.objects.get(clusterName=clusterName)
    #生成部署信息,这里使用list,因为dict不是排序的,因为后面的部署要求是顺序的
    try:
        deploy_info = gen_step_img_hosts_list(nodeType, nodeName, clusterName,is_master)
    except:
        exe_info = traceback.print_exc()
        print exe_info
        if nodeType == 'cluster':
            masterQSet.status = 3
            masterQSet.save()
        return False
    if nodeType == 'cluster':
        hosts = get_all_hosts(deploy_info)
    #检查部署mesos集群的所有主机6071端口是否连通
    check_con_result = is_connect(celery_id, clusterName,hosts,name)
    if not check_con_result:
        if nodeType == 'cluster':
            masterQSet.status = 3
            masterQSet.save()
        return 'failed'
    
    #下载部署mesos 各节点所需要的docker image
    from utils.mesos_deploy import download_img
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj = MesosDeployLog.objects.create(celery_id=celery_id,cluster_name=clusterName,name=name,
                                              step_name='imgDownload',start_time=start_time,status=2)
    for oneInfo in deploy_info:
        res = download_img(oneInfo['hosts'],oneInfo['img'])
        if not res['status']:
            log_obj.status = 4
            log_obj.msg = res['msg']
            log_obj.finished_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_obj.save()
            if nodeType == 'cluster':
                masterQSet.status = 3
                masterQSet.save()
            return 'failed'
    log_obj.finished_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_obj.status = 3
    log_obj.save()
   
    #创建mesos集群各节点，以容器方式运行
    for oneInfo in deploy_info:
        if nodeType == 'cluster':
            hosts = oneInfo['hosts']
        img = oneInfo['img']
        step_name = oneInfo['step']
        queryset = oneInfo['queryset']
        zk_hosts = get_node_hosts(clusterName, clusterName)
        #env_volumes是dict,里面的env是以ip为key的dict
        env_volumes_dict = gen_env_volumes_containerName(queryset, zk_hosts, clusterName, step_name, hosts)
        env = env_volumes_dict['env']
        volumes = env_volumes_dict['volumes']
        containerName = env_volumes_dict['containerName']
        #获取nodeName
        nodeName = get_nodeName_for_cluster(clusterName, step_name, oneInfo)
        #deploy_node内部会批量部署 某一步,如deployZK这一步可能包含5台主机
        deploy_res = deploy_node(hosts,img,env,volumes,containerName,celery_id,clusterName,name,step_name,nodeName,masterQSet)
        
        if deploy_res['status']:
            #如果部署成功,比如deployMT(部署marathon)成功,则把MesosMarathon表里对应的marathon集群状态设置为"成功"
            set_cluster_status(clusterName,nodeName,step_name,4)
        else:
            set_cluster_status(clusterName,nodeName,step_name,3)
            if nodeType == 'cluster':
                masterQSet.status = 3
                masterQSet.save()
            return 'failed'
    if nodeType == 'cluster':
        masterQSet.status = 4
        masterQSet.save()
    return True

@task(name='deploy_mesos_node_task',bind=True)
def deploy_mesos_node_task(self,queryset,log_model,NodeStatus_model,hosts):
    pass


@task(name='check_mesos_cluster_task')
def check_mesos_cluster_task():
    def statistics_mesos_master_resource(masterObj):
        clusterName = masterObj.clusterName
        masterNodes = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                                     Q(nodeName=clusterName),
                                                     Q(containerStatus=1))
        if len(masterNodes) != 0:
            host = masterNodes[0].host
            url = 'http://{}:{}{}'.format(host,masterObj.masterPort,'/metrics/snapshot')
            r = requests.get(url)
            if r.ok:
                res_dict = r.json()
                masterObj.cpu_used = res_dict['master/cpus_used']
                masterObj.cpu_total = res_dict['master/cpus_total']
                masterObj.memory_used = res_dict['master/mem_used']/1000
                masterObj.memory_total = res_dict['master/mem_total']/1000
                masterObj.disk_used = res_dict['master/disk_used']/1000
                masterObj.disk_total = res_dict['master/disk_total']/1000
                masterObj.save()
        return True
    
    def get_master_leader(masterObj):
        clusterName = masterObj.clusterName
        masterNodes = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                                     Q(nodeName=clusterName),
                                                     Q(containerStatus=1))
        if len(masterNodes) != 0:
            host = masterNodes[0].host
            url = 'http://{}:{}{}'.format(host,masterObj.masterPort,'/master/state')
            r = requests.get(url)
            if r.ok:
                res_dict = r.json()
                masterObj.leader = res_dict['leader_info']['hostname']
                masterObj.save()
        
    def get_distinct_hosts(nodes):
        hosts = []
        for node in nodes:
            hosts.append(node.host)
        return set(hosts)
    
    def container_is_running(host,containerName):
        sock = DockerClient(base_url='{}:6071'.format(host))
        cls = sock.containers.get(containerName)
        if cls.status == 'running':
            return True
        else:
            return False
    
    def get_cluster_status(clusterName,nodeName,port,url_context):
        #获取xx集群下，容器停止的记录条数
        DieNodes = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                                  Q(nodeName=nodeName),
                                                  Q(containerStatus=2))
        #获取xx集群下，容器运行的记录条数
        ActNodes = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                                  Q(nodeName=nodeName),
                                                  Q(containerStatus=1))
        #如果没有停止的,需要判断运行的服务是否可用
        if len(DieNodes) == 0 and len(ActNodes) != 0:
            status = 1
        #如果有停止的，也有运行的,需要判断运行的服务是否可用
        elif len(DieNodes) != 0 and len(ActNodes) != 0 :
            status = 2
        #没有运行的，直接把集群状态变为不可用
        elif len(ActNodes) == 0:
            status = 3
        
        #status = 1, status = 2 都要进行服务可用性判断
        if status !=3:
            host = ActNodes[0].host
            url = 'http://{}:{}{}'.format(host,port,url_context)
            try:
                r = requests.get(url)
            except:
                return 3
            else:
                if r.ok:
                    status = 1
                else:
                    status = 3
        return status
        
    
    #这里得到的是多个集群状态判断出的最终集群可用状态,如一个master下有2个marathon集群，一个集群可用，一个集群不可用那么整个marathon集群就是2(waring)
    def status_judge(status_list):
        if len(status_list) > 1:
            #1,2 都没有说明 是3 (danger==unavailable)
            if 1 not in status_list and 2 not in status_list:
                status = 3
            #(1,2)组合 = 2 , (2,3)组合 = 2
            elif 2 in status_list:
                status = 2
            #2 不在里面，只有1，3 , 如果3不在，就只有1
            elif 3 not in status_list:
                status = 1
            #如果1 不在，就只有3
            elif 1 not in status_list:
                status = 3
            else:
                status = 2
        else:
            status = status_list[0]
        return status
    
    def set_master_status(masterObj):
        master_status = masterObj.master_status
        marathon_status = masterObj.marathon_status
        haproxy_status = masterObj.haproxy_status
        bamboo_status = masterObj.bamboo_status
        slave_status = masterObj.slave_status
        status_list = [master_status,marathon_status,haproxy_status,bamboo_status,slave_status]
        if 3 in status_list:
            masterObj.status = 6
            masterObj.save()
        elif 2 in status_list:
            masterObj.status = 5
            masterObj.save()
        else:
            masterObj.status = 4
            masterObj.save()        
    
    def set_status(masterObj,check_type,url_context):
        clusterName=masterObj.clusterName
        if check_type == 'marathon':
            clusters = MesosMarathon.objects.filter(Q(clusterName=clusterName),Q(status=4)|Q(status=5)|Q(status=6))
        elif check_type == 'haproxy':
            clusters = MesosHaproxy.objects.filter(Q(clusterName=clusterName),Q(status=4)|Q(status=5)|Q(status=6))
        elif check_type == 'slave':
            clusters = MesosSlave.objects.filter(Q(clusterName=clusterName),Q(status=4)|Q(status=5)|Q(status=6))
        else:
            clusters = MesosMaster.objects.filter(Q(clusterName=clusterName),Q(status=4)|Q(status=5)|Q(status=6))
        #status_list保存各xx集群(如MesosMarathon)的状态，最后依据此来综合判断xx 是否可用
        status_list = []
        #获取此集群下的所有已部署的xx集群
        if len(clusters) > 0:
            for cluster in clusters:
                if check_type == 'marathon':
                    nodeName = cluster.marathonID
                    port = cluster.marathonPort
                elif check_type == 'haproxy':
                    nodeName = cluster.haproxyID
                    port = cluster.bambooPort
                elif check_type == 'slave':
                    nodeName = cluster.slaveLabel
                    port = cluster.slavePort
                else:
                    nodeName = cluster.clusterName
                    port = cluster.masterPort
                status = get_cluster_status(clusterName, nodeName, port,url_context)
                #根据整个集群所有node状态，服务状态来设置集群状态
                if status == 1:
                    cluster.status = 4
                elif status == 2:
                    cluster.status = 5
                elif status == 3:
                    cluster.status = 6
                cluster.save()
                status_list.append(status)
            status = status_judge(status_list)
            if check_type == 'marathon':
                masterObj.marathon_status = status
            elif check_type == 'haproxy':
                masterObj.haproxy_status = status
            elif check_type == 'slave':
                masterObj.slave_status = status
            else:
                masterObj.master_status = status
            masterObj.save()
        else:
            #没有部署成功的集群
            if check_type == 'marathon':
                masterObj.marathon_status = 4
            elif check_type == 'haproxy':
                masterObj.haproxy_status = 4
            elif check_type == 'slave':
                masterObj.slave_status = 4
            else:
                masterObj.master_status = 4
            masterObj.save()
   
    
    #1 获取已部署成功的集群
    MesosClusters = MesosMaster.objects.filter(Q(status=4)|Q(status=5)|Q(status=6))
    #2 获取某个集群所有主机containerStatus=1或2（并去重）,检查主机连通性
    for masterObj in MesosClusters:
        clusterName = masterObj.clusterName
        nodes = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),
                                               Q(containerStatus=1)|Q(containerStatus=2))
        #2.1 如果有主机6071端口不通(说明docker服务挂了),更新此主机上的所有容器状态为停止
        hosts = get_distinct_hosts(nodes)
        conn_res = check_docker_6071(hosts)
        for host in conn_res['err_host']:
            MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(host=host)).update(containerStatus=2)
        #2.2 更新所有正常主机上的容器状态为运行
        for host in hosts-set(conn_res['err_host']):
            MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(host=host)).update(containerStatus=1)
        #2.3 检查运行的容器是否真正运行
        containers = MesosNodeStatus.objects.filter(Q(clusterName=clusterName),Q(containerStatus=1))
        for container in containers:
            host = container.host
            containerName = container.containerName
            if not container_is_running(host, containerName):
                MesosNodeStatus.objects.filter(Q(host=host),Q(containerName=containerName)).update(containerStatus=2)
        #3 检查zookeeper集群状态(从3.5.0开始zookeeper服务中嵌入了jetty server作为adminserver管理服务器，默认端口：8080)
        #4 检查mesos集群状态(master,marathon,slave),通过master 5050 api
        #http://mesos.apache.org/documentation/latest/endpoints/
        #http://192.168.10.3:5050/master/state
        # http://192.168.10.3:5050/metrics/snapshot
        set_status(masterObj, 'master', '/metrics/snapshot')
        set_status(masterObj, 'marathon', '/v2/info')
        set_status(masterObj, 'haproxy', '/api/state')
        set_status(masterObj, 'slave', '/metrics/snapshot')
        statistics_mesos_master_resource(masterObj)
        get_master_leader(masterObj)
        set_master_status(masterObj)
    return True
        
        
        
    
# @shared_task(name='test_celery')
# def test_celery():
#     print 'test_celery'
