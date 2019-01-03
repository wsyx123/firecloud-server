#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2017年12月26日

@author: yangxu
'''
import httplib
import json
from types import ListType
import datetime

class DockerHubV2(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def getImageAll(self):
        conn = httplib.HTTPConnection(self.host,self.port)
        url_context="/v2/_catalog"
        conn.request("GET", url_context)
        httpres = conn.getresponse()
        return json.loads(httpres.read())['repositories']
    
    def getImageTagList(self):
        image_tag_list = []
        imagenames = self.getImageAll()
        conn = httplib.HTTPConnection(self.host,self.port)
        if type(imagenames) is ListType:
            for name in imagenames:
                url_context="/v2/{}/tags/list".format(name)
                conn.request("GET", url_context)
                httpres = conn.getresponse()
                one_image_json = json.loads(httpres.read())
                one_image_tags_list = one_image_json["tags"]
                for i in range(len(one_image_tags_list)):
                    one_image_info_dict = {}
                    one_image_info_dict[name] = one_image_tags_list[i]
                    image_tag_list.append(one_image_info_dict)
        return image_tag_list
    
    def countImageAmount(self):
        count_list = self.getImageTagList()
        return len(count_list)

    def countImageSizeAndId(self,imagename,imageversion):
        imagename = imagename
        imageversion = imageversion
        headers = {"Accept":" application/vnd.docker.distribution.manifest.v2+json"}
        conn = httplib.HTTPConnection(self.host,self.port)
        url_context="/v2/{}/manifests/{}".format(imagename, imageversion)
        conn.request("GET", url_context,headers=headers)
        httpres = conn.getresponse()
        result = json.loads(httpres.read())
        imageId = result['config']['digest'].split(":")[1][0:12]
        imageTime = self.getImageCreateTime(imagename, imageversion)
        imageDockerVersion = self.getImageDockerVersion(imagename, imageversion)
        imageSize = 0
        for i in range(len(result['layers'])):
            imageSize = imageSize + result['layers'][i]['size']
        imageSize = str(round((float(imageSize)/1024/1024),1))+'MB'
        return {'imageid':imageId,'imagesize':imageSize,'imagetime':imageTime,'imagedockerversion':imageDockerVersion}
    
    def getImageCreateTime(self,imagename,imageversion):
        imagename = imagename
        imageversion = imageversion
        conn = httplib.HTTPConnection(self.host,self.port)
        url_context="/v2/{}/manifests/{}".format(imagename, imageversion)
        conn.request("GET", url_context)
        httpres = conn.getresponse()
        result = json.loads(httpres.read())
        utc_datetimeobj = datetime.datetime.strptime(str(json.loads(result['history'][0]['v1Compatibility'])['created']).split('.')[0],'%Y-%m-%dT%H:%M:%S')
        cst_datetimeobj = utc_datetimeobj + datetime.timedelta(hours=8)
        return str(cst_datetimeobj)
    
    def getImageDockerVersion(self,imagename,imageversion):
        imagename = imagename
        imageversion = imageversion
        conn = httplib.HTTPConnection(self.host,self.port)
        url_context="/v2/{}/manifests/{}".format(imagename, imageversion)
        conn.request("GET", url_context)
        httpres = conn.getresponse()
        result = json.loads(httpres.read())
        return (json.loads(result['history'][0]['v1Compatibility'])['docker_version'])
        

# instance = dockerhubv2('192.168.10.3', '5000')
# instance.countImageSize()        
# namelist = getImageAll('192.168.10.3', '5000')
# result = getImageTagList('192.168.10.3', '5000',namelist)
# print result