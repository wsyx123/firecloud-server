#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月13日 下午2:30:57
@author: yangxu
'''

import socket
from docker import DockerClient
from datetime import datetime

class MesosDeploy():
    def __init__(self,clsObj,deploy_model):
        self.clsObj = clsObj
        self.master_host_list = clsObj.masterDeploy.split(',')
        self.marathon_host_list = clsObj.marathonDeploy.split(',')
        self.haproxy_host_list = clsObj.haproxyDeploy.split(',')
        self.slave_host_list = clsObj.slaveDeploy.split(',')
        self.deploy_model = deploy_model
        
    
    def get_cluster_all_host(self):
        # return a tuple of all host
        all_host_list = self.master_host_list + self.marathon_host_list\
                        + self.haproxy_host_list + self.slave_host_list
        return set(all_host_list)
    
    def get_cluster_all_image(self):
        '''
        return [
                {'image':'master','hosts':[]},
                ]
        '''
        image_list = []
        image_list.append({'image':self.clsObj.masterImage,'hosts':self.master_host_list})
        image_list.append({'image':self.clsObj.zkImage,'hosts':self.master_host_list})
        image_list.append({'image':self.clsObj.marathonImage,'hosts':self.marathon_host_list})
        image_list.append({'image':self.clsObj.haproxyImage,'hosts':self.haproxy_host_list})
        image_list.append({'image':self.clsObj.slaveImage,'hosts':self.slave_host_list})

        return image_list
        
    
    def check_con(self,deploy_obj):
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        err_host = []
        for host in self.get_cluster_all_host():
            result = s.connect_ex((host,6071))
            if result == 0:
                continue
            else:
                err_host.append(host)
        if len(err_host) != 0:
            deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            deploy_obj.status = 4
            deploy_obj.msg = ','.join(err_host)+'端口:6071 连接失败!'
            deploy_obj.save()
            return False
        else:
            deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            deploy_obj.status = 3
            deploy_obj.save()
            return True
    
    def img_download(self,deploy_obj):
        for item in self.get_cluster_all_image():
            img = item['image']
            hosts = item['hosts']
            download_result = self.download(img, hosts)
            if not download_result['status']:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = download_result['msg']
                deploy_obj.save()
                return False
        deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deploy_obj.status = 3
        deploy_obj.save()
        return True
            
    
    def download(self,img,hosts):
        status_dict = {'status':True}
        for host in hosts:
            base_url = "http://{}:6071".format(host)
            sock = DockerClient(base_url=base_url)
            try:
                sock.images.pull(img)
            except Exception as e:
                msg = str(e)
                status_dict['msg'] = "{} download {} fail:{}".format(host,img,msg)
                status_dict['status'] = False
        return status_dict
                
    def create_container(self,deploy_obj,step_name):
        if step_name == "deployZK":
            return self.deploy_zookeeper(deploy_obj)
        elif step_name == 'deployMaster':
            return self.deploy_master(deploy_obj)
        elif step_name == 'deployMT':
            return self.deploy_marathon(deploy_obj)
        elif step_name == 'deployHA':
            return self.deploy_haproxy(deploy_obj)
        elif step_name == 'deploySlave':
            return self.deploy_slave(deploy_obj)
        else:
            return False
            
    def deploy_zookeeper(self,deploy_obj):
        self.zookeeper_env = ['ZOO_INIT_LIMIT=10',
                         'ZOO_TICK_TIME=3000',
                         'ZOO_INIT_LIMIT=5',
                         'ZOO_SYNC_LIMIT=2',
                         'ZOO_MAX_CLIENT_CNXNS=60',
                         'ZOO_ADMIN_ENABLESERVER=false']
        img = self.clsObj.zkImage
        hosts = self.master_host_list
        ZOO_SERVERS = ''
        for i in range(len(hosts)):
            ZOO_SERVERS = ZOO_SERVERS + "server.{}={}:2888:3888:participant;0.0.0.0:2181 ".format(i+1,hosts[i])
            
        for i in range(len(hosts)):
            zookeeper_env = self.zookeeper_env
            ZOO_MY_ID = "ZOO_MY_ID={}".format(i+1)
            zookeeper_env.append("ZOO_SERVERS={}".format(ZOO_SERVERS))
            zookeeper_env.append(ZOO_MY_ID)
            base_url = "http://{}:6071".format(hosts[i])
            sock = DockerClient(base_url=base_url)
            try:
                sock.containers.run(self, img,detach=True,
                                    name='mesos-zookeeper',
                                    user='root',
                                    tty=True,
                                    stderr=True,
                                    stdout=True,
                                    environment=zookeeper_env,
                                    network_mode='host',
                                    restart_policy='always')
            except Exception as e:
                msg = str(e)
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = msg
                deploy_obj.save()
                return False
            else:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 3
                deploy_obj.save()
                return True
            
    def deploy_master(self,deploy_obj):
        img = self.clsObj.masterImage
        hosts = self.master_host_list
        mesos_zk = 'zk://'
        for i in range(len(hosts)):
            if i == len(hosts) - 1:
                mesos_zk = mesos_zk + hosts[i]+':2181/'+self.clsObj.clusterName
            else:
                mesos_zk = mesos_zk + hosts[i]+':2181,'
        MESOS_ZK = "MESOS_ZK={}".format(mesos_zk)
        MESOS_CLUSTER = "MESOS_CLUSTER={}".format(self.clsObj.clusterName)
        MESOS_HOSTNAME_LOOKUP = "MESOS_HOSTNAME_LOOKUP=false"
        for i in range(len(hosts)):
            MESOS_HOSTNAME = "MESOS_HOSTNAME={}".format(hosts[i])
            MESOS_IP = "MESOS_IP={}".format(hosts[i])
            MESOS_QUORUM = "MESOS_QUORUM={}".format(len(hosts)/2+1)
            
            base_url = "http://{}:6071".format(hosts[i])
            sock = DockerClient(base_url=base_url)
            try:
                sock.containers.run(self, img,detach=True,
                                    name='mesos-master',
                                    user='root',
                                    tty=True,
                                    stderr=True,
                                    stdout=True,
                                    environment=[MESOS_ZK,MESOS_CLUSTER,MESOS_HOSTNAME,
                                                 MESOS_HOSTNAME_LOOKUP,MESOS_IP,MESOS_QUORUM],
                                    network_mode='host',
                                    restart_policy='always')
            except Exception as e:
                msg = str(e)
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = msg
                deploy_obj.save()
                return False
            else:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 3
                deploy_obj.save()
                return True
            
    
    def deploy_marathon(self,deploy_obj):
        img = self.clsObj.marathonImage
        hosts = self.marathon_host_list
        marathon_zk = 'zk://'
        for i in range(len(hosts)):
            if i == len(hosts) - 1:
                marathon_zk = marathon_zk + hosts[i]+':2181/'+self.clsObj.marathonID
            else:
                marathon_zk = marathon_zk + hosts[i]+':2181,'
        MARATHON_ZK = "MARATHON_ZK={}".format(marathon_zk)
        MARATHON_MASTER = "MARATHON_MASTER={}".format(self.clsObj.marathonZK)
        MARATHON_EVENT_SUBSCRIBER = "MARATHON_EVENT_SUBSCRIBER=http_callback"
        for i in range(len(hosts)):
            MARATHON_HOSTNAME = "MARATHON_HOSTNAME={}".format(hosts[i])
            MARATHON_HTTP_ADDRESS = "MARATHON_HTTP_ADDRESS={}".format(hosts[i])
            MARATHON_HTTPS_ADDRESS = "MARATHON_HTTPS_ADDRESS={}".format(hosts[i])
            
            base_url = "http://{}:6071".format(hosts[i])
            sock = DockerClient(base_url=base_url)
            try:
                sock.containers.run(self, img,detach=True,
                                    name='mesos-marathon',
                                    user='root',
                                    tty=True,
                                    stderr=True,
                                    stdout=True,
                                    environment=[MARATHON_ZK,MARATHON_MASTER,MARATHON_EVENT_SUBSCRIBER,
                                                 MARATHON_HOSTNAME,MARATHON_HTTP_ADDRESS,MARATHON_HTTPS_ADDRESS],
                                    network_mode='host',
                                    restart_policy='always')
            except Exception as e:
                msg = str(e)
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = msg
                deploy_obj.save()
                return False
            else:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 3
                deploy_obj.save()
                return True
     
    def deploy_haproxy(self,deploy_obj):
        #https://github.com/QubitProducts/bamboo
        img = self.clsObj.haproxImage
        hosts = self.haproxy_host_list
        zk_hosts = self.master_host_list
        servicePort = self.clsObj.servicePort
        statusPort = self.clsObj.statusPort
        bambooPort = self.clsObj.bambooPort
        map_port = {'{}/tcp'.format(bambooPort):bambooPort,
                    '{}/tcp'.format(servicePort):servicePort,
                    '{}/tcp'.format(statusPort):statusPort}
        bamboo_zk_host = ''
        for i in range(len(zk_hosts)):
            if i == len(zk_hosts) - 1:
                bamboo_zk_host = bamboo_zk_host + zk_hosts[i]+':2181'
            else:
                bamboo_zk_host = bamboo_zk_host + zk_hosts[i]+':2181,'
        BAMBOO_ZK_HOST = "BAMBOO_ZK_HOST={}".format(bamboo_zk_host)
        BAMBOO_ZK_PATH = "/"+self.clsObj.haproxyID
        MARATHON_ENDPOINT = self.clsObj.haproxyMarathon
        BIND = "BIND=:{}".format(bambooPort)
        CONFIG_PATH = "CONFIG_PATH=config/production.example.json"
        BAMBOO_DOCKER_AUTO_HOST = "BAMBOO_DOCKER_AUTO_HOST=true"
        for i in range(len(hosts)):
            BAMBOO_ENDPOINT = "BAMBOO_ENDPOINT=http://{}:{}".format(hosts[i],bambooPort)
            base_url = "http://{}:6071".format(hosts[i])
            sock = DockerClient(base_url=base_url)
            try:
                sock.containers.run(self, img,detach=True,
                                    name='haproxy-bamboo',
                                    user='root',
                                    tty=True,
                                    stderr=True,
                                    stdout=True,
                                    ports=map_port,
                                    environment=[BAMBOO_ZK_HOST,BAMBOO_ZK_PATH,MARATHON_ENDPOINT,
                                                 BIND,CONFIG_PATH,BAMBOO_DOCKER_AUTO_HOST,BAMBOO_ENDPOINT],
                                    network_mode='host',
                                    restart_policy='always')
            except Exception as e:
                msg = str(e)
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = msg
                deploy_obj.save()
                return False
            else:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 3
                deploy_obj.save()
                return True
            
    def deploy_slave(self,deploy_obj):
        img = self.clsObj.slaveImage
        hosts = self.slave_host_list
        MESOS_MASTER = "MESOS_MASTER={}".format(self.clsObj.slaveZK)
        MESOS_WORK_DIR = "MESOS_WORK_DIR=/data/mesos/workdir"
        MESOS_ATTRIBUTES = "MESOS_ATTRIBUTES={}".format(self.clsObj.slaveLabel)
        MESOS_SYSTEMD_ENABLE_SUPPORT = "MESOS_SYSTEMD_ENABLE_SUPPORT=false"
        for i in range(len(hosts)):
            MESOS_HOSTNAME = "MESOS_HOSTNAME={}".format(hosts[i])
            MESOS_IP = "MESOS_IP={}".format(hosts[i])
            
            
            base_url = "http://{}:6071".format(hosts[i])
            sock = DockerClient(base_url=base_url)
            try:
                sock.containers.run(self, img,detach=True,
                                    name='mesos-slave',
                                    user='root',
                                    tty=True,
                                    stderr=True,
                                    stdout=True,
                                    privileged=True,
                                    environment=[MESOS_MASTER,MESOS_WORK_DIR,MESOS_ATTRIBUTES,
                                                 MESOS_SYSTEMD_ENABLE_SUPPORT,MESOS_HOSTNAME,MESOS_IP],
                                    volumes={'/sys/fs/cgroup': {'bind': '/sys/fs/cgroup', 'mode': 'rw'},
                                             '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
                                             '/data/mesos/workdir': {'bind': '/data/mesos/workdir', 'mode': 'rw'},
                                             },
                                    network_mode='host',
                                    restart_policy='always')
            except Exception as e:
                msg = str(e)
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 4
                deploy_obj.msg = msg
                deploy_obj.save()
                return False
            else:
                deploy_obj.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deploy_obj.status = 3
                deploy_obj.save()
                return True   
        