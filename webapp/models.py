# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# import system management model 
from model.sys_mgt import SysRole,SysUser,Level1Menu,\
Level2Menu,Menu_Role_rel,HomePage,AppOpt_Role_rel

# import asset model
from model.asset import AssetHost,HostEvent,HostImport,HostAccount,HostGroup,Enterprise

# import tasks model
from model.task import ScriptModel,TaskLog,TaskHost,AnsibleModel,AnsibleLog,AnsibleHost,\
FileModel,FileLog,FileHost,FileModelExistList,FileModelForHad,FileModelForUrl,PublicFile

# import paas model
from model.paas import RepositoryHost,RepositoryImage,PaasHost,MesosCluster,MesosMaster,\
MesosDeployLog

# Create your models here.
'''
auto_now:这个参数的默认值为false，设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改model，都会自动更新
auto_now_add:这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
'''


    
    