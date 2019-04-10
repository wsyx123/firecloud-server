#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import OptList,OptAudit,OptDelete
from views import ScriptList,ScriptAdd,ScriptDelete,get_script_content,\
ScriptUpdate,ScriptExecute,ScriptExecuteResult,script_copy
from views import AnsibleList,AnsibleAdd,ansible_upload_file,ansible_save,AnsibleUpdate,\
del_upload_file,AnsibleDelete,ansible_copy,AnsibleExecute,get_playbook_result
from views import FileList,FileDistributeAdd,FileDistributeUpdate,\
file_distribute_upload,file_distribute_delete,\
file_distribute_save,file_task_name_validate,\
get_file_distribute_result,file_distribute_send,FileDistributeResult,FileDistributeDelete
from views import PublicFileList,PublicFileUpload,public_file_delete
from fast_tool import FastToolList

urlpatterns = [
    url(r'^optlog/list/$',OptList.as_view(),name='OptList'),
    url(r'^optlog/delete/$',OptDelete,name='OptDelete'),
    url(r'^optlog/audit/(?P<pk>.+)$',OptAudit.as_view(),name='OptAudit'),
    url(r'^script/list/$',ScriptList.as_view(),name='ScriptList'),
    url(r'^script/add/$',ScriptAdd.as_view(),name='ScriptAdd'),
    url(r'^script/add/copy/$',script_copy),
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
    url(r'^ansible/execute/$',AnsibleExecute.as_view()),
    url(r'^ansible/execute/result/$',get_playbook_result),
    url(r'^file/list/$',FileList.as_view(),name='FileList'),
    url(r'^file/add/$',FileDistributeAdd.as_view(),name='FileAdd'),
    url(r'^file/update/(?P<pk>.+)$',FileDistributeUpdate.as_view(),name='FileUpdate'),
    url(r'^file/add/upload/$',file_distribute_upload),
    url(r'^file/add/delete/$',file_distribute_delete),
    url(r'^file/add/validate/$',file_task_name_validate),
    url(r'^file/add/save/$',file_distribute_save),
    url(r'^file/add/send/$',file_distribute_send),
    url(r'^file/add/result/$',get_file_distribute_result),
    url(r'^file/execute/result/$',FileDistributeResult.as_view()),
    url(r'^file/delete/(?P<pk>.+)$',FileDistributeDelete.as_view()),
    url(r'^publicFile/list/$',PublicFileList.as_view(),name='publicFileList'),
    url(r'^publicFile/upload/$',PublicFileUpload.as_view(),name='publicFileUpload'),
    url(r'^publicFile/delete/$',public_file_delete),
    url(r'fastTool/list/$',FastToolList.as_view(),name='fastToolList')
    ]