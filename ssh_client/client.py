#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月26日

@author: yangxu
'''
from paramiko import SSHClient,AutoAddPolicy
from interactive import interactive_shell


def connect(request):
    sshclient=SSHClient()
    sshclient.load_system_host_keys()
    sshclient.set_missing_host_key_policy(AutoAddPolicy())
    try:
        sshclient.connect('192.168.10.4',22,'root','password')
    except Exception as e:
        print e
    else:
        chan=sshclient.invoke_shell()
        interactive_shell(chan,request)
    

#################################################################
# 
# while True:
#     data=chan.recv(512)
#     if not data:
#         break
#     print(data)


