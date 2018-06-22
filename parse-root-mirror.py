#!/usr/bin/env 
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
        #r = requests.get(rooturl)
        #with open(rootyaml,"wb") as f:
        #    f.write(r.content)
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
    return allX 
   

def parCountry(filedict):
    contrylist =[]
    n = []
    for k,v in filedict.items():
        m = {}
        for l in v:
            if 'Country' not in l.keys():
                continue 
            contrylist.append(l['Country'])
            count_frq = {}
            for item in contrylist:
                if item in count_frq:
                    count_frq[item] += 1
                else:
                    count_frq[item] =1
                m['contry']=count_frq
                m['loc']=len(contrylist)
                m['root'] = k
        #n.append(m)
        print m
    #print n
    return  n 


def overall(allX)
    '''
    所有yml文件整体结果进行分析
    ①：根镜像节点总数（会出现US USA，需要有一个国家代码表来转换）
    ②：每个国家town数，而不是节点数，有可能一个town有多个site
    ③：
    '''

def contryX():
    '''
    入口是一个国家简写，输出这个国家的节点数，包括Global和Local
    '''



if __name__ == '__main__':
    curdir = os.path.split(os.path.realpath(__file__))[0]
    localdir = os.path.join(curdir,'rootfile2')
    #DownYaml(rootdict,localdir)
    filelist = os.listdir(localdir)
    print filelist  #['a-root.yml','b-root.yml']
    ParYaml(localdir,filelist)
    #filepath='E:\\personal-study\\python\\pythonscripts\\rootfile\\m-root.yml'
    #filedict = ParYaml(filepath)
    #m=parCountry(filedict)
