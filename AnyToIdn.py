#!/usr/bin/env python
#coding=gbk

#from __future__ import unicode_literals
import idna
import json
import sys


def TextToIdna(yourfile):
    lines=[]
    with open(yourfile, 'r') as f:
        for line in f:
            lines.append(line.strip())
    tmplist=[]
    for l in lines:
        str1 = l.encode('raw_unicode_escape').split('.')
        tmplist.append(str1)

    for j in tmplist:
        jlist=[]
        for h in j:
            if h.startswith('xn--'): 
                tt = idna.decode(h)
                jlist.append(tt) 
            else:
                jlist.append(h) 
        print '.'.join(jlist)

if __name__ == '__main__':
    '''
     The Script be used from file each line to ZW,when each line contains puny code anyway,It can be normal runing....................
    '''
    yourfile=sys.argv[1]
    TextToIdna(yourfile)