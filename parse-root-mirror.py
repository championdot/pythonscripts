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
    #print allX  
    return allX 
   

def parX(allinfolist,X):
    '''
    想做到如果想看某一个根的情况，如果不传rootlist，就代表是全部根的
    X代表的是某个字段，比如根据国家Country,Type(Global 还是Local),
    [
        {
            'filename':'a-root.yml',
            'info':     [{Country:CN,TOWN:CN},{Country:CN,TOWN:CN}]
        },
        {
            'filename':'b-root.yml',
            'info':     [{Country:CN,TOWN:CN},{Country:CN,TOWN:CN}]
        }
        ]
    '''
    alltotal = []
    for root in allinfolist:
        total = {}
        Xlist =[]
        for infolist in root['info']:
            if X in infolist.keys():
                Xlist.append(infolist[X])
        count_frq ={}
        for item in Xlist:
            if item in count_frq:
                count_frq[item] += 1
            else:
                count_frq[item] =1
        cc = []
        for contrydata in count_frq.values():
            cc.append(contrydata)
        total['filename']=root['filename']
        if X=='Sites':
            total['nodesitecount']=sum(Xlist)
        else:
        #elif: X =='Country':
            total['Xlistcount']=count_frq
            #total['locnt']
        total['loccnt'] = sum(cc)
        print total
        alltotal.append(total)
    return alltotal

def overall(allX,filelist):
    '''
    所有yml文件整体结果进行分析
    ①：根镜像节点总数（会出现US USA，需要有一个国家代码表来转换）
    ②：每个国家town数，而不是节点数，有可能一个town有多个site
    ③：
    '''
    d3 =[]
    for filename in filelist:
        for allinfo in allX:
            if filename == allinfo['filename']:
                d2 = allinfo['Xlistcount']
                d3.append(d2)
    d4 = {}
    for i in d3:
        for k,v in i.items():
            if k in d4.keys():
                d4[k] += v
            else:
                d4[k] = v
    print d4
def contryX():
    '''
    入口是一个国家简写，输出这个国家的节点数，包括Global和Local
    '''



if __name__ == '__main__':
    curdir = os.path.split(os.path.realpath(__file__))[0]
    localdir = os.path.join(curdir,'rootfile2')
    #DownYaml(rootdict,localdir)
    filelist = os.listdir(localdir)
    #print filelist  #['a-root.yml','b-root.yml']
    #filepath='E:\\personal-study\\python\\pythonscripts\\rootfile\\m-root.yml'
    #filedict = ParYaml(filepath)
    #m=parCountry(filedict)

    #正式执行
    allinfolist=ParYaml(localdir,filelist)
    #print allinfolist
    #parX(allinfolist,'Town')
    print '#####'
    alltotal=parX(allinfolist,'Country')
    #print '#######'
    #print alltotal
    hx={}
    for l in alltotal:
        lx=l['Xlistcount']
        hx.update(lx)
        X,Y = Counter(lx),Counter(hx)
        hx = dict(X+Y)
    print hx
    #parX(allinfolist,'Sites')
    #print '######'
    #parX(allinfolist,'State')
    #parX(allinfolist,'Type')
    #overall(allinfolist,filelist)
    #parX(allinfolist,'IPv4')
    #parX(allinfolist,'IPv6')  
