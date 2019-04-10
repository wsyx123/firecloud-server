#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.conf.urls import url
from views import Enterprise,AddDepartment,Employee,AddEmployee,Project,AddProject

urlpatterns = [
    url(r'^enterprise/list/$', Enterprise.as_view(),name='enterprise'),
    url(r'^enterprise/addDepartment/$', AddDepartment.as_view(),name='addDepartment'),
    url(r'^project/list/$', Project.as_view(),name='project'),
    url(r'^project/add/$', AddProject.as_view(),name='addProject'),
    url(r'^employee/list/$', Employee.as_view(),name='employee'),
    url(r'^employee/add/$', AddEmployee.as_view(),name='addEmployee'),
    ]