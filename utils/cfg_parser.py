#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2017年11月19日

@author: yangxu
'''
from ConfigParser import ConfigParser

'''
在使用python2 configparser读取配置文件的时候，发现没法保留配置文件大小写，进行重写optionxform
'''
# class myconf(configparser):  
#     def __init__(self,defaults=None):  
#         configparser.__init__(self,defaults=None)  
#     def optionxform(self, optionstr):  
#         return optionstr

class confParse(object):  
  
    def __init__(self,conf_path):  
        self.conf_path = conf_path  
        self.conf_parser = ConfigParser()
        self.conf_parser.read(conf_path)  
  
    def get_sections(self):
        return self.conf_parser.sections()  
  
    def get_options(self,section):  
        return self.conf_parser.options(section)  
  
    def get_items(self,section):  
        return self.conf_parser.items(section)  
  
    def get_val(self,section,option,is_bool = False,is_int = False):  
        if is_bool and not is_int:  
            #bool类型配置  
            val = self.conf_parser.getboolean(section,option)  
            return val  
        elif not is_bool and is_int:  
            val = self.conf_parser.getint(section,option)  
            return val  
  
        val = self.conf_parser.get(section,option)  
        return val
    def add_section(self,section):
        self.conf_parser.add_section(section)
        self.conf_parser.write(open(self.conf_path,"w"))
    def set_option(self,section,option,value):
        self.conf_parser.set(section, option, value)
        self.conf_parser.write(open(self.conf_path,"w"))
