#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from ansible.plugins.callback import CallbackBase 
from datetime import datetime
from webapp.models import AnsibleHost,FileHost

class CollectAssetInfoCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self._result = {'status':None,'result':None}
        super(CollectAssetInfoCallback,self).__init__(display=None)
    
    def get_size(self,size):
        if len(str(size)) > 9:
            return str(int(float(size)/1024/1000/1000))+'G'
        else:
            return str(int(float(size)/1024/1000))+'M'
    
    def get_ansible_mounts(self,ansible_facts):
        ansible_mounts = ansible_facts['ansible_mounts']
        mount_list = []
        for mount in ansible_mounts:
            mount_dict = {}
            size_total = mount['size_total']
            size_available = mount['size_available']
            size_used = size_total - size_available
            percent = round(float(size_used)/size_total,2)*100
            
            mount_dict['name'] = mount['device']
            mount_dict['size'] = self.get_size(size_total)
            mount_dict['used'] = self.get_size(size_used)
            mount_dict['available'] = self.get_size(size_available)
            mount_dict['percent'] = percent
            mount_dict['mount'] = mount['mount']
            mount_list.append(mount_dict)
        return mount_list
    
    def get_ansible_ethernet(self,ansible_facts):
        ansible_interfaces = ansible_facts['ansible_interfaces']
        eth_list = []
        for eth in ansible_interfaces:
            eth_dict = {}
            eth_dict['name'] = eth
            eth_dict['ip'] = ansible_facts['ansible_'+eth]['ipv4']['address']
            eth_dict['netmask'] = ansible_facts['ansible_'+eth]['ipv4']['netmask']
            if ansible_facts['ansible_'+eth].has_key('macaddress'):
                eth_dict['mac'] = ansible_facts['ansible_'+eth]['macaddress']
            else:
                eth_dict['mac'] = None
            if ansible_facts['ansible_'+eth].has_key('speed'):
                eth_dict['speed'] = ansible_facts['ansible_'+eth]['speed']
            else:
                eth_dict['speed'] = None
            eth_dict['status'] = ansible_facts['ansible_'+eth]['active']
            eth_list.append(eth_dict)
        return eth_list
        
    
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
        results['vendor'] = system_vendor
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
        results['eth_list'] = self.get_ansible_ethernet(host_info)
        results['mounts'] = self.get_ansible_mounts(host_info)
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

class PlaybookExecuteCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self.task_id=kwargs['task_id']
        super(PlaybookExecuteCallback,self).__init__(display=None)

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        step = str(result._task).split(':')[1].strip()
        task = result.task_name
        AnsibleHost.objects.create(task_id=self.task_id,step=step,task=task,host=host,status=True)
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        step = str(result._task).split(':')[1].strip()
        task = result.task_name
        msg = result._result['msg']
        AnsibleHost.objects.create(task_id=self.task_id,step=step,task=task,host=host,status=False,msg=msg)
        
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        step = str(result._task).split(':')[1].strip()
        task = result.task_name
        msg = result._result['msg']
        AnsibleHost.objects.create(task_id=self.task_id,step=step,task=task,host=host,status=False,msg=msg)

class FileDistributeCallback(CallbackBase):
    def __init__(self,*args,**kwargs):
        self.task_id=kwargs['task_id']
        super(FileDistributeCallback,self).__init__(display=None)

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        task = result.task_name
        FileHost.objects.create(task_id=self.task_id,task=task,host=host,status=True)
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result.task_name
        msg = result._result['msg']
        FileHost.objects.create(task_id=self.task_id,task=task,host=host,status=False,msg=msg)
        
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        task = result.task_name
        msg = result._result['msg']
        FileHost.objects.create(task_id=self.task_id,task=task,host=host,status=False,msg=msg)