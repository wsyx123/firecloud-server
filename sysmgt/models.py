#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:57:56
@author: yangxu
'''
from __future__ import unicode_literals
from django.db import models

class SysRole(models.Model):
    name = models.CharField(max_length=16,unique=True,verbose_name='角色名')
    description = models.CharField(max_length=64,verbose_name='描述')
    home_page = models.ForeignKey('HomePage',blank=True, null=True,)
    def users(self):
        return SysUser.objects.filter(role_id=self.id)
    
    def __unicode__(self):
        return '%s' %(self.description)

class SysUser(models.Model):
    user_status = (
                   (1,'启用'),
                   (2,'禁用')
                   )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20,blank=False)
    description = models.CharField(max_length=64,null=True,blank=True)
    role = models.ForeignKey(SysRole,null=True,blank=True)
    tel = models.CharField(max_length=11)
    email = models.EmailField()
    status = models.IntegerField(choices=user_status,default=2,verbose_name='状态')
    last_login = models.DateTimeField(blank=True, null=True,verbose_name='最近登录')
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def role_id(self):
        return self.role.id
    def __unicode__(self):
        return '%s' %(self.username)


    
class Level1Menu(models.Model):
    name = models.CharField(max_length=16,verbose_name='一级菜单名称')
    description = models.CharField(max_length=32,verbose_name='中文描述')
    priority = models.IntegerField(verbose_name='菜单优先级')
    url = models.CharField(max_length=64,verbose_name='菜单url')
    menu_icon = models.CharField(max_length=32,verbose_name='菜单图标')
    
    def __unicode__(self):
        return '%s' %(self.name)

class Level2Menu(models.Model):
    parent_name = models.ForeignKey(Level1Menu,verbose_name='一级菜单名称')
    name = models.CharField(max_length=16,verbose_name='二级菜单名称')
    description = models.CharField(max_length=32,verbose_name='中文描述')
    priority = models.IntegerField(verbose_name='菜单优先级')
    url = models.CharField(max_length=64,verbose_name='菜单url')
    view = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.name)
    
class Menu_Role_rel(models.Model):
    role = models.ForeignKey(SysRole)
    level_1_menu = models.ForeignKey(Level1Menu)
    level_2_menu = models.ForeignKey(Level2Menu,null=True,blank=True)
    view = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.level_2_menu)
    
class HomePage(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    template_name = models.CharField(max_length=64)
    def __unicode__(self):
        return '%s' %(self.name)
    
class AppOpt_Role_rel(models.Model):
    role = models.ForeignKey(SysRole)
    publish = models.BooleanField(default=False)
    stop = models.BooleanField(default=False)
    start = models.BooleanField(default=False)
    reboot = models.BooleanField(default=False)
    scale = models.BooleanField(default=False)
    undeploy = models.BooleanField(default=False)
    connect = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.role)
    
class WhiteList(models.Model):
    url = models.CharField(max_length=32,unique=True)
    comment = models.CharField(max_length=32)
    enabled = models.BooleanField(default=False)