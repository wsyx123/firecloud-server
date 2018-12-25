#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import json
import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleParserError
import logging

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
#                     datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='dockerinstall.log',  
                    filemode='a')

class myplaybook():
    #这里是ansible运行 
    #初始化各项参数，大部分都定义好，只有几个参数是必须要传入的
    def __init__(self, playbook, extra_vars={}, 
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
        self.inventory=InventoryManager(loader=self.loader,sources=['hosts'])
        self.variable_manager=VariableManager(loader=self.loader, inventory=self.inventory)
    #定义运行的方法和返回值
    def run(self):
        self.complex_msg={'success':{},'failed':{},'unreachable':{},'notmatched':{},'started':{},'error':{}}
        if not os.path.exists(self.playbook_path):
            logging.error({'playbook':self.playbook_path,'msg':self.playbook_path+' playbook is not exist','flag':False})
            #results=self.playbook_path+'playbook is not existed'
            #return code,complex_msg,results
        pbex= PlaybookExecutor(playbooks=[self.playbook_path],
                       inventory=self.inventory,
                       variable_manager=self.variable_manager,
                       loader=self.loader,
                       options=self.options,
                       passwords=self.passwords)
        try:
            code=pbex.run()
        except AnsibleParserError:
            logging.error({'playbook':self.playbook_path,'msg':self.playbook_path+' playbook have syntax error','flag':False})
            #results='syntax error in '+self.playbook_path #语法错误
            

        
