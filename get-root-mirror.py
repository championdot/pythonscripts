#!/usr/bin/env python
#coding: utf-8

import string
import yaml 
import sys
import urllib
import os
from collections import Counter
import re
import datetime


now_time = datetime.datetime.now()
yes_time = now_time +datetime.timedelta(days=-1)
#DT= yes_time.strftime('%Y-%m-%d')
DT= now_time.strftime('%Y-%m-%d')

rootdict={}
for i in range(97,110):
    #a=('http://www.root-servers.org/download/%s-root.yml' %chr(i))
    a='http://root-servers.org/archives/%s/%s-root.yml' %(DT,chr(i))
    akey=a.split('/')[-1]
    rootdict[akey]=a

def DownYaml(rootdict,curdir):
    for  rootyaml,rooturl in rootdict.items():
        local = os.path.join(curdir,rootyaml)
        urllib.urlretrieve(rooturl,local)
        print 'download finished %s' %rootyaml

def ParYaml(localdir,filelist):
    '''
    将下载出来所有的根镜像文件进行解析成一个完整的列表数据结构
    [{'filename':'a-root.yml','info':[{},{}],'filename':'b-root.yml','info':[{},{}]}]
    '''
    allX =[]
    for file in filelist:
        filepath=os.path.join(localdir,file)
        if filepath.endswith('.yml'):
            with open(filepath,'r') as fy:
                x = yaml.load(fy)
        filedict = {}
        for k,v in x.items():
            filedict['filename']= file
            filedict['info']=x['Instances'] 
        allX.append(filedict) 
    return allX 


def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key,0) for obj in objs])
    return _total

if __name__ == '__main__':
    #dir = sys.argv[1]
    dir = DT 
    curdir = os.path.split(os.path.realpath(__file__))[0]
    localdir = os.path.join(curdir,'%s') %dir 
    isExists=os.path.exists(localdir)
    if not isExists:
        os.makedirs(localdir) 
        #DownYaml(rootdict,localdir)
    DownYaml(rootdict,localdir)
    filelist = os.listdir(localdir)
    
    #正式执行
    allinfolist=ParYaml(localdir,filelist)
    #itemdict=dict.fromkeys(['cry','st'],'')
    #t1={} 
    for i in allinfolist:
        allinfo=i['info']
        #t={}
        for infodict in allinfo:
            if 'Country' not in infodict.keys():
                infodict['Country']=infodict['Town']
            #print  i['filename'].split('.')[0].split('-')[0] +"\t"+ infodict['Country']+"\t"+infodict['Sites']+"\t"+infodict['Type']+"\t"+infodict['IPv4']+"\t"+infodict['IPv6']+"\t"+infodict['Town'].encode('utf-8')
            print  i['filename'].split('.')[0].split('-')[0],infodict['Country'],infodict['Sites'],infodict['Type'],infodict['IPv4'],infodict['IPv6'],infodict['Town'].encode('utf-8')
