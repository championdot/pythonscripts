#!/usr/bin/env python
#coding=utf8

#from __future__ import unicode_literals
import idna
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def TextToIdna(yourfile):
    lines=[]
    with open(yourfile, 'r') as f:
        for line in f:
            lines.append(line.strip())
    #把文本的每一行读取出来保存成一个列表

    tmplist=[]
    for l in lines:
        str1 = l.encode('raw_unicode_escape').split('.')
        tmplist.append(str1)
    #针对大列表里的字段再根据.分割成小列表，这样保证每一行是一个小列表，这两段for循环可以写成一个

    for j in tmplist: #循环大列表
        jlist=[]
        for h in j: #循环小列表，相当于处理每一行文本数据
            if h.startswith('xn--'): 
                tt = idna.decode(h)
                jlist.append(tt) 
            else:
                jlist.append(h) 
        print '.'.join(jlist) #每一行的内容是一个列表，合成一个文本字符串
        
if __name__ == '__main__':
    '''
     The Script be used from file each line to ZW,when each line contains puny code anyway,It can be normal runing....................
    '''
    yourfile=sys.argv[1]
    TextToIdna(yourfile)