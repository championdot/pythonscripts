#!/usr/bin/env python
#coding: utf-8

import string
import yaml 
import sys
import urllib
import os
from collections import Counter

rootdict={}
for i in range(97,110):
    a=('http://www.root-servers.org/download/%s-root.yml' %chr(i))
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
            #x['Instances'] is list
        allX.append(filedict) 
    #print allX  
    return allX 


if __name__ == '__main__':
    curdir = os.path.split(os.path.realpath(__file__))[0]
    localdir = os.path.join(curdir,'rootfile2')
    #DownYaml(rootdict,localdir)
    filelist = os.listdir(localdir)

    #正式执行
    allinfolist=ParYaml(localdir,filelist)
    with open('country-sites.txt','w') as f:
        for i in allinfolist:
            allinfo=i['info']
            #print i['filename']
            #f.write(i['filename'])
            for infodict in allinfo:
                if 'Country' not in infodict.keys():
                    infodict['Country']=infodict['Town']
                #f.write( i['filename'].split('.')[0].split('-')[0],infodict['Country'],infodict['Sites'] )
                print  i['filename'].split('.')[0].split('-')[0],infodict['Country'],infodict['Sites'],infodict['Type'],infodict['IPv4'],infodict['IPv6']