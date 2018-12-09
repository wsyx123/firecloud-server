#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月6日

@author: yangxu
'''
from django.views.generic import TemplateView,FormView,ListView,DeleteView,UpdateView,DetailView
from django.urls import reverse_lazy
from webapp.models import AssetHost,ScriptModel,HostAccount,TaskLog, TaskHost
from forms import ScriptModelForm
from firecloud.constants import SCRIPT_SAVE_PATH,SCRIPT_PICKLE_PATH
import os,uuid
from django.http import JsonResponse
from utils.ansibleAdHoc import myadhoc
from utils.callback import ScriptExecuteCallback,FileCopyCallback
from utils.log_task_execute import log_task_execute
import pickle
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def generate_host_var(var_str):
    '''
    generate variable  list,  eg: 
    [
        {'192.168.10.3':
            {'ansible_ssh_user':'root',
            'ansible_ssh_port': '22',}
        },
    ]
    '''
    data_list = []
    var_list = var_str.split(',')
    for item in var_list:
        if item == '':
            continue
        var_dict = {}
        host_ip = item.split(':')[0]
        host_account = item.split(':')[1]
        var_dict[host_ip]={'ansible_ssh_user':host_account}
        data_list.append(var_dict)
    return data_list
    
def generate_host_port_str(host_account_str):
    '''
    generate host:port  string , eg:   192.168.10.3:22,192.168.10.4:22,
    '''
    hosts_str = ''
    hosts_list = host_account_str.split(',')
    for item in hosts_list:
        if item == '':
            continue
        host_ip = item.split(':')[0]
        assetObj = AssetHost.objects.get(private_ip=host_ip)
        host_port = assetObj.port
        hosts_str = hosts_str+host_ip+':'+str(host_port)+','
    return hosts_str


class OptList(ListView):
    model = TaskLog
    context_object_name = 'logs'
    template_name = 'task/record/optlog.html'
    
class OptAudit(DetailView):
    model = TaskLog
    pk_url_kwarg = 'pk'
    context_object_name = 'OptLogDetail' #QuerySet 变量名
    template_name = 'task/record/OptAudit.html'
    def get_context_data(self, **kwargs):
        context = super(OptAudit, self).get_context_data(**kwargs)
        script_file=context['object'].script_file
        context['task_hosts'] = TaskHost.objects.filter(task_id=context['object'].task_id)
        try:
            with open(script_file,'r') as f:
                context['script'] = {'fullname':script_file,'contents':f.read(),'status':True}
        except IOError:
            context['script'] = {'fullname':script_file,'contents':'脚本已被删除!!!','status':False}
        return context
    
def OptDelete(request):
    if request.method == 'POST':
        task_id_str = request.POST.get('task_id_str')
        task_id_list = task_id_str.split(',')
        for task_id in task_id_list:
            TaskLog.objects.get(task_id=task_id).delete()
    return JsonResponse({'status':200})
    

def generate_host_list(assetHostQuerySet):
        host_list = []
        for host in assetHostQuerySet:
            accountQuerySetList = HostAccount.objects.filter(host_id=host.id)
            host_dict = {}
            host_dict['hostname'] = host.hostname
            host_dict['host_status'] = host.host_status
            host_dict['private_ip'] = host.private_ip
            host_dict['accounts'] = accountQuerySetList
            host_list.append(host_dict)
        return host_list

class ScriptList(ListView):
    model = ScriptModel
    context_object_name = 'scripts'
    template_name = 'task/script/ScriptList.html'
    
    def get_context_data(self, **kwargs):
        context = super(ScriptList, self).get_context_data(**kwargs)
        if self.request.session.get('_user_id') == 1:
            assetHostQuerySet = AssetHost.objects.all().order_by('private_ip')
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=self.request.session.get('_user_id')).order_by('private_ip')
        context['hosts'] = generate_host_list(assetHostQuerySet)
        context['total_host_count'] = len(context['hosts'])
        return context

class ScriptAdd(FormView):
    template_name = 'task/script/ScriptAdd.html'
    form_class = ScriptModelForm
    success_url = reverse_lazy('ScriptList')
    scriptTypeDict1 = {
                  1:'sh',
                  2:'py',
                  3:'pl'
                  }
    scriptTypeDict2 = {
                      'sh':'bash',
                      'py':'python',
                      'pl':'perl'
                      }
    
    file_id = None
    file_suffix = None
    filename = None
    fullname = None
    
    
    def get_context_data(self, **kwargs):
        context = super(ScriptAdd, self).get_context_data(**kwargs)
        if self.request.session.get('_user_id') == 1:
            assetHostQuerySet = AssetHost.objects.all().order_by('private_ip')
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=self.request.session.get('_user_id')).order_by('private_ip')
        context['hosts'] = generate_host_list(assetHostQuerySet)
        context['total_host_count'] = len(context['hosts'])
        return context
    
    def handle_uploaded_file(self,f):
        self.file_suffix = (f.name).split('.')[1]
        self.file_id = uuid.uuid4().hex[:8]
        self.filename = self.file_id+'.'+self.file_suffix
        self.fullname = os.path.join(SCRIPT_SAVE_PATH,self.filename)
        destination = open(self.fullname, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        
    def prepare_request_post(self,request_post,script_from):
        script_type = int(request_post.get('script_type'))
        self.file_suffix = self.scriptTypeDict1[script_type]
        self.file_id = uuid.uuid4().hex[:8]
        self.filename = self.file_id+'.'+self.file_suffix
        if script_from == 1 or script_from == 3:
            contents = request_post.get('script_content')
            self.fullname = os.path.join(SCRIPT_SAVE_PATH,self.filename)
            with open(self.fullname, 'wb') as f:
                f.write(contents)
            request_post['script_file'] = self.filename
        elif script_from == 2:
            request_post['script_file'] = self.filename  
        return request_post
            
    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        script_from = int(request.POST.get('script_from'))
        action_type = request.POST.get('action_type')
        task_name = request.POST.get('name')

        if script_from == 1 or script_from == 3:
            request.POST=self.prepare_request_post(request.POST,script_from)
        elif script_from == 2:
            self.handle_uploaded_file(request.FILES['script_file'])
            request.POST=self.prepare_request_post(request.POST,script_from)
        if action_type == 'save':
            form = self.get_form()
            if form.is_valid():
                form.save(commit=True)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif action_type == 'execute':
            '''
            host_account_str format eg:  192.168.10.3:clouder,192.168.10.4:root
            '''
            host_account_str = request.POST.get('checked_host_array')
            host_port_str = generate_host_port_str(host_account_str)
            hosts_var_list = generate_host_var(host_account_str)
            group = 'all'
            #first , copy script  to remote  host
            copy_task = [dict(action=dict(module='copy', 
                                          args='src={} dest=/tmp/ mode=755'.format(self.fullname))),]
            myCopy = myadhoc(copy_task,group,host_port_str,22,'root','password',
                             FileCopyCallback,hostVar=hosts_var_list)
            myCopy.run()
            myCopy_result = myCopy.results_callback._result
            
            ok_host_port_str = ''
            for host in myCopy_result['ok']:
                assetObj = AssetHost.objects.get(private_ip=host)
                host_port = assetObj.port
                ok_host_port_str = ok_host_port_str+host+':'+str(host_port)+','
            
            #second , Running the above copy of the script
            command = self.scriptTypeDict2[self.file_suffix]
            execute_task = [dict(action=dict(module='shell', args='{} /tmp/{} '.format(command,self.filename))),]
            myExecute=myadhoc(execute_task,group,ok_host_port_str,22,'root','password',
                              ScriptExecuteCallback,hostVar=hosts_var_list)
            myExecute.run()
            myExecute_result = myExecute.results_callback._result
            myExecute_result['task_id'] = self.file_id
            myExecute_result['task_name'] = task_name
            myExecute_result['failed']=myExecute_result['failed']+myCopy_result['failed']
            log_task_execute(myExecute_result,hosts_var_list,1,self.fullname,request.session.get('_user_id'))
            return JsonResponse(myExecute_result)
        else:
            return JsonResponse({'code':500})       
            
 
def get_script_content(request):
    if request.method == 'POST':
        haved_script_id = int(request.POST.get('haved_script_id'))
        scriptObj = ScriptModel.objects.get(id=haved_script_id)
        scriptname = scriptObj.script_file
        fullname = os.path.join(SCRIPT_SAVE_PATH,scriptname)
        try:
            with open(fullname,'r') as f:
                contents = f.read()
            return JsonResponse({'status':True,'contents':contents,'script_type':scriptObj.script_type})
        except IOError:
            msg = '文件不存在:'+fullname
            return JsonResponse({'status':False,'msg':msg})
    
class ScriptDelete(DeleteView):
    model = ScriptModel
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ScriptList')

class ExecuteClass():
    def __init__(self,scriptObj,host_port_str,host_var_list,fullname,task_id,user_id):
        self.group = 'all'
        self.scriptObj = scriptObj
        self.host_port_str = host_port_str
        self.host_var_list = host_var_list
        self.fullname = fullname
        self.task_id = task_id
        self.user_id = user_id
    def run_copy(self):
        #first , copy script  to remote  host
        copy_task = [dict(action=dict(module='copy', 
                                  args='src={} dest=/tmp/ mode=755'.format(self.fullname))),]
        myCopy = myadhoc(copy_task,self.group,self.host_port_str,22,'root','password',
                     FileCopyCallback,hostVar=self.host_var_list)
        myCopy.run()
        myCopy_result = myCopy.results_callback._result
        return myCopy_result
    
    def run_script(self):
        myCopy_result = self.run_copy()
        ok_host_port_str = ''
        for host in myCopy_result['ok']:
            assetObj = AssetHost.objects.get(private_ip=host)
            host_port = assetObj.port
            ok_host_port_str = ok_host_port_str+host+':'+str(host_port)+','
    
        #second , Running the above copy of the script
        script_type = {1:'bash',2:'python',3:'perl'}
        command = script_type[self.scriptObj.script_type]
        execute_task = [dict(action=dict(module='shell', args='{} /tmp/{} '.format(command,self.scriptObj.script_file))),]
        myExecute=myadhoc(execute_task,self.group,ok_host_port_str,22,'root','password',
                          ScriptExecuteCallback,hostVar=self.host_var_list)
        myExecute.run()
        myExecute_result = myExecute.results_callback._result
        myExecute_result['task_id'] = self.task_id
        myExecute_result['task_name'] = self.scriptObj.name
        myExecute_result['failed']=myExecute_result['failed']+myCopy_result['failed']
        log_task_execute(myExecute_result,self.host_var_list,1,self.fullname,self.user_id)
        return myExecute_result

def ScriptExecute(request):
    if request.method == 'POST':
        host_account_str = request.POST.get('checked_host_array')
        script_id = int(request.POST.get('id'))
        scriptObj = ScriptModel.objects.get(id=script_id)
        # script total_run_count + 1
        scriptObj.total_run_count = scriptObj.total_run_count + 1
        scriptObj.save()
        host_port_str = generate_host_port_str(host_account_str)
        host_var_list = generate_host_var(host_account_str)
        fullname = os.path.join(SCRIPT_SAVE_PATH,scriptObj.script_file)
        task_id = uuid.uuid4().hex[:8]
        user_id = request.session.get('_user_id')
        
        ExeInstance = ExecuteClass(scriptObj,host_port_str,host_var_list,fullname,task_id,user_id)
        pickle_file = os.path.join(SCRIPT_PICKLE_PATH,task_id+'.pkl')
        f = open(pickle_file,'w')
        pickle.dump(ExeInstance, f, 0)
        f.close()
        return JsonResponse({'task_id':task_id,'task_total':len(host_var_list)})

class ScriptExecuteResult(TemplateView):
    template_name = 'task/script/ScriptExecuteResult.html'
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('get_result'):
            task_id = request.GET.get('task_id')
            pickle_file = os.path.join(SCRIPT_PICKLE_PATH,task_id+'.pkl')
            f = open(pickle_file,'r')
            ExecInstance = pickle.load(f)
            f.close()
            exeResult = ExecInstance.run_script()
            return JsonResponse(exeResult)
        kwargs['task_id']=request.GET.get('task_id')
        kwargs['task_total']=request.GET.get('task_total')
        return TemplateView.get(self, request, *args, **kwargs)
    
class ScriptUpdate(UpdateView):
    model = ScriptModel
    pk_url_kwarg = 'pk'
    form_class = ScriptModelForm
    template_name = 'task/script/ScriptUpdate.html'
    success_url = reverse_lazy('ScriptList')
    def get_context_data(self, **kwargs):
        context = super(ScriptUpdate,self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            # return 'script_id' in order to get script_content by script_di
            context['script_id'] = self.object.id
            context['script_from'] = self.object.script_from
            context['script_type'] = self.object.script_type
        return context
    
    def post(self, request, *args, **kwargs):
        contents = request.POST.get('script_content')
        filename = request.POST.get('script_file')
        fullname = os.path.join(SCRIPT_SAVE_PATH,filename)
        with open(fullname, 'wb') as f:
            f.write(contents)
        return UpdateView.post(self, request, *args, **kwargs)
    
class AnsibleExecute(TemplateView):
    template_name = 'task/ansible/AnsibleExecute.html'
    
class AnsibleList(TemplateView):
    template_name = 'task/ansible/AnsibleList.html'
    
class AnsibleAdd(TemplateView):
    template_name = 'task/ansible/AnsibleAdd.html'
    
class FileSend(TemplateView):
    template_name = 'task/file/file.html'