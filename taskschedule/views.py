#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年11月13日

@author: yangxu
'''
from django.views.generic import ListView,FormView,UpdateView,TemplateView,DeleteView
from forms import PeriodicTaskForm,CrontabScheduleForm,IntervalScheduleForm
from djcelery.models  import PeriodicTask,CrontabSchedule,IntervalSchedule
from django.urls import reverse_lazy

class ListTask(ListView):
    model = PeriodicTask
    context_object_name = 'task_list'
    template_name = 'celery_task/task/ListTask.html'
    
    
class AddTask(FormView):
    form_class =PeriodicTaskForm
    template_name = 'celery_task/task/AddTask.html'
    success_url = reverse_lazy('ListTask')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class UpdateTask(UpdateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    pk_url_kwarg = 'pk' #指明url 的key 为pk
    success_url = reverse_lazy('ListTask')
    template_name = 'celery_task/task/UpdateTask.html'

class DeleteTask(DeleteView):
    model = PeriodicTask
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ListTask')
    
class ListCrontab(ListView):
    model = CrontabSchedule
    ordering = ['id']
    context_object_name = 'crontab_list'
    template_name = 'celery_task/crontab/ListCrontab.html'
    
class AddCrontab(FormView):
    form_class =CrontabScheduleForm
    template_name = 'celery_task/crontab/AddCrontab.html'
    success_url = reverse_lazy('ListCrontab')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class UpdateCrontab(UpdateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    pk_url_kwarg = 'pk' #指明url 的key 为pk
    success_url = reverse_lazy('ListCrontab')
    template_name = 'celery_task/crontab/UpdateCrontab.html'

class DeleteCrontab(DeleteView):
    model = CrontabSchedule
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ListCrontab')
    
class ListInterval(ListView):
    model = IntervalSchedule
    ordering = ['id']
    context_object_name = 'interval_list'
    template_name = 'celery_task/interval/ListInterval.html'
    
class AddInterval(FormView):
    form_class =IntervalScheduleForm
    template_name = 'celery_task/interval/AddInterval.html'
    success_url = reverse_lazy('ListInterval')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class UpdateInterval(UpdateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    pk_url_kwarg = 'pk' #指明url 的key 为pk
    success_url = reverse_lazy('ListInterval')
    template_name = 'celery_task/interval/UpdateInterval.html'

class DeleteInterval(DeleteView):
    model = IntervalSchedule
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ListInterval')

 
class FlowerMonitor(TemplateView):
    template_name = 'celery_task/task/flower.html'   

    
    