#!/usr/bin/env 

import string
import yaml 
import sys
import urllib
import os
from collections import Counter

rootdict = []
#rootdict = {} 
for i in range(97,110):
    a=('http://www.root-servers.org/download/%s-root.yml' %chr(i))
    akey=a.split('/')[-1]
    rootdict.append(a)
    #rootdict[akey]=a
#print rootdict

def ParAllYaml(localdir,filelist):
    allinfo=[]
    for file in filelist:
        filepath=os.path.join(localdir,file)
        with open(filepath,'r') as fy:
            x = yaml.load(fy)
        nodecount=len(x['Instances'])
        allnodelist=x['Instances']
    allinfo.extend(allnodelist)
    print allinfo
    return allinfo

def Xctry(allinfolist):
    for nodedict in allinfolist:
        if 'CN' in nodedict.values():
            print nodedict

def Xinfo(allinfolist):
    contrylist =[]
    for nodedict in allinfolist:
        if 'Country' not in nodedict.keys():
            nodedict['Country']=nodedict['Town']
            contrylist.append(nodedict['Country'])
            continue 
        else:
            contrylist.append(nodedict['Country'])
    print len(contrylist)
    print contrylist
    count_frq ={}
    for item in contrylist:
        if item in count_frq:
            count_frq[item] += 1
        else:
            count_frq[item] =1
    #print len(contrylist)
    frq=sorted(count_frq.items(),key = lambda x:x[1],reverse = True)
    print frq
    #for i in frq:
    #    print str(i).strip('(').strip(')')
    #return contrylist

def parCountry(allinfolist):
    contrylist =[]
    n = []
    '''
    alllist=[
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
    for root in alllist:
        for infolist in root['info']:
            for l in infolist:
                if 'Country' not in l.keys():
                    l['Country']=l['Town']
                    contrylist.append(l['Country'])
                    continue 
                else:
                    contrylist.append(l['Country'])
    print len(contrylist)
    print contrylist
    count_frq ={}
    for item in contrylist:
        if item in count_frq:
            count_frq[item] += 1
        else:
            count_frq[item] =1
    #print len(contrylist)
    frq=sorted(count_frq.items(),key = lambda x:x[1],reverse = True)
    print frq

    
if __name__ == '__main__':
    curdir = os.path.split(os.path.realpath(__file__))[0]
    localdir = os.path.join(curdir,'rootfile2')
    filelist = os.listdir(localdir)
    filedict=ParAllYaml(localdir,filelist)
    #print filedict
    Xinfo(filedict)
    #Xctry(filedict)