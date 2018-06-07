#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'CNNIC'

import csv
import sys
import urllib

import chardet
import pandas
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

'''
爬取www.rfc-editor.org页面中RFC的状态为Standard的RFC列表并且保存到csv文件中
'''
def GetHtmlTab(url):
    html = requests.get(url)
    page = html.content.decode("utf-8")
    bsObj = BeautifulSoup(page, 'lxml')
    nav = bsObj.find('div', {"class": "scrolltable"})
    #print type(nav)  #<class 'bs4.element.Tag'>
    ulist = []
    for line in nav:
        trs = line.find_all('tr')
        for tr in trs:
            ui = []
            for td in tr:
                ui.append(td.string)
            ulist.append(ui)
    #print ('**********************************')
    print ulist #要是这样的话，name 和file 因为有超链接，因此爬到的这两个字段为空
    return ulist

#保存资源
def save_contents(urllist):
    writer = csv.writer(file('E:\personal-study\python\pythonscripts/rfc.csv','wb+'))
    for i in range(len(urllist)):
        writer.writerow([urllist[i][0],urllist[i][1],urllist[i][2]])
        
if __name__ == '__main__':
    url='https://www.rfc-editor.org/search/rfc_search_detail.php?sortkey=Number&sorting=DESC&page=All&pubstatus%5B%5D=Standards%20Track&std_trk=Internet%20Standard'
    ulist=GetHtmlTab(url)
    save_contents(ulist)
