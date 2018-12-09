# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
'''
auto_now:这个参数的默认值为false，设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改model，都会自动更新
auto_now_add:这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
'''
class SysRole(models.Model):
    name = models.CharField(max_length=16,unique=True,verbose_name='角色名')
    description = models.CharField(max_length=64,verbose_name='描述')
    home_page = models.ForeignKey('HomePage',blank=True, null=True,)
    def users(self):
        return SysUser.objects.filter(role_id=self.id)
    
    def __unicode__(self):
        return '%s' %(self.description)

class SysUser(models.Model):
    user_status = (
                   (1,'启用'),
                   (2,'禁用')
                   )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20,blank=False)
    description = models.CharField(max_length=64,null=True,blank=True)
    role = models.ForeignKey(SysRole,null=True,blank=True)
    tel = models.CharField(max_length=11)
    email = models.EmailField()
    status = models.IntegerField(choices=user_status,default=2,verbose_name='状态')
    last_login = models.DateTimeField(blank=True, null=True,verbose_name='最近登录')
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def role_id(self):
        return self.role.id
    def __unicode__(self):
        return '%s' %(self.username)


    
class Level1Menu(models.Model):
    name = models.CharField(max_length=16,verbose_name='一级菜单名称')
    description = models.CharField(max_length=32,verbose_name='中文描述')
    priority = models.IntegerField(verbose_name='菜单优先级')
    url = models.CharField(max_length=64,verbose_name='菜单url')
    menu_icon = models.CharField(max_length=32,verbose_name='菜单图标')
    
    def __unicode__(self):
        return '%s' %(self.name)

class Level2Menu(models.Model):
    parent_name = models.ForeignKey(Level1Menu,verbose_name='一级菜单名称')
    name = models.CharField(max_length=16,verbose_name='二级菜单名称')
    description = models.CharField(max_length=32,verbose_name='中文描述')
    priority = models.IntegerField(verbose_name='菜单优先级')
    url = models.CharField(max_length=64,verbose_name='菜单url')
    view = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.name)
    
class Menu_Role_rel(models.Model):
    role = models.ForeignKey(SysRole)
    level_1_menu = models.ForeignKey(Level1Menu)
    level_2_menu = models.ForeignKey(Level2Menu,null=True,blank=True)
    view = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.level_2_menu)
    
class HomePage(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    template_name = models.CharField(max_length=64)
    def __unicode__(self):
        return '%s' %(self.name)
    
class AppOpt_Role_rel(models.Model):
    role = models.ForeignKey(SysRole)
    publish = models.BooleanField(default=False)
    stop = models.BooleanField(default=False)
    start = models.BooleanField(default=False)
    reboot = models.BooleanField(default=False)
    scale = models.BooleanField(default=False)
    undeploy = models.BooleanField(default=False)
    connect = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.role)
    
    
    

