#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2019年1月13日 下午2:30:57
@author: yangxu
'''
from docker import DockerClient
import re

def check_docker_6071(hosts):
    err_host = []
    for host in hosts:
        base_url="{}:6071".format(host)
        try:
            DockerClient(base_url=base_url)
        except:
            err_host.append(host)
        else:
            pass
    if len(err_host) != 0:
        msg = ','.join(err_host)+'端口:6071 连接失败!'
        status = False
    else:
        msg = ''
        status = True
    return {'status':status,'msg':msg,'err_host':err_host}
    
def download_img(hosts,img):
    status_dict = {'status':True}
    for host in hosts:
        base_url = "http://{}:6071".format(host)
        sock = DockerClient(base_url=base_url)
        try:
            sock.images.pull(img)
        except Exception as e:
            msg = str(e)
            status_dict['msg'] = "{} download {} Fail:{}".format(host,img,msg)
            status_dict['status'] = False
    return status_dict

def create_container(host,img,env,volume,containerName):
    base_url = "http://{}:6071".format(host)
    sock = DockerClient(base_url=base_url)
    try:
        containerObj = sock.containers.create(img,detach=True,name=containerName,user='root',
                                             tty=True,
                                             #stderr=True,stdout=True,
                                             network_mode='host',
                                             environment=env,
                                             volumes=volume,
                                             restart_policy={"Name": "always"})
    except Exception as e:
        msg = str(e)
        return {'status':False,'msg':msg}
    else:
        return {'status':True,'containerObj':containerObj}

def gen_zookeeper_env(hosts):
    zookeeper_env_dict = {}
    zookeeper_env = ['ZOO_INIT_LIMIT=10','ZOO_TICK_TIME=3000','ZOO_INIT_LIMIT=5',
                     'ZOO_SYNC_LIMIT=2',
                     'ZOO_MAX_CLIENT_CNXNS=60',
                     'ZOO_ADMIN_ENABLESERVER=false']
    ZOO_SERVERS = ''
    for i in range(len(hosts)):
        ZOO_SERVERS = ZOO_SERVERS + "server.{}={}:2888:3888:participant ".format(i+1,hosts[i])
    zookeeper_env.append("ZOO_SERVERS={}".format(ZOO_SERVERS))
    for i in range(len(hosts)):
        temp_env = zookeeper_env
        ZOO_MY_ID = "ZOO_MY_ID={}".format(i+1)
        temp_env.append(ZOO_MY_ID)
        zookeeper_env_dict[hosts[i]] = temp_env
    return zookeeper_env_dict

def gen_zookeeper_volume():
    volumes = {'/data/zookeeper/data': {'bind': '/data', 'mode': 'rw'},}
    return volumes
        
def gen_master_env(hosts,clusterName,masterPort):
    master_env_dict = {}
    mesos_zk = 'zk://'
    for i in range(len(hosts)):
        if i == len(hosts) - 1:
            mesos_zk = mesos_zk + hosts[i]+':2181/'+clusterName
        else:
            mesos_zk = mesos_zk + hosts[i]+':2181,'
    MESOS_ZK = "MESOS_ZK={}".format(mesos_zk)
    MESOS_CLUSTER = "MESOS_CLUSTER={}".format(clusterName)
    MESOS_PORT = "MESOS_PORT={}".format(masterPort)
    MESOS_LOG_DIR = "MESOS_LOG_DIR=/var/log/mesos"
    MESOS_WORK_DIR = "MESOS_WORK_DIR=/var/tmp/mesos"
    MESOS_HOSTNAME_LOOKUP = "MESOS_HOSTNAME_LOOKUP=false"
    MESOS_QUORUM = "MESOS_QUORUM={}".format(len(hosts)/2+1)
    master_env_list = [MESOS_ZK,
                       MESOS_CLUSTER,
                       MESOS_PORT,
                       MESOS_LOG_DIR,
                       MESOS_WORK_DIR,
                       MESOS_HOSTNAME_LOOKUP,
                       MESOS_QUORUM]
    for i in range(len(hosts)):
        temp_env = master_env_list
        MESOS_HOSTNAME = "MESOS_HOSTNAME={}".format(hosts[i])
        MESOS_IP = "MESOS_IP={}".format(hosts[i])
        temp_env.extend([MESOS_HOSTNAME,MESOS_IP])
        master_env_dict[hosts[i]] = temp_env
    return master_env_dict

def gen_master_volume():
    volumes = {'/data/mesos-master/log': {'bind': '/var/log/mesos', 'mode': 'rw'},
               '/data/mesos-master/workdir': {'bind': '/var/tmp/mesos', 'mode': 'rw'}}
    return volumes        

def gen_marathon_env(hosts,marathonID,masterZK):
    marathon_env_dict = {}
    #IP 地址匹配
    zk_hosts=re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b',masterZK)
    marathon_zk = 'zk://'
    for i in range(len(zk_hosts)):
        if i == len(zk_hosts) - 1:
            marathon_zk = marathon_zk + zk_hosts[i]+':2181/'+marathonID
        else:
            marathon_zk = marathon_zk + zk_hosts[i]+':2181,'
    MARATHON_ZK = "MARATHON_ZK={}".format(marathon_zk)
    #mesos master 的zookeeper node
    MARATHON_MASTER = "MARATHON_MASTER={}".format(masterZK)
    #MARATHON_EVENT_SUBSCRIBER = "MARATHON_EVENT_SUBSCRIBER=http_callback"  v1.7.50 is deprecated
    marathon_env_list = [MARATHON_ZK,MARATHON_MASTER]
    for i in range(len(hosts)):
        temp_env = marathon_env_list
        MARATHON_HOSTNAME = "MARATHON_HOSTNAME={}".format(hosts[i])
        MARATHON_HTTP_ADDRESS = "MARATHON_HTTP_ADDRESS={}".format(hosts[i])
        MARATHON_HTTPS_ADDRESS = "MARATHON_HTTPS_ADDRESS={}".format(hosts[i])
        temp_env.extend([MARATHON_HOSTNAME,MARATHON_HTTP_ADDRESS,MARATHON_HTTPS_ADDRESS])
        marathon_env_dict[hosts[i]] = temp_env
    return marathon_env_dict

def gen_marathon_volume():
    volumes = {'/data/marathon/log': {'bind': '/var/log/marathon', 'mode': 'rw'},}
    return volumes  
         
 
def gen_haproxy_env(hosts,haproxyID,bambooPort,zk_hosts,marathonEndpoint):
    #https://github.com/QubitProducts/bamboo
    bamboo_env_dict = {}
    bamboo_zk_host = ''
    for i in range(len(zk_hosts)):
        if i == len(zk_hosts) - 1:
            bamboo_zk_host = bamboo_zk_host + zk_hosts[i]+':2181'
        else:
            bamboo_zk_host = bamboo_zk_host + zk_hosts[i]+':2181,'
    BAMBOO_ZK_HOST = "BAMBOO_ZK_HOST={}".format(bamboo_zk_host)
    BAMBOO_ZK_PATH = "BAMBOO_ZK_PATH=/{}".format(haproxyID)
    MARATHON_ENDPOINT = "MARATHON_ENDPOINT={}".format(marathonEndpoint)
    MARATHON_USE_EVENT_STREAM = "MARATHON_USE_EVENT_STREAM=True"
    BIND = "BIND=:{}".format(bambooPort)
    CONFIG_PATH = "CONFIG_PATH=config/production.example.json"
    BAMBOO_DOCKER_AUTO_HOST = "BAMBOO_DOCKER_AUTO_HOST=true"
    bamboo_env_list = [BAMBOO_ZK_HOST,
                       BIND,
                       CONFIG_PATH,
                       BAMBOO_DOCKER_AUTO_HOST,
                       BAMBOO_ZK_PATH,
                       MARATHON_ENDPOINT,
                       MARATHON_USE_EVENT_STREAM]
    for i in range(len(hosts)):
        temp_env = bamboo_env_list
        BAMBOO_ENDPOINT = "BAMBOO_ENDPOINT=http://{}:{}".format(hosts[i],bambooPort)
        temp_env.append(BAMBOO_ENDPOINT)
        bamboo_env_dict[hosts[i]] = temp_env
    return bamboo_env_dict

def gen_haproxy_volume():
    volumes = {'/data/haproxy/log': {'bind': '/var/log/supervisor', 'mode': 'rw'},}
    return volumes 
        
def gen_slave_env(hosts,master_zk,slaveLabel):
    slave_env_dict = {}
    MESOS_MASTER = "MESOS_MASTER={}".format(master_zk)
    MESOS_WORK_DIR = "MESOS_WORK_DIR=/var/tmp/mesos"
    MESOS_LOG_DIR = "MESOS_LOG_DIR=/var/log/mesos"
    MESOS_CONTAINERIZERS =  "MESOS_CONTAINERIZERS=docker,mesos"
    MESOS_ATTRIBUTES = "MESOS_ATTRIBUTES=mesos:{}".format(slaveLabel)
    MESOS_SYSTEMD_ENABLE_SUPPORT = "MESOS_SYSTEMD_ENABLE_SUPPORT=false"
    slave_env_list = [MESOS_MASTER,
                      MESOS_WORK_DIR,
                      MESOS_LOG_DIR,
                      MESOS_CONTAINERIZERS,
                      MESOS_ATTRIBUTES,
                      MESOS_SYSTEMD_ENABLE_SUPPORT]
    for i in range(len(hosts)):
        temp_env = slave_env_list
        MESOS_HOSTNAME = "MESOS_HOSTNAME={}".format(hosts[i])
        MESOS_IP = "MESOS_IP={}".format(hosts[i])
        temp_env.extend([MESOS_HOSTNAME,MESOS_IP])
        slave_env_dict[hosts[i]] = temp_env
    return slave_env_dict

def gen_slave_volume():
    volumes = {'/data/mesos-slave/log': {'bind': '/var/log/mesos', 'mode': 'rw'},
               '/data/mesos-slave/workdir': {'bind': '/var/tmp/mesos', 'mode': 'rw'},
               '/sys/fs/cgroup': {'bind': '/sys/fs/cgroup', 'mode': 'rw'},
               '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}}
    return volumes


