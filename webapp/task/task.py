#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年8月6日

@author: yangxu
'''
from django.views.generic import TemplateView,FormView,ListView,DeleteView,UpdateView,DetailView
from django.urls import reverse_lazy
from webapp.models import AssetHost,ScriptModel,HostAccount,TaskLog, TaskHost,AnsibleModel
from forms import ScriptModelForm
from firecloud.constants import SCRIPT_SAVE_PATH,SCRIPT_PICKLE_PATH,ANSIBLE_PROJECT_PATH
import os,uuid
from django.http import JsonResponse
from utils.ansibleAdHoc import myadhoc
from utils.callback import ScriptExecuteCallback,FileCopyCallback
from utils.log_task_execute import log_task_execute
from utils.cfg_parser import confParse
import linecache
import pickle
import json
import sys
import io,yaml
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
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
    
class AnsibleList(ListView):
    model = AnsibleModel
    context_object_name = 'ansibles'
    template_name = 'task/ansible/AnsibleList.html'
    
# ------------------ ansible add -----------------------------------    
class AnsibleAdd(TemplateView):
    template_name = 'task/ansible/AnsibleAdd.html'
    def get_context_data(self, **kwargs):
        context = super(AnsibleAdd, self).get_context_data(**kwargs)
        if self.request.session.get('_user_id') == 1:
            assetHostQuerySet = AssetHost.objects.all().order_by('private_ip')
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=self.request.session.get('_user_id')).order_by('private_ip')
        context['hosts'] = generate_host_list(assetHostQuerySet)
        context['total_host_count'] = len(context['hosts'])
        return context

def save_upload_file(playbook_name,role_name,file_type,f):
    full_play_dir = os.path.join(ANSIBLE_PROJECT_PATH,playbook_name)
    full_role_dir = os.path.join(full_play_dir+'/roles',role_name)
    full_type_dir = os.path.join(full_role_dir,file_type) # lamp/install_db/templates
    full_name = os.path.join(full_type_dir,f.name) #l lamp/install_db/templates/my.cnf.j2
    if not os.path.exists(full_type_dir):
        os.makedirs(full_type_dir, 0755)
    destination = open(full_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def del_upload_file(request):
    if request.method == 'POST':
        playbook_name = request.POST.get('playbook_name')
        role_name = request.POST.get('role_name')
        file_type = request.POST.get('file_type')+'s'
        file_name = request.POST.get('file_name')
        full_name = os.path.join(ANSIBLE_PROJECT_PATH,playbook_name+'/roles/'+\
                                 role_name+'/'+file_type+'/'+file_name)
        if os.path.exists(full_name):
            os.remove(full_name)
        
    return JsonResponse({'status':200})

def ansible_upload_file(request):
    if request.method == 'POST':
        f = request.FILES['file']
        playbook_name = request.POST.get('playbook_name')
        role_name = request.POST.get('role_name')
        file_type = request.POST.get('file_type')
        save_upload_file(playbook_name, role_name, file_type, f)
    return JsonResponse({'status':200})

def gen_main_yaml_and_hosts_file(playbook_data_dict):
    keys = playbook_data_dict.keys()
    keys.sort()
    '''
    [
    {"group":"install_db","hosts":['192.168.10.3:root','192.168.10.4:clouder']},
    ]
    '''
    host_data_list = []
    main_data_list = []
    total_role_count = 0
    for key in keys:
        '''
        {"group":"install_db","hosts":['192.168.10.3:root','192.168.10.4:clouder']}
        '''
        host_data_dict_tmp = {}
        main_data_dict_tmp = {}
        if 'step' in key:
            host_data_dict_tmp['group'] = str(playbook_data_dict[key]['role_name'])
            host_data_dict_tmp['hosts'] = playbook_data_dict[key]['hosts']
            main_data_dict_tmp['name'] = str(playbook_data_dict[key]['role_name'])
            main_data_dict_tmp['hosts'] = str(playbook_data_dict[key]['role_name'])
            main_data_dict_tmp['roles'] = []
            main_data_dict_tmp['roles'].append(str(playbook_data_dict[key]['role_name']))
            total_role_count = total_role_count + 1
            host_data_list.append(host_data_dict_tmp)
            main_data_list.append(main_data_dict_tmp)
    full_play_dir = os.path.join(ANSIBLE_PROJECT_PATH,playbook_data_dict['playbook_name'])
    full_filename = os.path.join(full_play_dir,'main.yml')
    with io.open(full_filename,'w',encoding='utf8') as f:
        yaml.dump(main_data_list, f, default_flow_style=False, allow_unicode=True)
    
    host_full_filename = os.path.join(full_play_dir,'hosts')    
    with open(host_full_filename,'w') as hf:
        for host in host_data_list:
            group_name = host['group']
            hf.write('['+group_name+']')
            hf.write('\n')
            for one_host in generate_host(host['hosts']):
                hf.write(one_host)
                hf.write('\n')
            hf.write('\n')
            
def generate_host(host_list):
    '''['192.168.10.3:root','192.168.10.4:clouder']
    generate host  list,  eg: 
    [
        '192.168.10.3 ansible_ssh_user=root ansible_ssh_port = 22',
        '192.168.10.4 ansible_ssh_user=root ansible_ssh_port = 22',
    ]
    '''
    data_list = []
    for item in host_list:
        var_dict = ''
        host_ip = item.split(':')[0]
        assetHostObj = AssetHost.objects.get(private_ip=host_ip)
        var_dict = var_dict+host_ip
        host_account = item.split(':')[1]
        if len(host_account.strip()) ==0:
            host_account = 'root'
        try:
            accountObj = HostAccount.objects.get(Q(host_id=assetHostObj.id),Q(account=host_account))
        except ObjectDoesNotExist:
            password = 'password'
        else:
            password = accountObj.passwd
        var_dict = var_dict+' ansible_ssh_user={} ansible_ssh_password={}'.format(host_account,password)
        data_list.append(var_dict)
    return data_list            
    
def playbook_mkdirs(full_dir):
    if not os.path.exists(full_dir):
        os.makedirs(full_dir, 0775)
       
def save_task_handler_var(playbook_data_dict):
    tasks = 0
    keys = playbook_data_dict.keys()
    full_play_dir = os.path.join(ANSIBLE_PROJECT_PATH,playbook_data_dict['playbook_name'])
    for key in keys:
        if 'step' in key:
            role_dir = os.path.join(full_play_dir+'/roles',playbook_data_dict[key]['role_name'])
            task_content = playbook_data_dict[key]['tasks']
            handler_content = playbook_data_dict[key]['handlers']
            var_content = playbook_data_dict[key]['vars']
            if len(task_content.strip()) !=0:
                x=yaml.load(task_content)
                if x is not None:
                    tasks = tasks + len(x)
                task_dir = os.path.join(role_dir,'tasks')
                playbook_mkdirs(task_dir)
                with open(task_dir+'/main.yml','w') as f:
                    f.write(task_content)
            if len(handler_content.strip()) !=0:
                handler_dir = os.path.join(role_dir,'handlers')
                playbook_mkdirs(handler_dir)
                with open(handler_dir+'/main.yml','w') as f:
                    f.write(handler_content)
            if len(var_content.strip()) !=0:
                var_dir = os.path.join(role_dir,'vars')
                playbook_mkdirs(var_dir)
                with open(var_dir+'/main.yml','w') as f:
                    f.write(var_content)
    return tasks

def ansible_save(request):
    if request.method == 'POST':
        save_dict = {}
        playbook_data_str = str(request.POST.get('playbook_data'))
        playbook_data_dict = json.loads(playbook_data_str)
        total_role_count = playbook_data_dict.keys()
        owner_id = int(request.session.get('_user_id'))
        save_dict['name'] = playbook_data_dict['playbook_name']
        if request.POST.get('action_type') == 'save':
            try:
                AnsibleModel.objects.get(name=save_dict['name'])
            except ObjectDoesNotExist:
                total_task_count = save_task_handler_var(playbook_data_dict)
                save_dict['owner_id'] = owner_id
                save_dict['total_run_count'] = 0
                save_dict['dir_name'] = playbook_data_dict['playbook_name']
                save_dict['total_role_count'] = len(total_role_count) - 1
                save_dict['total_task_count'] = total_task_count
                gen_main_yaml_and_hosts_file(playbook_data_dict)
                AnsibleModel.objects.create(**save_dict)
                return JsonResponse({'status':200})
            else:
                return JsonResponse({'status':500,'msg':'{}剧本名已经存在!'.format(save_dict['name'])})
            
        if request.POST.get('action_type') == 'update':
            playbook_id = request.POST.get('playbook_id')
            try:
                ansibleObj = AnsibleModel.objects.get(id=playbook_id)
            except ObjectDoesNotExist:
                return JsonResponse({'status':500,'msg':'剧本ID:{}不存在!'.format(playbook_id)})
            else:
                new_playbook_dir = os.path.join(ANSIBLE_PROJECT_PATH,playbook_data_dict['playbook_name'])
                old_playbook_dir = os.path.join(ANSIBLE_PROJECT_PATH,ansibleObj.name)
                os.rename(old_playbook_dir, new_playbook_dir)
                total_task_count = save_task_handler_var(playbook_data_dict)
                ansibleObj.name = playbook_data_dict['playbook_name']
                ansibleObj.dir_name = playbook_data_dict['playbook_name']
                ansibleObj.total_role_count = len(total_role_count) - 1
                ansibleObj.total_task_count = total_task_count
                gen_main_yaml_and_hosts_file(playbook_data_dict)
                ansibleObj.save()
                return JsonResponse({'status':200})
                
            
            
        
        
# ------------------end ansible add -----------------------------------  


# ------------------ansible update -----------------------------------
class AnsibleUpdate(UpdateView):
    model = AnsibleModel
    pk_url_kwarg = 'pk'
    form_class = ScriptModelForm
    template_name = 'task/ansible/AnsibleUpdate.html'
    success_url = reverse_lazy('AnsibleList')
    def get_context_data(self, **kwargs):
        context = super(AnsibleUpdate,self).get_context_data(**kwargs)
        if self.request.session.get('_user_id') == 1:
            assetHostQuerySet = AssetHost.objects.all().order_by('private_ip')
        else:
            assetHostQuerySet = AssetHost.objects.filter(owner_id=self.request.session.get('_user_id')).order_by('private_ip')
        context['hosts'] = generate_host_list(assetHostQuerySet)
        context['total_host_count'] = len(context['hosts'])
        playbook_dict = get_playbook_file_content(self.object.id)
        playbook_dict['playbook_id'] = self.object.id
        context['playbook_info'] = playbook_dict
        return context

def get_playbook_file_content(playbook_id):
    '''
    return all files content under the playbook_name directory of subdirectory, data format,eg:
    {
        "playbook_name":"lamp",
        "steps":[
            {
            "role_name":"install_db",
            "tasks": "contents",
            "handlers": "contents",
            "vars": "contents",
            "templates":[{'file_name':'file1','size':'125KB'},{'file_name':'file1','size':'125KB'}],
            "hosts": [{'ip':192.168.10.3,'account':'root','password':'password'}]
            }
        ]
    }
    '''
    playbook_dict = {}
    playbook_dict['steps'] = []
    playbookObj = AnsibleModel.objects.get(id=playbook_id)
    playbook_name = playbookObj.name
    playbook_dict['playbook_name'] = playbook_name
    playbook_dir = os.path.join(ANSIBLE_PROJECT_PATH,playbook_name)
    full_hosts_file = os.path.join(playbook_dir,'hosts')
    full_main_file = os.path.join(playbook_dir,'main.yml')
    # get roles list
    roles_list = get_roles_list_from_main(full_main_file)
    # get hosts contents 
    host_position = get_role_position_in_hosts(full_hosts_file)
    hosts_dict = gen_role_host_list_from_hosts(full_hosts_file, host_position)
    # get tasks,vars,handlers,templates,files info
    for role_name in roles_list:
        step_dict = get_playbook_other_info(playbook_dir, role_name)
        step_dict['hosts'] = hosts_dict[role_name]
        playbook_dict['steps'].append(step_dict)
    return playbook_dict
    
    
def get_playbook_other_info(playbook_dir,role_name):
    '''
    get the role's conents of tasks,vars,handlers conents and the file list of templates,files if exist
    {
    "role_name":"install_db"
    "tasks": "contents",
    "handlers": "contents",
    "vars": "contents",
    "templates":[{'file_name':'file1','size':'125KB'},{'file_name':'file1','size':'125KB'}],
    "files":[{'file_name':'file1','size':'125KB'},{'file_name':'file1','size':'125KB'}],  
    }
    '''
    role_dict = {}
    role_dict['role_name'] = role_name
    role_dir = os.path.join(playbook_dir,'roles/'+role_name)
    dir_list = os.listdir(role_dir)
    for one_dir in dir_list:
        if one_dir in ['templates','files']:
            role_dict[one_dir] = []
            tmp_dir = os.path.join(role_dir,one_dir)
            file_list = os.listdir(tmp_dir)
            for one_file in file_list:
                tmp_fullname = os.path.join(tmp_dir,one_file)
                if os.path.isfile(tmp_fullname):
                    file_dict = {}
                    file_dict['file_name'] = one_file
                    file_size = int(round(float(os.path.getsize(tmp_fullname))/1024,0))
                    file_dict['size'] = str(file_size)+'kb'
                    role_dict[one_dir].append(file_dict)
        elif one_dir in ['tasks','handlers','vars']:
            tmp_dir = os.path.join(role_dir,one_dir)
            main_fullname = os.path.join(tmp_dir,'main.yml')
            with open(main_fullname,'r') as f:
                contents = f.read()
            role_dict[one_dir] = contents
    return role_dict
        

def get_roles_list_from_main(full_main_file):
    '''
    ['install_db','install_web']
    '''
    roles_list = []
    with open(full_main_file,'r') as f:
        x = yaml.load(f)
        for role in x:
            roles_list.append(role['name'])
    return roles_list

def gen_role_host_list_from_hosts(full_hosts_file,host_position):
    '''
    {'install_db':[{'ip':192.168.10.3,'account':'root','password':'password'}]}
    '''
    roles_dict = {}
    for role in host_position:
        all_lines_list = linecache.getlines(full_hosts_file)[role['start']:role['end']]
        role_name = all_lines_list[0].strip().strip('[').strip(']')
        roles_dict[role_name] = []
        for i in range(1,len(all_lines_list)):
            tmp_dict = {}
            line_str = all_lines_list[i].strip()
            if len(line_str) !=0:
                split_list = line_str.split()
                tmp_dict['ip'] = split_list[0]
                tmp_dict['account'] = split_list[1].split('=')[1]
                tmp_dict['password'] = split_list[2].split('=')[1]
                roles_dict[role_name].append(tmp_dict)
    return roles_dict  
                    
def get_role_position_in_hosts(full_hosts_file):
    '''
    [
        {'name':'install_db','start':0,'end':3},
        {'name':'install_web','start':3,'end':None}  None is mean [3:]
    ]
    '''
    confObj = confParse(full_hosts_file)
    sections = confObj.get_sections()
    host_position = []
    def get_line_num(section):
        with open(full_hosts_file,'r') as f:
            line_num = 0
            for line in f.readlines():
                if section in line:
                    return line_num
                line_num = line_num + 1
    
    for i in range(len(sections)):
        position_dict = {}
        line_num = get_line_num(sections[i])
        start = line_num
        position_dict['name'] = sections[i]
        position_dict['start'] = start
        position_dict['end'] = 0
        host_position.append(position_dict)
        if i !=0:
            host_position[i-1]['end'] = start
        if i == len(sections) - 1:
            host_position[i]['end'] = None
    return host_position
    
    
# ------------------end ansible update -----------------------------------  

# ---------------------ansible delete -----------------------------------
class AnsibleDelete(DeleteView):
    model = AnsibleModel
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('AnsibleList')
    def post(self, request, *args, **kwargs):
        ansibleObj = AnsibleModel.objects.get(id=kwargs['pk'])
        playbook_dir = os.path.join(ANSIBLE_PROJECT_PATH,ansibleObj.name)
        if os.path.exists(playbook_dir):
            import shutil
            shutil.rmtree(playbook_dir, ignore_errors=True)
        return DeleteView.post(self, request, *args, **kwargs)

# ---------------------end ansible delete -----------------------------------

class AnsibleExecute(TemplateView):
    template_name = 'task/ansible/AnsibleExecute.html'
    
class FileSend(TemplateView):
    template_name = 'task/file/file.html'