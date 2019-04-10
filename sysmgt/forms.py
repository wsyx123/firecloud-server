#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月29日

@author: yangxu
'''
from django import forms
from models import SysUser,SysRole

class SysUserForm(forms.ModelForm):
    class Meta:
        model = SysUser
        fields = "__all__"
        widgets = {'username': forms.TextInput(attrs={'class': 'width-100'}),
                   'password': forms.TextInput(attrs={'class':'width-100'}),
                   'description': forms.TextInput(attrs={'class': 'width-100'}),
                   'tel': forms.TextInput(attrs={'class': 'width-100'}),
                   'email': forms.EmailInput(attrs={'class': 'width-100'}),
                   'status': forms.Select(attrs={'class':'form-control'}),
                   'role': forms.Select(attrs={'class':'form-control'})
                   }
class SysRoleForm(forms.ModelForm):
    class Meta:
        model = SysRole
        fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class':'form-control'}),
                   'home_page': forms.Select(attrs={'class':'form-control'}),
                   'description': forms.TextInput(attrs={'class':'form-control'}),
                   }
        