#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月23日

@author: yangxu
'''
from __future__ import absolute_import
from celery import task

from webapp.models import HostImport,AssetHost,HostEvent
from utils.ansibleAdHoc import myadhoc
from utils.ansibleplaybook import myplaybook
from utils.callback import CollectAssetInfoCallback
from utils.mesos_deploy import MesosDeploy
import xlrd
from django.core.validators import validate_ipv4_address
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
import time

@task(name='test_celery')
def test_celery():
    print 'test_celery'

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
    
       

@task(name='process_asset_import')
def process_asset_import(import_id,full_filename):
    datalist = get_assets_data(full_filename)
    asset_format_check(import_id,datalist)
        
        
@task(name='collect_host_info')
def collect_host_info(asset_id,private_ip,port,user,password,action_num):
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

#to initialize mesos cluster deploy log table
def init_deploy_log_table(celery_id,cluster_name,deploy_model):
    deploy_model.objects.filter(cluster_name=cluster_name).delete()
    step_name_list = ["checkCon","imgDownload",
                      "deployZK","deployMaster",
                      "deployMT","deployHA","deploySlave"]
    MesosDeployLogList = []
    for step_name in step_name_list:
        deployLog = deploy_model(celery_id=celery_id,cluster_name=cluster_name,step_name=step_name)
        MesosDeployLogList.append(deployLog)
    deploy_model.objects.bulk_create(MesosDeployLogList)

@task(name='mesos_cluster_deploy_task',bind=True)
def mesos_cluster_deploy_task(self,clsObj,deploy_model,detail_model):
    celery_id = self.request.id
    clusterName = clsObj.clusterName
    #to insert into MesosDeployLog
    init_deploy_log_table(celery_id, clusterName, deploy_model)
    #Check the host connectivity
    deploy_obj = deploy_model.objects.get(Q(cluster_name=clusterName),Q(step_name='checkCon'))
    deploy_obj.status = 2
    deploy_obj.save()
    deploy_cls_instance = MesosDeploy(clsObj,deploy_model)
    check_con_result = deploy_cls_instance.check_con(deploy_obj)
    if not check_con_result:
        clsObj.status = 3
        clsObj.save()
        return 'failed'
        
    #download docker image
    deploy_obj = deploy_model.objects.get(Q(cluster_name=clusterName),Q(step_name='imgDownload'))
    deploy_obj.status = 2
    deploy_obj.save()
    img_download_result = deploy_cls_instance.img_download(deploy_obj)
    if not img_download_result:
        clsObj.status = 3
        clsObj.save()
        return 'failed'
    #create container
    step_name_list = ["deployZK","deployMaster","deployMT","deployHA","deploySlave"]
    for step_name in step_name_list:
        deploy_obj = deploy_model.objects.get(Q(cluster_name=clusterName),Q(step_name=step_name))
        deploy_obj.status = 2
        deploy_obj.save()
        create_container_result = deploy_cls_instance.create_container(deploy_obj,step_name,detail_model)
        if not create_container_result:
            clsObj.status = 3
            clsObj.save()
            return 'failed'
    clsObj.status = 4
    clsObj.save()
    return True
    
    
# @shared_task(name='test_celery')
# def test_celery():
#     print 'test_celery'
