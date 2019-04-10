#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月19日

@author: yangxu
'''
from django import forms
from models import AssetHost,HostGroup

class AssetHostForm(forms.ModelForm):
    class Meta:
        model = AssetHost
        fields = "__all__"
        widgets = {'private_ip': forms.TextInput(attrs={'class': 'width-100'}),#1L
                   'port': forms.NumberInput(attrs={'class': 'width-100'}),
                   'host_status': forms.Select(attrs={'class':'form-control'}),
                   'remote_user': forms.TextInput(attrs={'class': 'width-100'}),
                   'remote_passwd': forms.TextInput(attrs={'class': 'width-100'}),
                   'type': forms.Select(attrs={'class':'form-control'}),
                   'serial': forms.TextInput(attrs={'class':'width-100'}),
                   'hostname': forms.TextInput(attrs={'class': 'width-100'}),
                   'public_ip': forms.TextInput(attrs={'class': 'width-100'}),
                   'cpu_no': forms.NumberInput(attrs={'class': 'width-100'}),
                   'cpu_model': forms.TextInput(attrs={'class': 'width-100'}),
                   'memory': forms.NumberInput(attrs={'class': 'width-100'}),
                   'disk': forms.NumberInput(attrs={'class': 'width-100'}),
                   'os': forms.TextInput(attrs={'class': 'width-100'}),
                   'kernel': forms.TextInput(attrs={'class': 'width-100'}),
                   'machine_model': forms.TextInput(attrs={'class': 'width-100'}),
                   'position': forms.TextInput(attrs={'class': 'width-100'}),
                   'group': forms.Select(attrs={'class':'form-control'}),
                   'operate_status': forms.Select(attrs={'class':'form-control'}),
                   'agent_status': forms.Select(attrs={'class':'form-control'}),
                   'department': forms.TextInput(attrs={'class':'form-control'}), #20L
                   }
        help_texts = {
            'private_ip':'Some useful help text.',
        }
    

class HostGroupForm(forms.ModelForm):
    class Meta:
        model = HostGroup
        fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'width-100'}),
                   'description': forms.TextInput(attrs={'class': 'width-100'}),
                   'maintainer': forms.TextInput(attrs={'class': 'width-100'}),
                   'tel': forms.TextInput(attrs={'class': 'width-100'}),
                   'email': forms.EmailInput(attrs={'class': 'width-100'})
                   }