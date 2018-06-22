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
    #srsnav = bsObj.find('div',{"class": "col_6 shift_2 margin_bottom zone-counts stack_mobile"})
    #dnsnav = bsObj.find('div', {"class": "col_10 shift_1 clearfix"})
    
    srsnav = bsObj.find('table')
    

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yed = yesterday.strftime("%Y%m%d")
 
    with open (yed,'a+') as f:
        f.write('all srs data set\n')
        for m in srsnav:
            f.write(str(m))
    for tr in srsnav.findAll('tr'):
        #print tr
        for td in tr.findAll('td'):
            print td
            tt =  td.getText()
            print tt.strip('.')
            #f.write(tt)
        #f.write('all dns data set\n')
        #for l in dnsnav:
        #    if len(l) <>0 :
        #         continue;
        #    f.write(str(l))


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
    GetHtmlTab(url)
    #GetRootfile(url2)