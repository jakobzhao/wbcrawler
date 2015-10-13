# !/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import sqlite3
import sys
import os


#import ssl, socket
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf-8')

num = 20
headers = {
        "User-Agent" : "Mozilla/5.3 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "Accept" : "text/xml,application/xml,application/xhtml+xml,text/htm;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "gbk",
        "Content-type": "application/x-www-form-urlencoded;charset=gbk",
    }

proxies = {
     'http': 'http://1.85.4.142:8080',      
           }


current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
database = current_path + '/../data/house2.sqlite'



def add_bdgeocoding(database, count, houses):
    global mutex
    #Variables
    #http://api.map.baidu.com/geocoder/v2/?address=浦东江环路688弄&output=json&ak=Y4wB8DznamkwhY8RxDiYNSHS&callback=showLocation
    #http://api.map.baidu.com/geocoder/v2/?address=%E6%B5%A6%E4%B8%9C%E6%B1%9F%E7%8E%AF%E8%B7%AF688%E5%BC%84&output=json&ak=Y4wB8DznamkwhY8RxDiYNSHS
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    
    #Dividing the tasks
    q = len(houses) / num
    i = count * q
    
    print "total geocoding tasks ", str(len(houses)) + "\n"
    print "thread " , str(count), " starts from ", str(i) + "\n"
    while i < ( count + 1 ) * q: 
        #address = houses[i][2] + '市' + houses[i][0]
        address =  houses[i][0]
        
        address = address.replace("!", " ").replace("*", " ").replace("'", " ").replace("(", " ").replace(")", " ").replace(";", " ").replace(":", " ").replace("@", " ").replace("&", " ").replace("=", " ").replace("+", " ").replace("$", " ").replace(",", " ").replace("/", " ").replace("?", " ").replace("%", " ").replace("#", " ").replace("[", "").replace("]", " ")
        # all the reserved code by baidu ! * ' ( ) ; : @ & = + $ , / ? % # [ ]
        url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=xml&ak=Y4wB8DznamkwhY8RxDiYNSHS'
        try:
            #content = pq(url,  parser='html_fragments', headers = headers, proxies = proxies, timeout = 0.1)
            content = pq(url,  parser='html_fragments', timeout = 1)
        except:
            #i = i + 1
            print "entered 3"
            continue
        
        lat = content("lat").text()
        lng = content("lng").text()
        if lat == "":
            print "entered 1"
            lat = str(1)
            lng = str(1)            
            #i = i + 1
            #continue
        mutex.acquire()
        cursor.execute('update houses set lat = '+ lat +', lng = ' + lng + ' where ROWID == ' + str(houses[i][5]))
        conn.commit()
        mutex.release() 
        print lat, lng, address, "Current house is No.", str(i)
        i = i + 1
    conn.close()
    print "Successfully geocode the tabels!"
    #thread.exit_thread() 
    #return True



 
def main(num):
    global count, mutex
    threads = []
    
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    cursor.execute('select address, fst_adm, snd_adm, lat, lng, ROWID from houses where lat = 1')
    
    houses = cursor.fetchall()
    conn.close()
    #count = 1
    # 创建一个锁
    mutex = threading.Lock()    
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=add_bdgeocoding, args=(database, x, houses)))
    # 启动所有线程
    for t in threads:
        t.start()
    ## 主线程中等待所有子线程退出
    #for t in threads:
    #    t.join()  
 
 
if __name__ == '__main__':
    main(num)