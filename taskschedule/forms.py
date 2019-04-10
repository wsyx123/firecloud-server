#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年10月29日

@author: yangxu
'''
from django import forms
from djcelery.models  import PeriodicTask,CrontabSchedule,IntervalSchedule
from djcelery.admin import TaskChoiceField
from django.utils.translation import ugettext_lazy as _

class PeriodicTaskForm(forms.ModelForm):
    task = TaskChoiceField(label=_('Task (registered)'),
                              required=False)
    class Meta:
        model = PeriodicTask
        fields = "__all__"
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'task': forms.Select(attrs={'class':'form-control'}),
                   'args': forms.TextInput(attrs={'class': 'form-control'}),
                   'kwargs': forms.TextInput(attrs={'class': 'form-control'}),
                   'queue': forms.Select(attrs={'class': 'form-control'}),
                   'exchange': forms.Select(attrs={'class':'form-control'}),
                   'routing_key': forms.Select(attrs={'class':'form-control'}),
                   'expires': forms.TimeInput(attrs={'class':'form-control','placeholder':'2018-12-12 00:00:01'}),
                   'enabled': forms.CheckboxInput(attrs={'class':'ace ace-checkbox-2'}),
                   'crontab': forms.Select(attrs={'class':'form-control'}),
                   'interval': forms.Select(attrs={'class':'form-control'})
                   }
        
class CrontabScheduleForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = "__all__"
    
class IntervalScheduleForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"

        