class AssetHost(models.Model):
    host_status = (
                   (1,u'在线'),
                   (2,u'离线'),
                   )
    operate_status = (
                      (1,u'运营中'),
                      (2,u'维护中'),
                      (3,u'已下线')
                      )
    private_ip = models.GenericIPAddressField(unique=True,verbose_name='私网IP')#1L
    port = models.IntegerField(verbose_name='端口')
    host_status = models.IntegerField(choices=host_status,verbose_name='状态')
    remote_user = models.CharField(max_length=32,verbose_name='远程帐号')
    remote_passwd = models.CharField(max_length=64,verbose_name='用户密码')
    agent_is_install = models.BooleanField(default=False,verbose_name='agent已安装')
    
    serial = models.CharField(max_length=64,null=True, blank=True,verbose_name='序列号')
    hostname = models.CharField(max_length=32,null=True,blank=True,verbose_name='主机名')
    public_ip = models.GenericIPAddressField(null=True, blank=True,verbose_name='公网IP')
    cpu_no = models.IntegerField(null=True, blank=True,verbose_name='CPU核数')
    cpu_model = models.CharField(max_length=128,null=True, blank=True,verbose_name='CPU型号')
    memory = models.IntegerField(null=True, blank=True,verbose_name='物理内存')
    disk = models.FloatField(null=True, blank=True,verbose_name='磁盘容量')
    os = models.CharField(max_length=64,null=True, blank=True,verbose_name='操作系统')
    kernel =models.CharField(max_length=64,null=True, blank=True,verbose_name='内核版本')
    machine_model = models.CharField(max_length=32,null=True, blank=True,verbose_name='机器型号')
    
    position = models.CharField(max_length=64,null=True, blank=True,verbose_name='位置信息')
    group = models.ForeignKey('HostGroup',on_delete=models.PROTECT,verbose_name='主机组')
    operate_status = models.IntegerField(choices=operate_status,null=True, blank=True,verbose_name='运营状态')
    department = models.CharField(max_length=64,null=True, blank=True,verbose_name='使用部门')#20L
    owner = models.ForeignKey('SysUser')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    
    def get_maintainer(self):
        return HostGroup.objects.get(id=self.group_id).maintainer
    
    def __unicode__(self):
        return '%s' %(self.private_ip)
    
class HostEvent(models.Model):
    actions = (
                   (1,u'代理安装'),
                   (2,u'规格信息收集'),
                   (3,u'规格信息刷新'),
                   )
    host = models.ForeignKey('AssetHost')
    action = models.IntegerField(choices=actions)
    is_succeeded = models.BooleanField(default=False)
    content = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' %(self.action)
    
class HostImport(models.Model):
    filename = models.CharField(max_length=16,verbose_name="文件名")
    total_line = models.IntegerField(default=0,verbose_name="行数")
    succeeded_line = models.IntegerField(default=0,verbose_name="处理成功")
    failure_line = models.IntegerField(default=0,verbose_name="处理失败")
    err_line = models.CharField(max_length=64,null=True,blank=True,verbose_name="错误行号")
    err_msg = models.TextField(null=True,blank=True,verbose_name="错误信息")
    is_finished = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' %(self.filename)
    
class HostAccount(models.Model):
    userStatus = (
                  (1,'正常'),
                  (2,'锁定')
                  )
    host = models.ForeignKey(AssetHost)
    account = models.CharField(max_length=16)
    passwd = models.CharField(max_length=32,null=True,blank=True)
    last_password_change = models.CharField(max_length=16,null=True,blank=True)
    password_expires = models.CharField(max_length=16,default='Never')
    account_expires = models.CharField(max_length=16,default='Never')
    status = models.IntegerField()
    msg = models.CharField(max_length=32,null=True,blank=True)


class HostGroup(models.Model):
    name = models.CharField(max_length=32,verbose_name='主机组')
    description = models.CharField(max_length=64,verbose_name='备注')
    maintainer = models.CharField(max_length=32,verbose_name='运维人员')
    tel = models.CharField(max_length=11,verbose_name='电话')
    email = models.CharField(max_length=32,verbose_name='邮箱')
    def hosts(self):
        return len(AssetHost.objects.filter(group_id=self.id))
    def __unicode__(self):
        return '%s' %(self.name)
    
class Enterprise(models.Model):
    pass

