# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# from webapp.models import PaasHost,MesosMaster,MesosCluster

# Register your models here.

# class PaasHostAdmin(admin.ModelAdmin):
#     list_display = ('ip','label')
#     list_editable = ['label']
#     
# class MesosClusterAdmin(admin.ModelAdmin):
#     list_display = ('name','master_nodes','slave_nodes','haproxy_nodes','cpu_used','cpu_total')
#     
# class MesosMasterAdmin(admin.ModelAdmin):
#     list_display = ('cluster','version','image','hosts_list','leader')
#     
#     
#     
# admin.site.register(PaasHost, PaasHostAdmin)
# admin.site.register(MesosCluster, MesosClusterAdmin)
# admin.site.register(MesosMaster, MesosMasterAdmin)