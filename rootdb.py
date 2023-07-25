#!/usr/bin/env python

import sys
reload (sys)
sys.setdefaultencoding('utf-8')
import os
import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import re
import logging
import json
import time

from concurrent.futures import ThreadPoolExecutor,as_completed



curdt = datetime.datetime.now().strftime('%Y%m%d')
ysdt= (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def create_detail_day():
    daytime = datetime.datetime.now().strftime('%Y%m%d')
    #hourtime = datetime.datetime.now().strftime('%H:%M:%S')
    return daytime


def make_print_to_file(path='./'):
    class Logger(object):
        def __init__(self,filename="default.log",path="./"):
            #sys.stdout = io.TextIOWrapper(sys.stdout,encoding='utf-8')
            self.terminal = sys.stdout
            #self.log = open(os.path.join(path,filename),"a",encoding='utf-8')
            self.log = open(os.path.join(path,filename),"a")
        def write(self,message):
            self.terminal.write(message)
            self.log.write(message)
        def flush(self):
            pass
    sys.stdout = Logger(create_detail_day(),path=path)


def intodb(tablename,dataset):
    connector = sqlite3.connect('example.db')
    cursor = connector.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS  ROOTTLDS (date text,tld text,type text,manager text,result text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS  TLDSINFO (date text,tld text,NS text,glue text)''')
    connector.commit()

    if tablename == 'TLDSINFO':
        for data in dataset:
            datadb = [{"date_p": data.get('date'),
               "tld_p": data.get('tld'),
               "ns_p": data.get('NS'),
               "glue_p": data.get('glue')}]
            cursor.executemany("INSERT OR REPLACE INTO TLDSINFO (date, tld, NS,glue) VALUES (:date_p, :tld_p, :ns_p, :glue_p)""", datadb)
        connector.commit()

    elif tablename == 'ROOTTLDS':
        for data in dataset:
            datadb = [{"date_p": data.get('date'),
               "tld_p": data.get('tld'),
               "type_p": data.get('type'),
               "manager_p": data.get('manager'),
               "result_p": data.get('result')}]
            cursor.executemany("INSERT OR REPLACE INTO ROOTTLDS (date, tld, type, manager, result) VALUES (:date_p, :tld_p, :type_p, :manager_p, :result_p)""", datadb)

        connector.commit()

    cursor.close()
    connector.close()


def roottlds():
    tldsurlset=[]
    rootdataset=[]
    data={}
    rooturl='https://www.iana.org/domains/root/db'
    html = requests.get(rooturl)
    return_code= html.status_code
    #print return_code

    if return_code == 200:
        page = html.content
        file = BeautifulSoup(page, 'html.parser')
        for row in file.findAll('table')[0].tbody.findAll('tr'):
            tldurl = row.findAll('td')[0].find('a').get('href')
            tldsurlset.append(tldurl)
            zonename = row.findAll('td')[0].find('a').get('href').split('/')[-1].split('.')[0]
            type = row.findAll('td')[1].get_text()
            manager = row.findAll('td')[2].get_text()
            data['date'] = curdt
            data['zonename'] = zonename
            data['type'] = type
            data['manager'] = manager
            data['result'] = 'old'
            rootdataset.append(data)

            print data
    #print len(tldsurlset)
    return rootdataset,tldsurlset


def tldsinfo(tldurl):
    data={}
    tlddataset=[]
    baseurl="https://www.iana.org"

    #for url in tldsurlset:
    #    time.sleep(5)
    html = requests.get(baseurl+tldurl)
    return_code= html.status_code
    #print return_code
    if return_code == 200:
        page = html.content.decode("utf-8")
        file = BeautifulSoup(page, 'html.parser')
        zonename = tldurl.split('/')[-1].split('.')[0]
        data['tld'] = zonename
        data['date']= curdt
        tables=file.find_all("table", class_=["iana-table"])
        if len(tables) == 0:
            data['NS'] = 'null'
            data['glue'] = 'null'
            print data
            tlddataset.append(data)
            exit
        else:
            for div in tables:
                rows = div.find_all('tr')
                allrows=rows[1:]
                for i in range(len(allrows)):
                    NS = (allrows[i].findAll('td')[0].get_text()).decode('utf-8')
                    data['NS']=NS
                    glues = allrows[i].findAll('td')[1].find_all(text = re.compile("\d"))
                    for j in range(len(glues)):
                        data['glue']=glues[j]
                        print data
                #tlddataset.append(data)
    #return tlddataset


if __name__ == '__main__':
    make_print_to_file(path="./rootdb/")
    rootdataset,tldsurlset=roottlds()
    print datetime.datetime.now()

    executor = ThreadPoolExecutor(max_workers=5)
    all_task = [executor.submit(tldsinfo,(tldurl)) for tldurl in tldsurlset]

    for future in as_completed(all_task):
        data = future.result()
        #print ("{}s success".format(data))

    print datetime.datetime.now()
