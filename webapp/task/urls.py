#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from task import OptList,OptAudit,OptDelete
from task import ScriptList,ScriptAdd,ScriptDelete,FileSend,get_script_content,\
ScriptUpdate,ScriptExecute,ScriptExecuteResult
from task import AnsibleList,AnsibleExecute,AnsibleAdd,ansible_upload_file,ansible_save,AnsibleUpdate,\
del_upload_file,AnsibleDelete,ansible_copy

urlpatterns = [
    url(r'^optlog/list/$',OptList.as_view(),name='OptList'),
    url(r'^optlog/delete/$',OptDelete,name='OptDelete'),
    url(r'^optlog/audit/(?P<pk>.+)$',OptAudit.as_view(),name='OptAudit'),
    url(r'^script/list/$',ScriptList.as_view(),name='ScriptList'),
    url(r'^script/add/$',ScriptAdd.as_view(),name='ScriptAdd'),
    url(r'^script/execute/result/$',ScriptExecuteResult.as_view(),name='ScriptExecuteResult'),
    url(r'^script/execute/$',ScriptExecute,name='ScriptExecute'),
    url(r'^script/add/content/$',get_script_content),
    url(r'^script/update/(?P<pk>.+)$',ScriptUpdate.as_view(),name='ScriptUpdate'),
    url(r'^script/delete/(?P<pk>.+)$',ScriptDelete.as_view(),name='ScriptDelete'),
    url(r'^ansible/list/$',AnsibleList.as_view(),name='AnsibleList'),
    url(r'^ansible/add/$',AnsibleAdd.as_view(),name='AnsibleAdd'),
    url(r'^ansible/add/save/$',ansible_save),
    url(r'^ansible/add/copy/$',ansible_copy),
    url(r'^ansible/add/file/$',ansible_upload_file),
    url(r'^ansible/delete/file/$',del_upload_file),
    url(r'^ansible/update/(?P<pk>.+)$',AnsibleUpdate.as_view(),name='AnsibleUpdate'),
    url(r'^ansible/delete/(?P<pk>.+)$',AnsibleDelete.as_view(),name='AnsibleDelete'),
    url(r'^ansible/execute/$',AnsibleExecute.as_view(),name='AnsibleExecute'),
    url(r'^file/$',FileSend.as_view(),name='file'),
    ]