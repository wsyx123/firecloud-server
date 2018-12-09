#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from ansible.plugins.callback import CallbackBase 
from datetime import datetime       

class CollectAssetInfoCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self._result = {'status':None,'result':None}
        super(CollectAssetInfoCallback,self).__init__(display=None)
    
    def get_public_ip(self,private_ip,interfaces,host_info):
        for eth in interfaces:
            if eth != 'lo' and host_info['ansible_'+eth] != private_ip:
                return host_info['ansible_'+eth]['ipv4']['address']
        
    def sum_disk(self,mounts,uuids,swap):
        '''not include swap size,so less than acture size'''
        disk_size = swap*1024*1024
        uuid_list = []
        for key,value in uuids.items():
            uuid_list.append(value[0])
        for mount in mounts:
            if mount['uuid'] in uuid_list:
                disk_size = disk_size + mount['size_total']
        return disk_size/1000/1000/1024
        
    def v2_runner_on_ok(self, result, **kwargs):
        self._result['status'] = 'ok'
        host_info = result._result['ansible_facts']
        #address
        private_ip = result._host.get_name()
        results = {'private_ip':private_ip}
        #主机名
        hostname = host_info['ansible_hostname']
        results['hostname'] = hostname
        #操作系统  CentOS
        distribution_name = host_info['ansible_distribution']
        # 操作系统版本  7.5.1804
        distribution_version = host_info['ansible_distribution_version']
        results['os'] = distribution_name+' '+distribution_version
        #产品序列号
        product_serial = host_info['ansible_product_serial']
        results['serial'] = product_serial
        #所有磁盘分区ID
        devices_id = host_info['ansible_device_links']['uuids']
        #所有挂载点  结合devices_id 可以统计出机器上所有磁盘总大小
        mounts = host_info['ansible_mounts']
        swap = host_info['ansible_swaptotal_mb']
        results['disk'] = self.sum_disk(mounts, devices_id, swap)
        #服务器型号
        product_name = host_info['ansible_product_name']
        results['machine_model'] = product_name
        #服务器供应商
        system_vendor = host_info['ansible_system_vendor']
        #内核
        kernel = host_info['ansible_kernel']
        results['kernel'] = kernel
        #CPU 核数
        cpu_num = host_info['ansible_processor_count']
        results['cpu_no'] = cpu_num
        #CPU 型号
        cpu_model = host_info['ansible_processor'][2]
        results['cpu_model'] = cpu_model
#         vcpu_num = host_info['ansible_processor_vcpus']
        memory_total = host_info['ansible_memtotal_mb']
        results['memory'] = memory_total
#         memory_info = host_info['ansible_memory_mb']
#         uptime = host_info['ansible_uptime_seconds']
        
        interfaces = host_info['ansible_interfaces']
        results['public_ip'] = self.get_public_ip(private_ip, interfaces, host_info)
        self._result['result'] = results
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        private_ip = result._host.get_name()
        self._result['result'] = {'private_ip':private_ip}
        self._result['result']['msg'] = result._result['msg']
        
    def v2_runner_on_unreachable(self, result):
        private_ip = result._host.get_name()
        self._result['status'] = 'unreachable'
        self._result['result'] = {'private_ip':private_ip}
        self._result['result']['msg'] = result._result['msg']
        

class ScriptExecuteCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self._result = {'ok':[],'failed':[]}
        super(ScriptExecuteCallback,self).__init__(display=None)

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        start_time = result._result['start']
        data = result._result['stdout']
        self._result['ok'].append({'host':host,
                                   'start_time':start_time,
                                   'data':data,
                                   'status':'ok'})
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        start_time = result._result['start']
        data = result._result['stderr']
        self._result['failed'].append({'host':host,
                                       'start_time':start_time,
                                       'data':data,
                                       'status':'failed'})
        
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
        data = result._result['msg']
        self._result['failed'].append({'host':host,
                                       'start_time':start_time,
                                       'data':data,
                                       'status':'failed'})
        
class FileCopyCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self._result = {'ok':[],'failed':[]}
        super(FileCopyCallback,self).__init__(display=None)

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        self._result['ok'].append(host)
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
        data = result._result['msg']
        self._result['failed'].append({'host':host,
                                       'start_time':start_time,
                                       'data':data,
                                       'status':'failed'})
        
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
        data = result._result['msg']
        self._result['failed'].append({'host':host,
                                       'start_time':start_time,
                                       'data':data,
                                       'status':'failed'})