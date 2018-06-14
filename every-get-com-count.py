#!/usr/bin/env python
import sys
import chardet
import pandas
import requests
from bs4 import BeautifulSoup

'''every-get-com-count.py 
   from URL Get com and net TLD SRS and DNS data set
   '''

def GetHtmlTab(url):
    html = requests.get(url)
    page = html.content.decode("utf-8")
    bsObj = BeautifulSoup(page, 'lxml')
    srsnav = bsObj.find('div',{"class": "col_6 shift_2 margin_bottom zone-counts stack_mobile"})
    dnsnav = bsObj.find('div', {"class": "col_10 shift_1 clearfix"})
    
    for m in srsnav:
        print m
    
    for l in dnsnav:
        if len(l) <>0 :
            continue;
        #print l


if __name__ == '__main__':
    url = 'https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml'
    GetHtmlTab(url)