#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月4日 下午12:39:29
@author: yangxu
'''
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView,DeleteView
from webapp.models import RepositoryHost,RepositoryImage
from .forms import RepositoryHostForm
from django.http import JsonResponse
from utils.dockerhubv2api import DockerHubV2
import docker

#docker.DockerClient(base_url='http://192.168.10.3:6071')

class RepositoryHostList(ListView):
    model = RepositoryHost
    context_object_name = 'repoHosts'
    template_name = 'paas/repository/RepoHostList.html'

class RepositoryHostAdd(FormView):
    form_class = RepositoryHostForm
    template_name = 'paas/repository/RepoHostList.html'
    success_url = reverse_lazy('RepositoryHostList')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class RepositoryHostDelete(DeleteView):
    model = RepositoryHost
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('RepositoryHostList')
    template_name = 'paas/repository/RepoHostList.html'

def repositor_refresh(request):
    if request.method == 'POST':
        repo_host_id =  int(request.POST.get('id'))
        repoObj = RepositoryHost.objects.get(id=repo_host_id)
        ip = repoObj.ip
        port = repoObj.port
        label = repoObj.label
        try:
            dockhubObj = DockerHubV2(ip,port)
        except Exception as e:
            msg = str(e)
            repoObj.status = 2
            return JsonResponse({'code':400,'status':2,'msg':msg})
        else:
            imageinfolisttmp = getimagelist(ip,dockhubObj,dockhubObj.getImageTagList())
            image_num = len(imageinfolisttmp)
            repoObj.image_num = image_num
            RepositoryImage.objects.filter(ip_port=ip+':'+str(port)).delete()
            for image in imageinfolisttmp:
                RepositoryImage.objects.create(image_name=image['imagename'],image_id=image['imageid'],
                                           docker_version=image['imagedockerversion'],ip_port=ip+':'+str(port),label=label,
                                           image_size=image['imagesize'],create_time=image['imagetime'])
        repoObj.save()
        return JsonResponse({'code':200,'status':1,'num':image_num})

def getimagelist(imagehost,instance,imagetag_list):
    imageinfolist = []
    for i in range(len(imagetag_list)):
        for imagename,imageversion in imagetag_list[i].items():
            one_image_info_dict = {'imagehost':imagehost}
            size_id_time_version = instance.countImageSizeAndId(imagename,imageversion)
            one_image_info_dict["imagename"] = imagename+":"+imageversion
            one_image_info_dict["imagesize"] = size_id_time_version["imagesize"]
            one_image_info_dict["imageid"] = size_id_time_version["imageid"]
            one_image_info_dict["imagetime"] = size_id_time_version["imagetime"]
            one_image_info_dict["imagedockerversion"] = size_id_time_version["imagedockerversion"]
        imageinfolist.append(one_image_info_dict)
    return imageinfolist

class RepositoryImageList(ListView):
    model = RepositoryImage
    context_object_name = 'repoImages'
    template_name = 'paas/repository/RepoImageList.html'
    