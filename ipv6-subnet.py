#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
功能：划分IPV6子网
Usage:$0  2001:dc7:1000::1/122 126 
''' 
import sys
import re

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
# base = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]

#16--->10---2
#hex2dec---->dec2bin

def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

def bin2dec(string_num):
    return str(int(string_num, 2))

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))

def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))

def Nzero(n):
    #将当前大网段中的冒号替换成几组0000
    c=':'.join(int(n) * '0'.zfill(4).split(':')) #简写为下面两行
    #b=int(n) * '0'.split(':')
    #c=':'.join(b)
    d=':' + c+':' 
    #print d  #:0000:0000:0000:0000: 
    return d  #:0000:0000:0000:0000: 

#def IP6AddrToBin(ip6addr):

def splitAllbinStr(binstr,submask,bigmask):                                                      
    prestr = binstr[:int(bigmask)] #前bigmask位不变 

    interfacebitNum=int(128)-int(submask) #128 - 126 submask位数后面不变的位数
    EnableAddrCount = 2 ** int(interfacebitNum) -2
    dynbitNum=int(submask)-int(bigmask) # 126 - 120   获取变化的位数
    SubNetCount=2**int(dynbitNum)  # 2** 6 获取子网个数
    #print SubNetCount,dynbitNum

    mindata=int(dynbitNum)*'0'  # 000000 变化位的起始地址
    maxdata=int(dynbitNum)*'1'  # 111111 变化位的最后地址

    #startaddr  #每个子网的可用地址数，以及大网段里最小地址和最大地址
    #maxaddr

    #stepNum=int(dynbitNum)-1 #5
    #mstep = int(stepNum) * '0' + '1' #000001  地址自增的二进制步长,这里没有用到

    endstr = int(interfacebitNum) * '0' #00 主机地址位数

    subnetlist=[]
    for i in range(int(SubNetCount)): #这里巧妙的用了子网个数来作为循环次数，而不是从开始值自增
        dynstr = str(dec2bin(i)).zfill(dynbitNum)
        allstr = prestr + dynstr + endstr
        alldata=bin2hex(allstr)  #这个返回是没有冒号分割的字符串
        bindata=':'.join(re.findall(r'.{4}',alldata)) #每隔4个字符用冒号分割的字符串
        print bindata+'/' + str(submask)
        subnetlist.append(bindata + '/' + str(submask))
    return SubNetCount,EnableAddrCount


if __name__ == '__main__': 
    # 2001:dc7:1000::/120 126 参考RFC5952
    IP6BigNet = sys.argv[1]  #2001:dc7:1000::/120 
    IP6Subsuffix = sys.argv[2]  #126 
    if len(sys.argv) > 2:
        pass
    else:  
        print "输入合法的IPv6地址段以及掩码" 
        sys.exit() 

    IP6BigAddr = IP6BigNet.split('/')[0]  #2001:dc7:1000:: 
    IP6Bigsuffix = IP6BigNet.split('/')[1]   #120

    # 判断必须输入两个参数;\ #子网网段掩码必须大于大网段的掩码;\ #冒号在大网段地址中只能出现1次; \ # 大网段字符串里必须包含'/'；\        #大网段字符串里不能包含'.'#IPv6地址格式8段7个冒号 

    if len(sys.argv) > 2 and int(IP6Subsuffix) > int(IP6Bigsuffix) and IP6BigNet.count('::') == 1 and IP6BigNet.count('/') == 1 and IP6BigNet.count('.') == 0 and IP6BigNet.count('::') <= 7:
        pass
    else:
        print "输入合法的IPv6地址段以及掩码"
        sys.exit(0)

    #计算出大网段里共有多少个地址
    #2 ** (128 - 120) 个地址
    IP6BigAddrCount= 2 ** (int(128) -  int(IP6Bigsuffix))
    
    #计算出变化的后面几位

    #先将输入的大网段地址的双冒号进行补全
    #求出当前大网段里冒号的个数，决定需要补充几段0000
    ZeroNum = int(8) - int(IP6BigAddr.count(':'))
    MergeZero =  Nzero(ZeroNum)    
    AllStr = IP6BigAddr.replace("::",MergeZero)
    print AllStr #2001:dc7:1000:0000:0000:0000:0000:1
   
    g=[]
    for i in AllStr.split(':'):
        f=i.zfill(4)
        #e=':'.join(f)
        g.append(''.join(f))

    hexjoinstr = ''.join(g)
    #print hexjoinstr #20010dc7100000000000000000000000
    print re.findall(r'.{4}',hexjoinstr)  #['2001', '0dc7', '1000', '0000', '0000', '0000', '0000', '0001']

    AllbinStr =''
    for i in hexjoinstr:
        c = i.upper()
        decstr = hex2dec(c) #十六进制转十进制
        #bin(int(decstr))[2:]).zfill(4) #利用系统自带的bin函数将十进制转换为二进制，并且去掉前面的0b字符串，同时补全4位
        binstr = (bin(int(decstr))[2:]).zfill(4)
        #netregx=re.findall(r'.{4}',binstr)
        #print netregx
        AllbinStr += binstr
        #AllbinStr += netregx
    #print AllbinStr
    #00100000000000010000110111000111000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    subcount,enableaddr=splitAllbinStr(AllbinStr,IP6Subsuffix,IP6Bigsuffix)
print "%s has /%s  subnet %s , and every subnet available address count %s" %(IP6BigNet,IP6Subsuffix,subcount,enableaddr) 