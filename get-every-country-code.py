#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs

html_doc = requests.get('https://zh.wikipedia.org/wiki/ISO_3166-1').text
# print(html_doc)
soup = bs(html_doc, 'html.parser')
# print(soup.table.find('td').text)
all_trs = soup.table.find_all('tr')
for tr in all_trs:
    if tr.find('td') is not None:
        # print(tr.find('td').descendants)
        for child in tr.find('td').children:
            # print(child)
            with open('country_code.txt', 'a') as f:
                f.write(child+',')

