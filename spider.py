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
            current_time=cur.execute("select time from weather where city='%s'" %(cityName))
            if current_time==ddatetime:
                break;
            else:
                cur.execute("insert into weather values('%s','%s','%s','%s');" % (cityName, ddatetime, rain24h, wd))







            # python_to_json=json.dumps(value[rootkey], ensure_ascii=True)
        # json_to_python=json.loads(python_to_json)
        # if int(json_to_python[0]["obtId"]) == 59304:
        #
        #     print json_to_python[1]

    # fp = open('data.json', 'a+')
    # fp.write(json.dumps(value))
    # fp.close()

    # for subkey in subvalue:
    #     print subkey,subvalue[subkey]
    #

def test_function():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data

def sleeptime(hour,min,sec):
    return hour*3600+min*60+sec;




interval=sleeptime(5,0,0)
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




# data_written = test_function()
# print data_written["59658"]
# print json.loads(json.dumps(data_written["59658"]))[0]['wd']