#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年7月28日

@author: yangxu
'''
from django.views.generic import TemplateView
class Enterprise(TemplateView):
    template_name = 'asset/enterprise/enterprise.html'
   
    
class AddDepartment(TemplateView):
    template_name = 'asset/enterprise/addDepartment.html'
    
class Employee(TemplateView):
    template_name = 'asset/enterprise/Employee.html'
    def get_context_data(self, **kwargs):
        context = super(Employee, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['employees'] = [{'number':'101','name':'David','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'UI设计师','email':'david@firecloud.com'},
                                {'number':'102','name':'Jack','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'高级JAVA工程师','email':'jack@firecloud.com'},
                                {'number':'103','name':'Tom','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'云计算架构师','email':'tom@firecloud.com'},
                            ]
        return context

class AddEmployee(TemplateView):
    template_name = 'asset/enterprise/addEmployee.html'
    

class Project(TemplateView):
    template_name = 'asset/enterprise/Project.html'
    def get_context_data(self, **kwargs):
        context = super(Project, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['projects'] = [{'id':'20180805011','name':'IAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'需求分析','current_status':'需求分析'},
                               {'id':'20180805012','name':'PAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'概要设计','current_status':'概要设计'},
                               {'id':'20180805013','name':'SAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'技术选型','current_status':'技术选型'},
                            ]
        return context
    
class AddProject(TemplateView):
    template_name = 'asset/enterprise/addProject.html'
