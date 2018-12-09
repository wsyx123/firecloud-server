#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from asset import HostList,HostAdd,HostUpdate,HostDelete,host_import,HostDetail,\
                  get_import_result,host_refresh
from asset import AccountList
from asset import GroupList,GroupAdd,GroupUpdate,GroupDelete
from asset import Enterprise,AddDepartment,Employee,AddEmployee,Project,AddProject,asset_connect

urlpatterns = [
    url(r'^host/list/$', HostList.as_view(),name='HostList'),
    url(r'^host/add/$', HostAdd.as_view(),name='HostAdd'),
    url(r'^host/ssh/$',asset_connect,name='HostLogin'),
    url(r'^host/import/result/$', get_import_result),
    url(r'^host/import/$', host_import,name='HostImport'),
    url(r'^host/update/(?P<pk>.+)$', HostUpdate.as_view(),name='HostUpdate'),
    url(r'^host/refresh/$', host_refresh,name='HostRefresh'),
    url(r'^host/delete/(?P<pk>.+)$', HostDelete.as_view(),name='HostDelete'),
    url(r'^host/detail/(?P<pk>.+)$', HostDetail.as_view(),name='HostDetail'),
    url(r'^account/list/$', AccountList.as_view(),name='AccountList'),
    url(r'^group/list/$', GroupList.as_view(),name='GroupList'),
    url(r'^group/add/$', GroupAdd.as_view(),name='GroupAdd'),
    url(r'^group/update/(?P<pk>.+)$', GroupUpdate.as_view(),name='GroupUpdate'),
    url(r'^group/delete/(?P<pk>.+)$', GroupDelete.as_view(),name='GroupDelete'),
    url(r'^enterprise/list/$', Enterprise.as_view(),name='enterprise'),
    url(r'^enterprise/addDepartment/$', AddDepartment.as_view(),name='addDepartment'),
    url(r'^project/list/$', Project.as_view(),name='project'),
    url(r'^project/add/$', AddProject.as_view(),name='addProject'),
    url(r'^employee/list/$', Employee.as_view(),name='employee'),
    url(r'^employee/add/$', AddEmployee.as_view(),name='addEmployee'),
    ]