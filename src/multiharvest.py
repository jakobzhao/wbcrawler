# !/usr/bin/python  
# -*- coding: utf-8 -*-

import string, threading, time
import urllib
import sqlite3
import sys, os

#import ssl, socket
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf-8')

num = 1
tmp_num = num
headers = {
        "User-Agent" : "Mozilla/5.3 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "Accept" : "text/xml,application/xml,application/xhtml+xml,text/htm;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "gbk",
        "Content-type": "application/x-www-form-urlencoded;charset=gbk",
    }


#looking for proxies: http://proxy-list.org/english/index.php
proxies = {
    'http': 'http://110.208.27.120:9000',
    'http': 'http://198.211.121.51:80',
    'http': 'http://78.46.178.195:8118',
    'http': 'http://177.1.139.242:3128',
    'http': 'http://177.43.16.51:8080',    
    }


proxies = {
     'http': 'http://1.85.4.142:8080',      
           }

current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
database = current_path + '/../data/house2.sqlite'


def add_harvestHouses(database, count, ctable):
    
    global mutex, tmp_num
    query_header_houses = 'INSERT INTO houses (name, address, snd_adm, fst_adm, developer, picture, price, url) VALUES ( '
    
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    #'select city_id, page_id, city_name, abbr, fst_adm from cities where checked = -1


    #Dividing the tasks
    q = len(ctable) / num
    i = count * q
    
    print "total harvesting tasks ", str(len(ctable)) + "\n"
    print "thread " , str(count), " starts from ", str(i) + "\n"
    while i < ( count + 1 ) * q: 
        id = int(ctable[i][0])
        page_id = int(ctable[i][1]) + 1
        city_name = ctable[i][2]
        abbr = ctable[i][3]
        fst_adm = ctable[i][4]
        
        url = 'http://newhouse.' + abbr + '.soufun.com/house/' + urllib.quote(str(city_name)) + '_________________' + str(page_id) + '___.htm'
        if abbr == "bj":
            url = 'http://soufun.com/house/' + urllib.quote(str(city_name)) + '_________________' + str(page_id) + '___.htm'
        print url
        try:
            webpage = pq(url, parse="html", headers= headers, proxies = proxies, timeout = 1)
            #webpage = pq(url, parse="html", headers= headers, timeout = 1)
        except:
            #i = i + 1
            continue
        
        
        houses = webpage('.sslalone')
        mutex.acquire()
        for item in houses:
            house = {}
            house['snd_adm'] = city_name
            house['fst_adm'] = fst_adm
            house['url'] = pq(item)("div.sslaimg a").attr("href").encode('latin-1').decode('gbk')
            house['picture'] = pq(item)("div.sslaimg a img").attr("src").encode('latin-1').decode('gbk')
            house['name']= pq(item)("div.sslaimg a img").attr("alt").encode('latin-1', 'ignore').decode('gbk', 'ignore')
            house['developer'] = pq(item)("ul.sslainfor li").eq(3).find("a").text().encode('latin-1', 'ignore').decode('gbk', 'ignore')
            house['price'] = str(pq(item)(".junjia")).encode('latin-1').decode('gbk')
            try:
                house['address'] = pq(item)("ul.sslainfor li font").attr("title").encode('latin-1', 'ignore').decode('gbk', 'ignore')
            except:
                house['address'] = pq(item)("ul.sslainfor li").eq(1).text().encode('latin-1', 'ignore').decode('gbk', 'ignore').replace(" 查看地图","")
                
            query_body_houses = "'" + house['name'] + "', '" + house['address'] + "', '" + house['snd_adm'] + "', '" + house['fst_adm'] + "', '" + house['developer'] + "', '" + house['picture'] + "', '" + house['price'] + "', '" + house['url'] + "')"
         
            try:
                cursor.execute(query_header_houses + query_body_houses)
                #conn.commit()
                #mutex.release()
            except sqlite3.Error, e:
                print  "This house has already been inserted.", e.args[0]
            print house['name'], house['snd_adm']
            i = i + 1
        
        checked = 0
        if len(webpage('.sslalone')) == 0:
            checked = -1
            print "there is no houses in the city of", city_name, " the page of ", page_id
        else:
            checked = 1
      
        cursor.execute('update ctable set checked = ' + str(checked) + ' where rowid = ' + str(id))
        conn.commit()
        mutex.release()
        i = i + 1
        
    conn.close()
    tmp_num = tmp_num - 1
    print "thread" , str(count), " is dead. And only ", str(tmp_num), " is left." 
    


def main(num):
    global count, mutex
    threads = []
    
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    
    cursor.execute('select rowid, page_id, city_name, abbr, fst_adm from ctable where checked != 1')
    ctable = cursor.fetchall()
    conn.close()
    
    # 创建一个锁
    mutex = threading.Lock()    
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=add_harvestHouses, args=(database, x, ctable)))
    # 启动所有线程
    for t in threads:
        t.start()
    ## 主线程中等待所有子线程退出
    for t in threads:
        t.join()  
 
 
if __name__ == '__main__':
    main(num)