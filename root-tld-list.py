#!/usr/bin/env python
#coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
import datetime 

url='https://www.iana.org/domains/root/db'
html = requests.get(url)
page = html.content.decode("utf-8")
bsObj = BeautifulSoup(page, 'lxml')
roottld = bsObj.find('table',{"id": "tld-table"})

for i in roottld:
    print i
