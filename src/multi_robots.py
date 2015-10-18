# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

# harvesting plan:
# 1 main
# 4 repost
# 4 profile
# 4

# 7.6 posts per 5.4 users  3:2

# info 20 secs per user     540 total users
# path 30 secs per user     540 total users
# reposts  计算比例   4 times main post    760/5 = 152    2 sec(s) per post

# main 1 sec per post     152    total post
# repost     152 * 20 +  (152 * 4 增加的新帖？ 大于十条留言的帖子，超过三天的帖子）          600    total post


# main/repost ?
# 设置动态时间。或者重启？
# 获取所有的，
# 单另跑 reposts, info and path
# repost 一定要有时间限制，要不越跑越多。 三天之内。三天以外，量大的。（repost 其实是在做全局扫描。）

import threading
import sys

from pymongo import MongoClient

from settings import *

reload(sys)
sys.setdefaultencoding('utf-8')

num = 4
tmp_num = num


def add_harvestHouses(database, count, ctable):
    global mutex, tmp_num
    query_header_houses = 'INSERT INTO houses (name, address, snd_adm, fst_adm, developer, picture, price, url) VALUES ( '

    conn = sqlite3.connect(database)  # to name it with a specific word
    cursor = conn.cursor()
    # 'select city_id, page_id, city_name, abbr, fst_adm from cities where checked = -1


    # Dividing the tasks
    q = len(ctable) / num
    i = count * q

    print "total harvesting tasks ", str(len(ctable)) + "\n"
    print "thread ", str(count), " starts from ", str(i) + "\n"
    while i < (count + 1) * q:
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
            webpage = pq(url, parse="html", headers=headers, proxies=proxies, timeout=1)
            # webpage = pq(url, parse="html", headers= headers, timeout = 1)
        except:
            # i = i + 1
            continue

        houses = webpage('.sslalone')
        mutex.acquire()
        for item in houses:
            house = {}
            house['snd_adm'] = city_name
            house['fst_adm'] = fst_adm
            house['url'] = pq(item)("div.sslaimg a").attr("href").encode('latin-1').decode('gbk')
            house['picture'] = pq(item)("div.sslaimg a img").attr("src").encode('latin-1').decode('gbk')
            house['name'] = pq(item)("div.sslaimg a img").attr("alt").encode('latin-1', 'ignore').decode('gbk', 'ignore')
            house['developer'] = pq(item)("ul.sslainfor li").eq(3).find("a").text().encode('latin-1', 'ignore').decode('gbk', 'ignore')
            house['price'] = str(pq(item)(".junjia")).encode('latin-1').decode('gbk')
            try:
                house['address'] = pq(item)("ul.sslainfor li font").attr("title").encode('latin-1', 'ignore').decode('gbk', 'ignore')
            except:
                house['address'] = pq(item)("ul.sslainfor li").eq(1).text().encode('latin-1', 'ignore').decode('gbk', 'ignore').replace(" 查看地图", "")

            query_body_houses = "'" + house['name'] + "', '" + house['address'] + "', '" + house['snd_adm'] + "', '" + house['fst_adm'] + "', '" + house['developer'] + "', '" + house['picture'] + "', '" + house['price'] + "', '" + house[
                'url'] + "')"

            try:
                cursor.execute(query_header_houses + query_body_houses)
                # conn.commit()
                # mutex.release()
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
    print "thread", str(count), " is dead. And only ", str(tmp_num), " is left."


def main(num):
    global count, mutex
    threads = []

    client = MongoClient(address, port)
    db = client[project]
    user_count = db.users.find().count()
    post_count = db.posts.find().count()



    # 创建一个锁
    # mutex = threading.Lock()
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=add_harvestHouses, args=(user_count, post_count, x)))

    # 启动所有线程
    for t in threads:
        t.start()
    ## 主线程中等待所有子线程退出
    for t in threads:
        t.join()


if __name__ == '__main__':
    main(num)
