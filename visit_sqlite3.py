#!/usr/bin/env python

import sqlite3
import sys
import json
reload (sys)
sys.setdefaultencoding('utf-8')


conn = sqlite3.connect('/home/ops/ipv6_mon/ctrl/localdatabase/ctrl.db')
c = conn.cursor()

cursor = c.execute("select * from fetchrs")
for row in cursor:
    print row #每条记录就是每一天的数据

conn.close()
m=(u'2017-09-14 14:36:12',u'[{"__fetchrs__": true, "domain": "baidu.com", "fetchtime": "2017-09-14 14:36:02", "rank": "1"},{"__fetchrs__": true, "domain": "qq.com", "fetchtime": "2017-09-14 14:36:02", "rank": "2"}, {"__fetchrs__": true, "domain": "taobao.com", "fetchtime": "2017-09-14 14:36:02", "rank": "3"}, {"__fetchrs__": true, "domain": "tmall.com", "fetchtime": "2017-09-14 14:36:02", "rank": "4"}, {"__fetchrs__": true, "domain": "sohu.com", "fetchtime": "2017-09-14 14:36:02", "rank": "5"}, {"__fetchrs__": true, "domain": "sina.com.cn", "fetchtime": "2017-09-14 14:36:02", "rank": "6"}, {"__fetchrs__": true, "domain": "jd.com", "fetchtime": "2017-09-14 14:36:02", "rank": "7"}, {"__fetchrs__": true, "domain": "weibo.com", "fetchtime": "2017-09-14 14:36:02", "rank": "8"}, {"__fetchrs__": true, "domain": "360.cn", "fetchtime": "2017-09-14 14:36:02", "rank": "9"}, {"__fetchrs__": true, "domain": "google.com", "fetchtime": "2017-09-14 14:36:02", "rank": "10"}, {"__fetchrs__": true, "domain": "list.tmall.com", "fetchtime": "2017-09-14 14:36:02", "rank": "11"}, {"__fetchrs__": true, "domain": "youtube.com", "fetchtime": "2017-09-14 14:36:02", "rank": "12"}, {"__fetchrs__": true, "domain": "google.com.hk", "fetchtime": "2017-09-14 14:36:02", "rank": "13"}, {"__fetchrs__": true, "domain": "alipay.com", "fetchtime": "2017-09-14 14:36:02", "rank": "14"}, {"__fetchrs__": true, "domain": "youth.cn", "fetchtime": "2017-09-14 14:36:02", "rank": "15"}, {"__fetchrs__": true, "domain": "csdn.net", "fetchtime": "2017-09-14 14:36:02", "rank": "16"}, {"__fetchrs__": true, "domain": "hao123.com", "fetchtime": "2017-09-14 14:36:02", "rank": "17"}]')
#m 是一个序列，每个元素是unicode）
n= m[-1].encode('gbk') 
p = json.loads(n) #str to json
for k in p:
    print k['fetchtime'].split()[0],k['rank'],k["domain"]
