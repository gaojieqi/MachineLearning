#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import hmac
import base64,binascii,zlib
import os,random
import time
import httplib
import urllib
import urllib2
import re
import json
import MySQLdb

def registerUrl():
    try:
        req = urllib.urlopen("http://www.gdmo.cn/weather-gdmo/citylive/city-live!cityLiveData")
        data = req.read()
        return data
    except IOError as error:
        print("Your network is so bad!")
        exit()

def saveData(jsonData,conn,cur):
    value = json.loads(jsonData)
    rootlist = value.keys()
    for rootkey in rootlist:
        for i in range(0,len(value[rootkey])):
            cityName = value[rootkey][i]['cityName']
            ddatetime = unicode(str(value[rootkey][i]['ddatetime']), 'utf-8')
            rain24h = unicode(str(value[rootkey][i]['rain24h']), 'utf-8')
            wd = unicode(str(value[rootkey][i]['wd']), 'utf-8')
            request="select temperature from weather where city='%s' and time='%s'" % (cityName,ddatetime)
            quantity=cur.execute(request)
            # # 打印表中的多少数据
            # info = cur.fetchmany(quantity)
            # for ii in info:
            #     print ii
            if quantity > 0:
                print "pass"
            else:
                cur.execute("insert into weather values('%s','%s','%s','%s');" % (cityName, ddatetime, rain24h, wd))
                print "Insert succeed in"+time.strftime( ISOTIMEFORMAT, time.localtime() )

def sleeptime(hour,min,sec):
    return hour*3600+min*60+sec;


ISOTIMEFORMAT='%Y-%m-%d %X'
interval=sleeptime(1,0,0)

while 1==1:
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='4008517517',
        db='weather',
    )
    cur = conn.cursor()
    conn.set_character_set('utf8')

    data = registerUrl()
    saveData(data,conn,cur)


    cur.close()
    conn.commit()
    conn.close()
    time.sleep(interval)

