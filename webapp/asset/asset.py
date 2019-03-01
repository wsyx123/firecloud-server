#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年7月28日

@author: yangxu
'''
from dwebsocket import accept_websocket
from webapp.models import AssetHost,HostGroup,HostImport,HostEvent,HostAccount,SysUser,HostDisk,HostEth
from webapp.asset.forms import AssetHostForm,HostGroupForm
from ssh_client.client import connect
from django.shortcuts import render_to_response,HttpResponse
from django.views.generic import TemplateView,ListView,FormView,DeleteView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
import json
import xlrd
from webapp.tasks import process_asset_import_task,collect_host_info_task
import os,sys
from django.http.response import JsonResponse
root_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

class AssetView(ListView):
    model = AssetHost #数据模型
    context_object_name = 'host_list' #QuerySet 变量名
    template_name = 'asset/view/asset_index.html'
    
class HostList(ListView):
    model = AssetHost #数据模型
    context_object_name = 'host_list' #QuerySet 变量名
    template_name = 'asset/host/listhost.html'

class HostAdd(FormView):
    template_name = 'asset/host/addhost.html'
    form_class = AssetHostForm
    success_url = reverse_lazy('HostList')
    
    def post(self, request, *args, **kwargs): 
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 
        
    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        if self.request.POST.get('auto-collect').upper() == 'YES':
            self.object = form.save()
            collect_host_info_task.delay(self.object.id,self.object.private_ip,self.object.port,
                                    self.object.remote_user,self.object.remote_passwd,2)
        return super(HostAdd, self).form_valid(form)
    

class HostUpdate(UpdateView):
    model = AssetHost
    form_class = AssetHostForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('HostList')
    template_name = 'asset/host/edithost.html'
    
def host_refresh(request):
    if request.method == 'POST':
        key = request.POST.get('pk')
        obj = AssetHost.objects.get(id=key)
        try:
            collect_host_info_task.delay(obj.id,obj.private_ip,obj.port,obj.remote_user,obj.remote_passwd,3)
            status = 200
            err_msg = ''
        except Exception as e:
            status = 400
            err_msg = str(e)
    return JsonResponse({'status':status,'err_msg':err_msg})
        

class HostDelete(DeleteView):
    model = AssetHost
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('HostList')
    
class HostDetail(DetailView):
    model = AssetHost
    pk_url_kwarg = 'pk'
    context_object_name = 'detailhost' #QuerySet 变量名
    template_name = 'asset/host/detailhost.html'
    
    def get_context_data(self, **kwargs):
        context = super(HostDetail, self).get_context_data(**kwargs)
        context['EventQuerySet'] = HostEvent.objects.filter(host_id=context['object'].id)
        context['DiskQuerySet'] = HostDisk.objects.filter(host_id=context['object'].id)
        context['EthQuerySet'] = HostEth.objects.filter(host_id=context['object'].id)
        return context

def handle_uploaded_file(import_id,f):
    file_suffix = (f.name).split('.')[1]
    filename = root_dir+'/static/upload/'+str(import_id)+'.'+file_suffix
    destination = open(filename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filename

def host_import(request):
    import_info = {'status':False,'import_id':None,'total_line':0,'succeeded_line':0,'failure_line':0}
    if request.method == 'POST':
        filename = str(request.FILES['file'])
        if filename.endswith('xlsx') or filename.endswith('xls'):
            wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['file'].read())
            table = wb.sheets()[0]
            total_rows = table.nrows-2
            res = HostImport.objects.create(filename=filename,total_line=total_rows)
            import_info['import_id'] = res.id
            import_info['total_line'] = total_rows
            import_info['status'] = True
            full_filename = handle_uploaded_file(res.id,request.FILES['file'])
            process_asset_import_task.delay(res.id,full_filename)
#             datalist = get_assets_data(full_filename)
#             asset_format_check(res.id,datalist)
            return HttpResponse(json.dumps(import_info),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status':False,'err_msg':u'请上传excel文件'}),content_type="application/json")
    UserObj = SysUser.objects.get(id=request.session['_user_id'])
    return render_to_response('asset/host/importhost.html',{'roleid':UserObj.role_id,'username':UserObj.username})

def get_import_result(request):
    import_info = {'total_line':0,'succeeded_line':0,
                   'failure_line':0,'is_finished':False}
    if request.method == 'POST':
        key = request.POST.get('pk')
        obj = HostImport.objects.get(id=key)
        import_info['total_line'] = obj.total_line
        import_info['succeeded_line'] = obj.succeeded_line
        import_info['failure_line'] = obj.failure_line
        import_info['is_finished'] = obj.is_finished
        return HttpResponse(json.dumps(import_info),content_type="application/json")
        
class AccountList(ListView):
    model = HostAccount #数据模型
    context_object_name = 'user_list' #QuerySet 变量名
    template_name = 'asset/host/listHostUser.html'
  

@accept_websocket
def asset_connect(request):
    if request.is_websocket():
        connect(request)
    return render_to_response("asset/host/terminal.html")
    
class GroupList(ListView):
    model = HostGroup  #数据模型
    context_object_name = 'group_list' #QuerySet 变量名
    template_name = 'asset/hostgroup/hostgroup.html'
    
class GroupAdd(FormView):
    template_name = 'asset/hostgroup/AddGroup.html'
    form_class = HostGroupForm
    success_url = reverse_lazy('GroupList')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class GroupUpdate(UpdateView):
    model = HostGroup
    form_class = HostGroupForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('GroupList')
    template_name = 'asset/hostgroup/UpdateGroup.html'
    
class GroupDelete(DeleteView):
    model = HostGroup
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('GroupList')
    
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            err_msg = u'组内还有成员'
            return HttpResponse(json.dumps({'status':False,'err_msg':err_msg}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status':True}),content_type="application/json")
    
    
class Enterprise(TemplateView):
    template_name = 'asset/enterprise/enterprise.html'
   
    
class AddDepartment(TemplateView):
    template_name = 'asset/enterprise/addDepartment.html'
    
class Employee(TemplateView):
    template_name = 'asset/enterprise/Employee.html'
    def get_context_data(self, **kwargs):
        context = super(Employee, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['employees'] = [{'number':'101','name':'David','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'UI设计师','email':'david@firecloud.com'},
                                {'number':'102','name':'Jack','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'高级JAVA工程师','email':'jack@firecloud.com'},
                                {'number':'103','name':'Tom','enterprise':'Firecloud科技有限公司','department':'云计算组','job':'云计算架构师','email':'tom@firecloud.com'},
                            ]
        return context

class AddEmployee(TemplateView):
    template_name = 'asset/enterprise/addEmployee.html'
    

class Project(TemplateView):
    template_name = 'asset/enterprise/Project.html'
    def get_context_data(self, **kwargs):
        context = super(Project, self).get_context_data(**kwargs)
        context['name'] = u'杨旭'
        context['projects'] = [{'id':'20180805011','name':'IAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'需求分析','current_status':'需求分析'},
                               {'id':'20180805012','name':'PAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'概要设计','current_status':'概要设计'},
                               {'id':'20180805013','name':'SAAS','enterprise':'Firecloud科技有限公司','department':'云计算组','status':'技术选型','current_status':'技术选型'},
                            ]
        return context
    
class AddProject(TemplateView):
    template_name = 'asset/enterprise/addProject.html'