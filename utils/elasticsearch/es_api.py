#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月10日
@author: yangxu
'''
import httplib
import json
from index_mapping import cpu_mapping
from query_condition import generate_condition_data

class IndexApi(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(self.host,self.port)
    
    def create(self,index_name):
        body = json.dumps(cpu_mapping)
        url_context = '/'+index_name
        try:
            self.conn.request('PUT', url_context, body, {'Content-Type': 'application/json'})
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
    
    def delete(self,index_name):
        url_context = '/'+index_name
        try:
            self.conn.request('DELETE', url_context)
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
        
    def get(self,index_name):
        url_context = '/'+index_name
        try:
            self.conn.request('GET', url_context)
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}

class DocumentApi(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(self.host,self.port)
    
    def create(self,index_name,doc_type,doc_id,doc_body):
        if doc_id:
            url_context = '/{}/{}/{}'.format(index_name,doc_type,doc_id)
        else:
            url_context = '/{}/{}'.format(index_name,doc_type)
        body=json.dumps(doc_body)
        try:
            self.conn.request('POST', url_context, body, {'Content-Type': 'application/json'})
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
        
    def get(self,index_name,doc_type,doc_id):
        url_context = '/{}/{}/{}'.format(index_name,doc_type,doc_id)
        try:
            self.conn.request('GET', url_context)
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
            
    def mget(self,index_name,doc_type,doc_body):
        body = json.dumps(doc_body)
        url_context = '/{}/{}/_mget'.format(index_name,doc_type)
        try:
            self.conn.request('GET', url_context, body, {'Content-Type': 'application/json'})
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
        
    def search(self,index_name,doc_type,host,time_value):
        body = json.dumps(generate_condition_data(host,time_value))
        url_context = '/{}/{}/_search'.format(index_name,doc_type)
        try:
            self.conn.request('GET', url_context, body, {'Content-Type': 'application/json'})
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
    
    def delete(self,index_name,doc_type):
        doc_body = {
                    "query": {
                    "match_all": {}
                    }
                    }
        
        url_context = '/{}/{}/_delete_by_query'.format(index_name,doc_type)
        body=json.dumps(doc_body)
        try:
            self.conn.request('POST', url_context, body, {'Content-Type': 'application/json'})
        except Exception as e:
            print e
        else:
            httpres = self.conn.getresponse()
            return {'code':httpres.status,'result':httpres.read()}
        
            
        
# obj = IndexApi('192.168.10.3',9200)
# print obj.delete('dcos')
# print obj.create('dcos')


# obj = DocumentApi('192.168.10.3',9200)
# doc_body = {'host' : 'glance',
#             'timestamp' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             'usage' : 0.28,
#             'iowait' : 0.00}

# print obj.create(index_name='dcos', doc_type='cpu', doc_id=4, doc_body=doc_body)
# print obj.search(index_name='dcos', doc_type='cpu', second_condition=condition_data)

# Time = (json.loads(obj.get(index_name='dcos', doc_type='cpu', doc_id=3)['result'])['_source']['timestamp'])
# print Time 
# print (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
