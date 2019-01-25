#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午3:16:03
@author: yangxu
'''

from django import forms
from webapp.models import RepositoryHost,MesosMaster,MesosMarathon,MesosHaproxy,MesosSlave

class RepositoryHostForm(forms.ModelForm):
    class Meta:
        model = RepositoryHost
        fields = "__all__"

class MesosMasterForm(forms.ModelForm):
    class Meta:
        model = MesosMaster
        fields = "__all__"
        
class MesosMarathonForm(forms.ModelForm):
    class Meta:
        model = MesosMarathon
        fields = "__all__"
        
class MesosHaproxyForm(forms.ModelForm):
    class Meta:
        model = MesosHaproxy
        fields = "__all__"
        
class MesosSlaveForm(forms.ModelForm):
    class Meta:
        model = MesosSlave
        fields = "__all__"