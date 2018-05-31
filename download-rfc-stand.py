#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'CNNIC'

from bs4 import BeautifulSoup
import requests
import urllib
import pandas
import sys


type=sys.getfilesystemencoding() 

url='https://www.rfc-editor.org/search/rfc_search_detail.php?sortkey=Number&sorting=DESC&page=All&pubstatus%5B%5D=Standards%20Track&std_trk=Internet%20Standard'
html = requests.get(url)
page = html.content.decode("utf-8").encode(type)
bsObj = BeautifulSoup(page, 'lxml')
nav = bsObj.find('div', {"class": "scrolltable"})
#print nav
for line in nav:
    for d in line.find_all('tr'):
        print d        
        print ('**********************************')