class ScriptModel(models.Model):
    scriptType = (
                  (1,'bash'),
                  (2,'python'),
                  (3,'perl')
                  )
    scriptFrom = (
                  (1,'手动录入'),
                  (2,'本地导入'),
                  (3,'已有脚本')
                  )
    name = models.CharField(unique=True,max_length=64)
    script_type = models.IntegerField(choices=scriptType,default=1)
    script_from = models.IntegerField(choices=scriptFrom,default=1)
    script_file = models.CharField(max_length=64)
    script_owner = models.ForeignKey('SysUser')
    total_run_count = models.IntegerField(default=0,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
    
class TaskLog(models.Model):
    taskType = (
                (1,'脚本执行'),
                (2,'Ansible'),
                (3,'快速工具')
                )
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    task_name = models.CharField(max_length=32,verbose_name='名称')
    task_type = models.IntegerField(choices=taskType,verbose_name='类型')
    host_no = models.IntegerField(verbose_name='主机数量')
    finish_no = models.IntegerField(verbose_name='已完成')
    failure_no = models.IntegerField(verbose_name='失败')
    execute_owner = models.ForeignKey('SysUser')
    script_file = models.CharField(max_length=64)
    execute_time = models.DateTimeField(auto_now=True,verbose_name='执行时间')

class TaskHost(models.Model):
    executeStatus = (
                     (1,'成功'),
                     (2,'失败')
                     )
    task_id = models.CharField(max_length=8,verbose_name='任务ID')
    host_ip = models.GenericIPAddressField(verbose_name='主机IP')
    host_account = models.CharField(max_length=10,verbose_name='帐号')
    execute_status = models.IntegerField(choices=executeStatus)
    
class AnsibleModel(models.Model):
    scriptFrom = (
                  (1,'手动录入'),
                  (2,'本地导入'),
                  (3,'已有脚本')
                  )
    name = models.CharField(unique=True,max_length=64)
    script_from = models.IntegerField(choices=scriptFrom)
    script_file = models.CharField(max_length=64)
    script_owner = models.ForeignKey('SysUser')
    total_run_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    
class CmdTemplate(models.Model):
    temp_type = (
                 (1,'playbook'),
                 )
    name = models.CharField(max_length=32,verbose_name='剧本名')
    type = models.IntegerField(choices=temp_type,verbose_name='类型')
    owner = models.ForeignKey('SysUser',verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    description = models.CharField(max_length=32,verbose_name='说明')
    detail = models.TextField(verbose_name='详情')

class PaasHost(models.Model):
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    label = models.CharField(max_length=16,verbose_name='备注')
    
    def __unicode__(self):
        return '%s' %(self.ip)
    
    
class MesosCluster(models.Model):
    c_status = (
                (1,'health'),
                (2,'warning'),
                (3,'danger')
                )
    name = models.CharField(max_length=32,verbose_name='名称')
    master_nodes = models.IntegerField(verbose_name='管理节点')
    slave_nodes = models.IntegerField(verbose_name='计算节点')
    haproxy_nodes = models.IntegerField(verbose_name='Haproxy节点')
    cpu_used = models.FloatField(verbose_name='CPU使用核数')
    cpu_total = models.FloatField(verbose_name='CPU总核数')
    memory_used = models.FloatField(verbose_name='已使用内存')
    memory_total = models.FloatField(verbose_name='内存总量')
    disk_used = models.FloatField(verbose_name='已使用存储')
    disk_total = models.FloatField(verbose_name='存储总量')
    status = models.IntegerField(choices=c_status,verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    provider = models.CharField(max_length=32,verbose_name='供应商')
    def __unicode__(self):
        return '%s' %(self.name)
    
class MesosMaster(models.Model):
    m_status = (
                (1,'health'),
                (2,'warning'),
                (3,'danger')
                )
    cluster = models.ForeignKey('MesosCluster',verbose_name='集群')
    version = models.CharField(max_length=32,verbose_name='版本')
    image = models.CharField(max_length=128,verbose_name='镜像')
    hosts = models.ManyToManyField('PaasHost',verbose_name='主机')
    leader = models.GenericIPAddressField(verbose_name='leader地址')
    port = models.IntegerField(verbose_name='端口')
    zk = models.CharField(max_length=255,verbose_name='ZK地址')
    log_dir = models.CharField(max_length=255,verbose_name='日志目录')
    work_dir = models.CharField(max_length=255,verbose_name='工作目录')
    documentation = models.CharField(max_length=255,verbose_name='参考链接')
    status = models.IntegerField(choices=m_status,verbose_name='状态')
    def hosts_list(self):
        return ', '.join([a.ip for a in self.hosts.all()])
    
    def __unicode__(self):
        return '%s' %(self.cluster)


    
    