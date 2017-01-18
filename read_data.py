#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import json

import MySQLdb

def test_function():
    with open('data.json') as json_file:
        data=json.load(json_file, object_pairs_hook=my_obj_pairs_hook)
        return data


def my_obj_pairs_hook(lst):
    result={}
    count={}
    for key,val in lst:
        if key in count:count[key]=1+count[key]
        else:count[key]=1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key]=[result[key], val]
        else:
            result[key]=val
    return result

data_written = test_function()
print len(data_written["59088"])
for i in range(0,len(data_written["59088"])):
    print  data_written["59088"][i]


print type(data_written['59088'][0][0]['cityName'])
print type(data_written['59088'][0][0]['ddatetime'])
print type(unicode(str(data_written['59088'][0][0]['wd']),'utf-8'))
print type(data_written['59088'][0][0]['wd'])



cityName=data_written['59088'][0][0]['cityName']
ddatetime=unicode(str(data_written['59088'][0][0]['ddatetime']),'utf-8')
rain24h=unicode(str(data_written['59088'][0][0]['rain24h']),'utf-8')
wd=unicode(str(data_written['59088'][0][0]['wd']),'utf-8')

print cityName,ddatetime,rain24h,wd


conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='4008517517',
        db ='weather',
        )
cur = conn.cursor()
conn.set_character_set('utf8')
# cur.execute("insert into weather values(12,12,12,12")
# cur.execute("insert into weather values('a','b','d','c';")
# cur.execute("insert into test2 values('a','b');")
cur.execute("insert into weather values('%s','%s','%s','%s');"%(cityName,ddatetime,rain24h,wd))

# cur.execute("select * from user where userid = '%s' and password = '%s'" %(userid,password))

cur.close()
conn.commit()
conn.close()







# print data_written["59658"]
# print json.loads(json.dumps(data_written["59658"]))[0]['wd']