#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年7月28日

@author: yangxu
'''
from dwebsocket import accept_websocket
from models import AssetHost,HostGroup,HostImport,HostEvent,HostAccount,HostDisk,HostEth
from sysmgt.models import SysUser
from forms import AssetHostForm,HostGroupForm,HostAgentForm
from ssh_client.client import connect
from django.shortcuts import render_to_response,HttpResponse
from django.views.generic import TemplateView,ListView,FormView,DeleteView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
import json,xlrd,os,sys,datetime,urllib2
from tasks.celery_tasks import process_asset_import_task,collect_host_info_task
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from asset.models import HostAgent
from utils.elasticsearch.es_api import IndexApi,DocumentApi
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
    def post(self, request, *args, **kwargs):
        code = 200
        msg = ''
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            code = 400
            msg = e.message
        return JsonResponse({'code':code,'msg':msg})
    
class HostDetail(DetailView):
    model = AssetHost
    pk_url_kwarg = 'pk'
    context_object_name = 'detailhost' #QuerySet 变量名
    template_name = 'asset/host/detailhost-monitor.html'
    
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

class AgentRegister(TemplateView):
    def post(self,request):
        if request.method == 'POST':
            jsonData = json.loads(request.body)
            assetData = jsonData["asset"]
            startInfo = jsonData["agent"]
            assetData["owner"] = 1
            private_ip = assetData["private_ip"]
           
            #每次注册都检查资产记录,如果存在就更新
            try:
                AssetHost.objects.get(private_ip=private_ip)
            except ObjectDoesNotExist:
                AssetHost.objects.create(**assetData)#有可能创建失败
            else:
                AssetHost.objects.filter(private_ip=private_ip).update(**assetData)
            #每次注册都检查agent记录,如果存在就更新    
            try:
                HostAgent.objects.get(host=private_ip)
            except ObjectDoesNotExist:
                HostAgent.objects.create(**startInfo)#有可能创建失败
            else:
                HostAgent.objects.filter(host=private_ip).update(**startInfo)
        return JsonResponse({"code":702,"type":"register"})

class AgentHeartbeat(TemplateView):
    def post(self,request):
        if request.method == 'POST':
            jsonData = json.loads(request.body)
            host = jsonData["host"]
            try:
                #需要资产表,agent表中都有此ip记录才是正常
                AssetHost.objects.get(private_ip=host)
                HostAgent.objects.get(host=host)
            except Exception as e:
                return JsonResponse({"code":704,"type":"heartbeat","msg":e.message})
            else:
                HostAgent.objects.update(host=jsonData["host"],heartbeat_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                return JsonResponse({"code":702,"type":"heartbeat"})

def gen_monitor_data(indexObj,index,doc_type,host,interval,*args):
    data_dict = {"collect_time":[]}
    for arg in args:
        data_dict[arg] = []
    data = indexObj.search(index,doc_type,host,interval)
    data = json.loads(data["result"])
    for hit in data["hits"]["hits"]:
        data_dict["collect_time"].append(hit["_source"]["collect_time"][5:])
        for arg in args:
            data_dict[arg].append(hit["_source"][arg])
    for arg in args:
        data_dict[arg].reverse()
    data_dict["collect_time"].reverse()
    return data_dict

#通过agent api 获取主机运行情况
def get_host_status(host):
    agentObj = HostAgent.objects.get(host=host)
    port = agentObj.port
    url = "http://{}:{}/status".format(host,port)
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError:
        print("{}连接失败".format(url))
        return {"status":False}
    else:
        return {"status":True,"data":res.read()}

class HostStatus(TemplateView):
    def post(self,request):
        if request.method == 'POST':
            host = request.POST.get("host")
            res = get_host_status(host)
            if res["status"]:
                return JsonResponse(json.loads(res["data"]))
            else:
                return JsonResponse({"code":400})
        
class HostMonitor(TemplateView):
    def post(self,request):
        if request.method == 'POST':
            esObj = DocumentApi("172.16.149.10",9200)
            host = request.POST.get("host")
            interval = int(request.POST.get("time_value"))
            #cpu-load
            cpuLoadItem = ["load1","load5","load15"]
            cpuLoadData = gen_monitor_data(esObj, "cpu-load-2019-05", "cpu-load", host, interval,*cpuLoadItem)
            #cpu-usage
            cpuUsageItem = ["idle","iowait","user","system"]
            cpuUsageData = gen_monitor_data(esObj, "cpu-usage-2019-05", "cpu-usage", host, interval,*cpuUsageItem)
            #mem-usage
            memUsageItem = ["virt_available","virt_used","swap_available","swap_used"]
            memUsageData = gen_monitor_data(esObj,"mem-usage-2019-05", "mem-usage", host, interval,*memUsageItem)
            #disk-tps
            diskTpsItem = ["tps"]
            diskTpsData = gen_monitor_data(esObj, "disk-io-2019-05", "disk-io", host, interval,*diskTpsItem)
            #disk-speed
            diskSpeedItem = ["blks"]
            diskSpeedData = gen_monitor_data(esObj, "disk-io-2019-05", "disk-io", host, interval,*diskSpeedItem)
            #disk-usage
            diskUsageItem = ["available","used"]
            diskUsageData = gen_monitor_data(esObj, "disk-usage-2019-05", "disk-usage", host, interval,*diskUsageItem)
            #network
            networkItem = ["kb_recv","kb_sent"]
            networkData = gen_monitor_data(esObj, "net-io-2019-05", "net-io", host, interval,*networkItem)
            #netstat
            netstatItem = ["ESTABLISHED","LISTEN"]
            netstatData = gen_monitor_data(esObj, "net-conn-2019-05", "net-conn", host, interval,*netstatItem)
            #process
            processItem = ["processes","threads"]
            processData = gen_monitor_data(esObj, "process-thread-2019-05", "process-thread", host, interval,*processItem)
            
        return JsonResponse({"code":200,
                             "cpuload":cpuLoadData,
                             "cpuusage":cpuUsageData,
                             "memusage":memUsageData,
                             "disktps":diskTpsData,
                             "diskspeed":diskSpeedData,
                             "diskusage":diskUsageData,
                             "network":networkData,
                             "netstat":netstatData,
                             "process":processData
                             })
    
