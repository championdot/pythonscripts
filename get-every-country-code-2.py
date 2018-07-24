#!/usr/bin/env python
#coding: utf8

import requests
from bs4 import BeautifulSoup as bs


html_doc = requests.get('http://www.lingoes.cn/zh/translator/langcode.htm').text
# print(html_doc)
soup = bs(html_doc, 'html.parser')
print(soup.table.find('tr').text)
all_trs = soup.table.find_all('tr')
for tr in all_trs:
    if tr.find('td') is not None:
        # print(tr.find('td').descendants)
        for child in tr.find('td').children:
            # 将NavigableString 转化为string
            new_str = child.string + ''
            if '语言' not in new_str and '-' in new_str:
                with open('country_code.txt', 'a') as f:
                    f.write('\'' + new_str + '\',')