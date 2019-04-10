#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月24日

@author: yangxu
'''
from django.views.generic import ListView,FormView,UpdateView,DeleteView
from models import SysUser,SysRole,Menu_Role_rel,Level1Menu,Level2Menu
from forms import SysUserForm,SysRoleForm
from django.urls import reverse_lazy
import json


class UserMgt(ListView):
    model = SysUser
    context_object_name = 'user_list'
    template_name = 'sys_manage/UserMgt.html'
    
class UserAdd(FormView):
    template_name = 'sys_manage/UserAdd.html'
    form_class = SysUserForm
    success_url = reverse_lazy('UserMgt')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class UserUpdate(UpdateView):
    model = SysUser
    form_class = SysUserForm
    pk_url_kwarg = 'pk' #指明url 的key 为pk
    success_url = reverse_lazy('UserMgt')
    template_name = 'sys_manage/UserUpdate.html'
    
    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        obj = SysUser.objects.get(id=self.kwargs[self.pk_url_kwarg])
        self.object = form.save()
        self.object.last_login = obj.last_login
        return super(UserUpdate, self).form_valid(form)
   

class UserDelete(DeleteView):
    model = SysUser
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('UserMgt')
    template_name = 'sys_manage/UserDeleteConfirm.html'
    
class RoleMgt(ListView):
    model = SysRole
    context_object_name = 'role_list'
    template_name = 'sys_manage/RoleMgt.html'
    
class RoleAdd(FormView):
    template_name = 'sys_manage/RoleAdd.html'
    form_class = SysRoleForm
    success_url = reverse_lazy('RoleMgt')
    '''接收数据格式为
    {'role_id':[
                {'level1_id':1,'level2_id':2,'view':1,'create':1,'update':1,'delete':1},
                ]
    }
    '''
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        menu_list = str2json2list(str(request.POST["menu"]).strip("[").strip("]").split("},"))
        if form.is_valid():
            obj = form.save()
            patch_save(Menu_Role_rel, menu_list, obj)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class RoleUpdate(UpdateView):
    model = SysRole
    form_class = SysRoleForm
    pk_url_kwarg = 'pk' #指明url 的key 为pk
    success_url = reverse_lazy('RoleMgt')
    template_name = 'sys_manage/RoleUpdate.html'
    def get_context_data(self, **kwargs):
        roleid =self.kwargs[self.pk_url_kwarg]
        permobj = Menu_Role_rel.objects.filter(role_id=roleid)
        kwargs['permobj'] = permobj
        return UpdateView.get_context_data(self, **kwargs)
    
    def post(self, request, *args, **kwargs):
        menu_list = str2json2list(str(request.POST["menu"]).strip("[").strip("]").split("},"))
        obj = SysRole.objects.get(id=kwargs[self.pk_url_kwarg])
        patch_update(Menu_Role_rel, menu_list, obj)
        return UpdateView.post(self, request, *args, **kwargs)

class RoleDelete(DeleteView):
    model = SysRole
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('RoleMgt')
    

def str2json2list(menulist):
    all_list = []
    last_item = menulist.pop()
    for item in menulist:
        all_list.append(json.loads(item+"}"))
    all_list.append(json.loads(last_item))
    return all_list

def patch_save(mod,data,roleobj):
    obj_list = []
    for item in data:
        if item['view'] ==1 or item['create'] == 1 or item['update'] == 1 or item['delete'] == 1:
            level1obj = Level1Menu.objects.get(id=int(item['level1id']))
            if item['level2id']:
                level2obj = Level2Menu.objects.get(id=int(item['level2id']))
            else:
                level2obj = None
            obj = mod(role=roleobj,level_1_menu=level1obj,level_2_menu=level2obj,
                      view=item['view'],create=item['create'],update=item['update'],delete=item['delete'])
            obj_list.append(obj)
    mod.objects.bulk_create(obj_list)
    
def patch_update(mod,data,roleobj):
    obj_list = []
    mod.objects.filter(role=roleobj).delete()
    for item in data:
        if item['view'] ==1 or item['create'] == 1 or item['update'] == 1 or item['delete'] == 1:
            level1obj = Level1Menu.objects.get(id=int(item['level1id']))
            if item['level2id']:
                level2obj = Level2Menu.objects.get(id=int(item['level2id']))
            else:
                level2obj = None
            obj = mod(role=roleobj,level_1_menu=level1obj,level_2_menu=level2obj,
                      view=item['view'],create=item['create'],update=item['update'],delete=item['delete'])
            obj_list.append(obj)
    mod.objects.bulk_create(obj_list)
    