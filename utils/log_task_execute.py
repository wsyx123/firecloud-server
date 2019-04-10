#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018��12��05��

@author: yangxu
记录脚本执行
'''
from taskcenter.models import TaskLog,TaskHost

def log_task_execute(execute_result,host_account_var,task_type,script_file,owner_id):
    task_log_dict = {}
    task_log_dict['task_id'] = execute_result['task_id']
    task_log_dict['task_name'] = execute_result['task_name']
    task_log_dict['task_type'] = task_type
    task_log_dict['host_no'] = len(execute_result['failed'])+len(execute_result['ok'])
    task_log_dict['finish_no'] = len(execute_result['ok'])
    task_log_dict['failure_no'] = len(execute_result['failed'])
    task_log_dict['execute_owner_id'] = owner_id
    task_log_dict['script_file'] = script_file
    TaskLog.objects.create(**task_log_dict)
    
    def get_host_list(ok_list):
        host_list = []
        for host in ok_list:
            host_list.append(host['host'])
        return host_list
        
    
    task_host_dict = {}
    for item in host_account_var:
        for key,val in item.items():
            if key in get_host_list(execute_result['ok']):
                status = 1
            else:
                status = 2
            task_host_dict['task_id'] = execute_result['task_id']
            task_host_dict['host_ip'] = key
            task_host_dict['host_account'] = val['ansible_ssh_user']
            task_host_dict['execute_status'] = status
        TaskHost.objects.create(**task_host_dict)