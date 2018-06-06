#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'CNNIC'

from bs4 import BeautifulSoup
import requests
import urllib
import pandas
import sys
import chardet
import csv


url='https://www.rfc-editor.org/search/rfc_search_detail.php?sortkey=Number&sorting=DESC&page=All&pubstatus%5B%5D=Standards%20Track&std_trk=Internet%20Standard'
html = requests.get(url)
page = html.content.decode("utf-8")
bsObj = BeautifulSoup(page, 'lxml')
nav = bsObj.find('div', {"class": "scrolltable"})
print type(nav)  #<class 'bs4.element.Tag'>
ulist = []
for line in nav:
    trs = line.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)
        #print ('**********************************')

#保存资源
def save_contents(urllist):
    writer = csv.writer(file('E:\personal-study\python\pythonscripts/rfc.csv','wb'))
    for i in range(len(urllist)):
        print type(urllist)
        writer.writerow([urllist[i][0],urllist[i][1],urllist[i][2]])

save_contents(ulist)