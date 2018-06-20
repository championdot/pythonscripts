#!/usr/bin/env 

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
#print rootdict

def DownYaml(rootdict,curdir):
    for  rootyaml,rooturl in rootdict.items():
        print rootyaml,rooturl
        local = os.path.join(curdir,rootyaml)
        urllib.urlretrieve(rooturl,local)
        #r = requests.get(rooturl)
        #with open(rootyaml,"wb") as f:
        #    f.write(r.content)
        print 'download finished %s' %rootyaml

def ParYaml(localdir,filelist):
    filedict={}
    for file in filelist:
        filepath=os.path.join(localdir,file)
        with open(filepath,'r') as fy:
            x = yaml.load(fy)
            for k,v in x.items():
                filedict[file]= x['Instances']  #x['Instances'] is list
    return filedict 
           #{'m-root.yml':[{},{}],'j-root.yml':[{},{}]}

def parCountry(filedict):
    contrylist =[]
    m = {}
    n = []
    for k,v in filedict.items():
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
            sitecount=len(contrylist)
            m['sitecount']=sitecount
            m['contry']=count_frq 
            m['root'] = k
        n.append(m)
        print m
    #print n
    return  n 

if __name__ == '__main__':
    curdir = os.path.split(os.path.realpath(__file__))[0]
    #print curdir
    localdir = os.path.join(curdir,'rootfile')
    #print localdir
    #DownYaml(rootdict,localdir)
    filelist = os.listdir(localdir)
    #print filelist
    filedict=ParYaml(localdir,filelist)
    m=parCountry(filedict)