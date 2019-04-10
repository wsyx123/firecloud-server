#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年11月4日

@author: yangxu
'''

from sysmgt.models import SysUser,SysRole,Menu_Role_rel,Level2Menu
def get_home_page(userid):
    userobj = SysUser.objects.get(id=userid)
    roleobj = SysRole.objects.get(id=userobj.role_id)
    menu_role_obj = Menu_Role_rel.objects.filter(role=roleobj).order_by('level_1_menu','level_2_menu')[0]
    return Level2Menu.objects.get(id=menu_role_obj.level_2_menu_id).url