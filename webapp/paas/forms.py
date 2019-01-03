#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午3:16:03
@author: yangxu
'''

from django import forms
from webapp.models import RepositoryHost

class RepositoryHostForm(forms.ModelForm):
    class Meta:
        model = RepositoryHost
        fields = "__all__"