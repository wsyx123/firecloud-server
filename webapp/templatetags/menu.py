#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月23日

@author: yangxu
'''
from django import template
from webapp.models import Menu_Role_rel,Level1Menu,Level2Menu,SysRole,HomePage

def get_all_menu():
    '''
    this function is return a list of all level1menu and level2menu
    [
      [Level1MenuObj,[Level2MenuObj1,Level2MenuObj2,...]],
    ]
    '''
    menu_obj_list = []
    Level1MenuObjs = Level1Menu.objects.all()
    for queryobj in Level1MenuObjs:
        Level2MenuObjs = Level2Menu.objects.filter(parent_name_id=queryobj.id).order_by('priority')
        menu_obj_list.append([queryobj,Level2MenuObjs])
    return menu_obj_list
    

register = template.Library()

@register.inclusion_tag('base/_home.html')
def home_page(roleid):
    roleobj = SysRole.objects.get(id=roleid)
    if roleobj.home_page:
        home_page_obj = HomePage.objects.get(id=roleobj.home_page_id)
        return {'home_page_obj':home_page_obj}
    else:
        return {'home_page_obj':None}

@register.inclusion_tag('base/level1menu.html')
def level1menu(roleid):
    '''
    if this user is super role, invoke the get_all_menu to return all menu
    else this template tag is to generate 'level1menu' and level2menu base of role_id,
    first: get all objects from Menu_Role_rel model use role id,
    second: get all level1menu  and level2menu objects then make up a list
    '''
    if roleid == 1:
        menu_obj_list = get_all_menu()
    else:
        lev1_lev2_dict = {}# {1:[1,2,3],2[1,2]}
        '''
                            最终返回给level1menu.html的是 ： [
                                  [Level1MenuObj,[Level2MenuObj1,Level2MenuObj2,...]],
                                ]
        '''
        menu_obj_list = []
        #通过role id 获取一级，二级菜单
        m_r_objs = Menu_Role_rel.objects.filter(role_id = roleid)
        for queryobj in m_r_objs:
            Level1MenuId = queryobj.level_1_menu_id
            Level2MenuId = queryobj.level_2_menu_id
            if lev1_lev2_dict.has_key(Level1MenuId):
                lev1_lev2_dict[Level1MenuId].append(Level2MenuId)
            else:
                lev1_lev2_dict[Level1MenuId] = []
                lev1_lev2_dict[Level1MenuId].append(Level2MenuId)
        for Level1MenuId in lev1_lev2_dict.keys():
            
            temp1_list = []
            temp2_list = []
            Level1MenuObj = Level1Menu.objects.get(id=Level1MenuId)
            temp1_list.append(Level1MenuObj)
            if Level1MenuId == 1:
                temp2_list = []
            else:
                for Level2MenuId in lev1_lev2_dict[Level1MenuId]:
                    Level2MenuObj = Level2Menu.objects.get(id=Level2MenuId)
                    temp2_list.append(Level2MenuObj)
            temp1_list.append(temp2_list)
            menu_obj_list.append(temp1_list)
    return {'menu_obj_list':menu_obj_list}

@register.inclusion_tag('base/level2menu.html')
def level2menu(menu2_obj_list):
    return {'menu2_obj_list':menu2_obj_list}

@register.inclusion_tag('sys_manage/_ListMenuTable.html')
def menu_perm_list():
    menu_obj_list = get_all_menu()
    return {'menu_obj_list':menu_obj_list}

@register.inclusion_tag('sys_manage/_UpdateMenuTable.html')
def menu_perm_update(permobj):
    menu_obj_list = get_all_menu()
    for rel_queryset in permobj:
        for querylist in menu_obj_list:
            for level2_queryset in querylist[1]:
                if rel_queryset.level_2_menu_id == level2_queryset.id:
                    level2_queryset.view = rel_queryset.view
                    level2_queryset.create = rel_queryset.create
                    level2_queryset.update = rel_queryset.update
                    level2_queryset.delete = rel_queryset.delete
    return {'menu_obj_list':menu_obj_list}

@register.inclusion_tag('application/_opt.html')
def optapp(roleid):
    return {'roleid':roleid}

# control the add,delete button whether display
@register.inclusion_tag('base/_addbutton.html')
def ctl_button(roleid,path):
    if roleid == 1:
        return {'display':True}
    else:
        roleobj = SysRole.objects.get(id=roleid)
        level2obj = Level2Menu.objects.get(url=path)
        optobj = Menu_Role_rel.objects.get(role=roleobj,level_2_menu=level2obj)
        if optobj.create == 1:
            return {'display':True}
    return {'display':False}
