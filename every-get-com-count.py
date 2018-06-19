#!/usr/bin/env python
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

    with open (yed,'aw+') as f:
        f.write('all srs data set\n')
        for m in srsnav:
            f.write(str(m))

        f.write('all dns data set\n')
        for l in dnsnav:
            if len(l) <>0 :
                continue;
            f.write(str(l))

if __name__ == '__main__':
    '''every-get-com-count.py 
    from URL Get com and net TLD SRS and DNS data set
    '''
    url = 'https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml'
    GetHtmlTab(url)