#!/usr/bin/python
# _*_ coding : UTF-8 _*_
'''
@author: yangxu
'''
import os,sys
root_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

ASSET_IMPORT_PATH=root_dir+'/static/upload'

SCRIPT_SAVE_PATH=root_dir+'/static/upload/scripts'

SCRIPT_PICKLE_PATH=root_dir+'/static/upload/pickle'

ANSIBLE_PROJECT_PATH=root_dir+'/static/upload/ansible'

FILE_DISTRIBUTE_PATH=root_dir+'/static/upload/file'
PUBLIC_FILE_PATH = root_dir+'/static/upload/public_file'