#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月29日

@author: yangxu
'''
from django import forms
from webapp.models import ScriptModel,AnsibleModel,FileModel

class ScriptModelForm(forms.ModelForm):
    class Meta:
        model = ScriptModel
        fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'script_file': forms.TextInput(attrs={'class': 'form-control','readonly':'true'}),
                   }

class AnsibleModelForm(forms.ModelForm):
    class Meta:
        model = AnsibleModel
        fields = "__all__"

class FileModelForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = "__all__"

        