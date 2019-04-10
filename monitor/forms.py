#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on Mar 29, 2019

@author: yangxu
'''

from django import forms
from models import ZabbixNode


class ZabbixNodeForm(forms.ModelForm):
    class Meta:
        model = ZabbixNode
        fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'label': forms.Select(attrs={'class': 'form-control'}),
                   'version': forms.Select(attrs={'class': 'form-control'}),
                   'host': forms.Select(attrs={'class': 'form-control'}),
                   'port': forms.NumberInput(attrs={'class': 'form-control'}),
                   'run_model': forms.Select(attrs={'class': 'form-control'}),
                   'db_host':forms.TextInput(attrs={'class': 'form-control'}),
                   'db_port':forms.NumberInput(attrs={'class': 'form-control'}),
                   'db_database':forms.TextInput(attrs={'class': 'form-control'}),
                   'db_user':forms.TextInput(attrs={'class': 'form-control'}),
                   'db_password':forms.TextInput(attrs={'class': 'form-control'})
                   }