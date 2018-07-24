#!/usr/bin/env python
#coding: utf8


import sys
import requests
from bs4 import BeautifulSoup
import datetime 


def GetHtmlTab(url):

    html = requests.get(url)
    page = html.content.decode("utf-8")
    bsObj = BeautifulSoup(page, 'lxml')
    srsnav = bsObj.find('div',{"class": "col_6 shift_2 margin_bottom zone-counts stack_mobile"})
    dnsnav = bsObj.find('div', {"class": "col_10 shift_1 clearfix"})
    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yed = yesterday.strftime("%Y%m%d")

    #trs = srsnav.find_all('tr')
    ulist = []
    trs = srsnav.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr.strip():
            ui.append(td.string)
        ulist.append(ui)
    #print ('**********************************')
    print ulist 

    #with open (yed,'aw+') as f:
    #    f.write('all srs data set\n')
    #    for m in srsnav:
    #        f.write(str(m))

    #    f.write('all dns data set\n')
    #    for l in dnsnav:
    #        if len(l) <>0 :
    #            continue;
    #        f.write(str(l))



def GetRootfile(url):
    html = requests.get(url)
    page = html.content.decode("utf-8")
    bsObj = BeautifulSoup(page, 'lxml')
    rootnav = bsObj.find('p')
    with open ('rootzone','a+') as f:
        for i in rootnav:
            lit = i.split('\t')
            if 'RRSIG' in lit or 'DNSKEY' in lit or 'DS' in lit or 'A' in lit or 'AAAA' in lit or 'NSEC' in lit:
                continue
            else:
                f.write(lit)
        for line in f.readlines():
            print line

if __name__ == '__main__':
    '''every-get-com-count.py 
    from URL Get com and net TLD SRS and DNS data set
    #url1中可以在col_10 shift_1下
    #包含一个div（col_6 shift_2 margin_bottom zone-counts stack_mobile）和
    #<p>（clear） 
    #其中div为注册的表格数据，<p>为解析数据
    #输出文件可以月为单位输出到一个文件（注册和解析各一个文件）
    '''
    url = 'https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml'
    #url2 = 'https://www.internic.net/domain/root.zone'
    GetHtmlTab(url)
    #GetRootfile(url2)
    '''
    日期，解析量，com，net
    '''

