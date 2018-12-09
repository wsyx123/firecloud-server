#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

class HostVar():
    def get_name(self):
        return '192.168.10.3'

class myadhoc():
    def __init__(self,tasks,group,host,port,user,password,callback,hostVar=None):
        self.tasks = tasks
        self.group = group
        self.host = host
        self.user = user
        self.password = password
        self.results_callback = callback()
        self.hostVar = hostVar
    
    def get_result(self):
        return self.results_callback._result
    
    def run(self):
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 
                                         'become_method', 'become_user', 'check', 'diff',
                                         'ssh_extra_args','remote_user'])
        # initialize needed objects
        loader = DataLoader()
        options = Options(connection='ssh', module_path='', forks=100, become=None, 
                          become_method=None, become_user=None, check=False, diff=False,
                          ssh_extra_args='-o StrictHostKeyChecking=no', remote_user=self.user)
        passwords = dict(conn_pass=self.password)
#         passwords = dict(vault_pass='secret')
        
        
        # create inventory and pass to var manager
        inventory = InventoryManager(loader=loader, sources=[self.host])
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        #方法一   设置主机变量，其实set_host_variable 操作的是_vars_cache  类型defaultdict
        #host = HostVar() 
        #variable_manager.set_host_variable(host, 'ansible_ssh_user', 'clouder')
        #方法二   设置主机变量, 直接操作_vars_cache
        for host in self.hostVar:
            for key,val in host.items():
                variable_manager._vars_cache[key]=val
        
        # create play with tasks
        
        play_source =  dict(
                name = "Ansible Play",
                hosts = self.group,
                gather_facts = 'no',
                tasks = self.tasks,
            )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        
        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=passwords,
                      stdout_callback=self.results_callback,
                  )
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()


