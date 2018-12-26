#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.errors import AnsibleParserError

class myplaybook():
    #这里是ansible运行 
    #初始化各项参数，大部分都定义好，只有几个参数是必须要传入的
    def __init__(self, playbook,hosts,result_callback,task_id,extra_vars={}, 
                        connection='ssh',
                        become=False,
                        become_user=None,
                        module_path=None,
                        fork=50,
                        ansible_cfg=None,   #os.environ["ANSIBLE_CONFIG"] = None
                        passwords={},
                        check=False,
                        diff=False):
        self.playbook_path=playbook
        self.passwords=passwords
        self.extra_vars=extra_vars
        self.hosts = hosts
        self.result_callback = result_callback(task_id=task_id)
        Options = namedtuple('Options',
                   ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path',
                   'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                      'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check','diff'])
        self.options = Options(listtags=False, listtasks=False, 
                              listhosts=False, syntax=False, 
                              connection=connection, module_path=module_path, 
                              forks=fork, private_key_file=None, 
                              ssh_common_args=None, ssh_extra_args='-o StrictHostKeyChecking=no', 
                              sftp_extra_args=None, scp_extra_args=None, 
                              become=become, become_method=None, 
                              become_user=become_user, 
                              verbosity=None, check=check,diff=diff)
        if ansible_cfg != None:
            os.environ["ANSIBLE_CONFIG"] = ansible_cfg
        self.loader=DataLoader()
        self.inventory=InventoryManager(loader=self.loader,sources=[self.hosts])
        self.variable_manager=VariableManager(loader=self.loader, inventory=self.inventory)
    #定义运行的方法和返回值
    def run(self):
        pbex= PlaybookExecutor(playbooks=[self.playbook_path],
                       inventory=self.inventory,
                       variable_manager=self.variable_manager,
                       loader=self.loader,
                       options=self.options,
                       passwords=self.passwords)
        pbex._tqm._stdout_callback = self.result_callback
        try:
            execute_host_count=pbex.run()
            return execute_host_count
        except Exception as e:
            return str(e)
            
    def get_result(self):
        return self.result_callback._result
        
