# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

import urllib2
import sqlite3
import time
import sys
import os
import socket
import cookielib
import datetime

import mechanize
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
from pytz import timezone

from settings import *

query_header_statuses  = 'INSERT INTO statuses  (id, status_type, text, created_at, source, geo, thumbnail_pic, user_id, user_screen_name, reposts_count, comments_count) VALUES ( '
query_header_comments  = 'INSERT INTO statuses  (id, status_type, text, created_at, source, user_id, user_screen_name) VALUES ( '
query_header_users     = 'INSERT INTO users     (id, screen_name, province, city, location, description, url, profile_image_url, profile_url, domain, weihao, gender, created_at, geo_enabled, verified, avatar_large, verified_reason, lang, bi_followers_count, followers_count, friends_count, statuses_count, favourites_count) VALUES ( '
query_header_retweets  = 'INSERT INTO retweets  (id, retweet_type, from_status_id, from_status_user_id, from_status_user_screen_name, to_status_id, to_status_user_id,to_status_user_screen_name, created_at) VALUES ( '



reload(sys)
sys.setdefaultencoding('utf-8')
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]


def weibo_manual_login():
    username = "vcjmi41976504@126.com"

    password = "zx1987"

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)

    browser.get("http://weibo.com/login.php")

    user = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[1]/div/input')
    user.send_keys(username, Keys.ARROW_DOWN)

    passwd = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[2]/div/input')
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # //*[@id="pl_login_form"]/div[3]/div[2]/div[3]/div/input
    browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[6]').click()
    vcode = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[3]/div/input')
    if vcode:
        code = raw_input("verify code:")
        if code:
            vcode.send_keys(code, Keys.ARROW_DOWN)

    browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[6]').click()
    print "login successfully."
    browser.get("http://s.weibo.com/weibo/政府")
    return browser


def weibo_login():

    br = mechanize.Browser()
    #cookie jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    #加上各种协议
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    # br.set_proxies({"http": "165.139.179.225:8080"})
    #加上自己浏览器头部，和登陆了通行证的cookie
    br.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'),('Cookie',ck) ]

    # for f in br.forms():
    #     print f
    # br.select_form(nr=0)
    # print br
    # br.form['username']='13580491531'
    # br.form['password']='buhui1314iliting'
    # br.submit()
    # br.add_password('http://login.sina.com.cn/signup/signin.php?entry=sso','13580491531','buhui1314iliting')
    #登陆新浪通行证
    br.open('http://login.sina.com.cn/signup/signin.php?entry=sso')
    # a = br.request.unredirected_hdrs['Cookie']
    # a = a[a.index("SGUID=")+6:a.index("ArtiFSize")-1]
    # print a
    return(br)


def get_response(browser, url, waiting):
    rd = {}
    while rd == {}:
        time.sleep(waiting)
        try:
            # rd = browser.open("http://weibo.cn/search/mblog?keyword=" + keyword, timeout=20)
            rd = browser.open(url, timeout=20)
            # a = browser.request.unredirected_hdrs['Cookie']
            # a = a[a.index("SGUID=")+6:a.index("ArtiFSize")-1]
            # print a
            # rd = browser.open('http://s.weibo.com/weibo/%25E5%259C%25B0%25E6%2596%25B9%25E6%2594%25BF%25E5%25BA%259C&page=10' + keyword, timeout=20)
            # time.sleep(2)
            rd = rd.read()
        except urllib2.URLError, e:
            rd = {}
            print e.reason + "urlib2 error."
        except socket.timeout, e:
            rd = {}
            print e.message

            # url_raw = urllib.unquote(rd.geturl())
            # print url_raw.decode("utf-8", "ignore")

            # if "login.sina.com.cn/sso/login.php" in url_raw:
            #     #time.sleep(4)
            #     # http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fs.weibo.com%2Fweibo%2F%E8%85%90%E8%B4%A5&_rand=1444204219.5002&gateway=1&service=weibo&entry=miniblog&useticket=1&returntype=META&_client_version=0.6.12
            #     #rd = browser.open(url_raw, timeout=20)
            #     #rd = browser.open(url_raw.decode("utf-8"), timeout=20)
            #     rd = browser.open(url_raw[url_raw.index("url=") + 4:], timeout=20)
            #     #rd = browser.open('http://s.weibo.com/weibo/' + keyword, timeout=30)
            #     print rd.geturl().decode("utf-8") + " again"
    return rd

def parse_keyword(keyword, browser, project):
    import json
    client = MongoClient('localhost', 27017)
    db = client[project]

    url = 'http://s.weibo.com/weibo/' + keyword.decode("utf-8")
    print url

    rd = get_response(browser, url, WAITING_TIME)

    # output for testing
    f = open("parse_keyword_" + toPinyin(keyword) + ".html", "w")
    f.write(rd)
    f.close()

    c = rd[rd.index('"pid":"pl_weibo_direct"') - 1: rd.index('"pid":"pl_weibo_relation"') - 61]
    soup = BeautifulSoup(json.loads(c)['html'], 'html5lib')


    # Get the number of the pages
    pages = 1
    try:
        pages = len((soup.find('div', {'node-type': 'feed_list_page_morelist'})).findAll('li'))
    except:
        # 可缩短下次对同一个词搜索的时间间隙
        print "the total page number was not acquired. Probably need to try again."

    print "total pages = %d" % pages
    stop_flag = False

    for i in range(pages):
        url = 'http://s.weibo.com/weibo/' + keyword + '&page=' + str(i + 1)
        print url.decode("utf-8")
        rd = get_response(browser, url, WAITING_TIME)
        # repeated code start
        c = rd[rd.index('"pid":"pl_weibo_direct"') - 1: rd.index('"pid":"pl_weibo_relation"') - 61]
        soup = BeautifulSoup(json.loads(c)['html'], 'html5lib')
        posts = soup.findAll('div', {'action-type': 'feed_list_item'})
        # repeated code end

        print "total posts = %d" % len(posts)
        for post in posts:
            json_data = parse_post(post, keyword)
            try:
                post_return = db[toPinyin(keyword)].insert_one(json_data['post'])
                user_return = db.users.insert_one(json_data['user'])
            except KeyError, e:
                print e.message + ". BeautifulSoup does not working properly."
            except errors.DuplicateKeyError, e:
                print e.message
                # the first page may have selected post from days ago. or the post was published within a day, still update and run.
                if i == 0 or delta.days < 1:
                    # update
                    # obtain the timestamp of a post
                    # 2015-10-07 00:26:00+08:06  Beiing Time, therefore, when comparing, I have to change the local time to beijing time.
                    tzchina = timezone('Asia/Chongqing')
                    timestamp = json_data['post']['timestamp']
                    # post_time = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=tzchina)
                    # What is the time now? pay attention to the time zone differences.
                    tzchina = timezone('Asia/Chongqing')
                    now = datetime.datetime.now(tzchina)
                    delta = now - timestamp
                    # the second time constraint, if the post was published within one day, update the post.
                    if delta.days < 1:
                        db[toPinyin(keyword)].update({'mid': json_data['post']['mid']},
                                                     {'$set': {'fwd_count': json_data['post']['fwd_count'],
                                                               'cmd_count': json_data['post']['cmt_count'],
                                                               'like_count': json_data['post']['like_count'],
                                                               }
                                                      })
                else:
                    stop_flag = True
                    break
        if stop_flag:
            # important here, for others, I need to design a collecting mechanism.
            update_keyword(keyword, now)
            print "Complete! Does not continue to process historical data."
            break
    print "keyword parsed."


def update_keyword(keyword, now):
    pass
def parse_post(post, keyword):
    mid = post.attrs['mid']

    username = post.find('a', class_='W_texta W_fb').attrs['title']
    userid = post.find('a', class_='W_texta W_fb').attrs['href'][19:]

    if post.find('a', class_='approve') == None:
        user_verified = False
    else:
        user_verified = True

    content = post.find('p', class_='comment_txt').get_text()
    t = post.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']

    fwd_count = int(post.find('a', {'action-type': 'feed_list_forward'}).get_text().replace("转发", "0"))
    cmt_count = int(post.find('a', {'action-type': 'feed_list_comment'}).get_text().replace("评论", "0"))
    like_count = int("0" + post.find('a', {'action-type': 'feed_list_like'}).get_text())

    # location
    if post.find('span', class_='W_btn_tag') == None:
        loc = ""
    else:
        loc = post.find('span', class_='W_btn_tag').attrs['title']

    # t = '2015-10-05 08:51'   timestamp from weibo example
    tzchina = timezone('Asia/Chongqing')
    # utc = timezone("UTC")
    t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0,
                                tzinfo=tzchina)
    # t_utc = t_china.replace(tzinfo=tzchina).astimezone(utc)
    result_json = {
        "post": {
            "keyword": keyword,
            "mid": mid,
            "content": content,
            "timestamp": t_china,
            "fwd_count": fwd_count,
            "cmt_count": cmt_count,
            "like_count": like_count,
            "location": loc,
            "sentiment": 0,
            "user": {
                "userid": userid,
                "username": username,
                "user_verified": user_verified,
                "location": "",
                "follower_count": 0,
                "friend_count": 0,
                "verified_info": "",
                "path": []
            },
            "comments": [],
            "reply": []
        },
        "user": {
            "userid": userid,
            "username": username,
            "user_verified": user_verified
        }
    }

    print username, " ", t_china, " ", fwd_count, cmt_count, like_count, " ", content.decode("utf-8", "ignore").encode(
        "gbk", "ignore")
    return result_json

# hanzi to pinyin
def toPinyin(keyword):
    from pypinyin import lazy_pinyin
    py = lazy_pinyin(unicode(keyword))
    result = ''
    for i in py:
        result += i
    return result


def sendEmail(reciever, msg):
    import smtplib
    sender = 'snsgis@gmail.com'
    username = 'snsgis@gmail.com'

    msg = '''From: Crawler Server <snsgis@gmail.com>
To: Administrator <''' + reciever + '''>
Subject: Warning from Crawler Server
MIME-Version: 1.0

To whom it concerns,

''' + msg + '''
--
sent from crawler server
notice: Please don't reply to this email, nobody would notice your email. However, don't hesitate to 
contact the administrator Bo Zhao <jakobzhao@gmail.com> at your convenience.
'''
    # The actual mail send
    try:
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com','587')
        server.ehlo()
        server.starttls()
        server.login(username, EMAIL_PASSWORD)
        server.sendmail(sender, reciever, msg)
        server.quit()
    except socket.gaierror, e:
        print str(e) + "/n error raises when sending E-mails."


def geocoding(database):
    from pygeocoder import Geocoder
    #Variables    
    
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    cursor.execute('select id, location, lat, lng from users')
    user_locs = cursor.fetchall()
    
    conn2 = sqlite3.connect(current_path + '/' + 'gazetteers.db')
    cursor2 = conn2.cursor()
    cursor2.execute('select id, location, lat, lng from gazetteers')
    gazetteers = cursor2.fetchall()
    
    a = {}
    for gazetteer in gazetteers:
        a[gazetteer[1]] = (gazetteer[0],gazetteer[2],gazetteer[3])
    i = 0
    p = 0
    while i < len(user_locs):
        if user_locs[i][2] == None:
            if user_locs[i][1] in a.keys():
                cursor.execute('update users set lat = '+ str(a[user_locs[i][1]][1]) +', lng = ' + str(a[user_locs[i][1]][2]) + ' where id == ' + str(user_locs[i][0]))
                user_locs[i] = (user_locs[i][0],user_locs[i][1], a[user_locs[i][1]][1], a[user_locs[i][1]][2])
            else:
                s = user_locs[i][1].replace('其他', '').replace('海外','')
                coordinates = Geocoder.geocode(s)  
                time.sleep(1)
                cursor.execute('update users set lat = '+ str(coordinates.coordinates[0]) +', lng = ' + str(coordinates.coordinates[1]) + ' where id == ' + str(user_locs[i][0]))
                user_locs[i] = (user_locs[i][0],user_locs[i][1],coordinates.coordinates[0],coordinates.coordinates[1])
                p = p + 1
                try:
                    cursor2.execute('insert into gazetteers (location, lat, lng) values( "' + user_locs[i][1] + '", ' + str(coordinates.coordinates[0]) + ',' + str(coordinates.coordinates[1])  + ')')
                except sqlite3.Error, e:
                    print  "This gazetteer has been inserted.", e.args[0]
            print "i = " + str(i) + ", p = " + str(p)
            j = 0
            while j< len(user_locs):
                if user_locs[j][2] == None:
                    if user_locs[j][1] == user_locs[i][1]:
                        user_locs[j] = (user_locs[j][0],user_locs[j][1], user_locs[i][2], user_locs[i][3])
                        cursor.execute('update users set lat = '+ str(user_locs[i][2]) +', lng = ' + str(user_locs[i][3]) + ' where id == ' + str(user_locs[j][0]))
                        #print 'update users set lat = '+ str(user_locs[i][2]) +', lng = ' + str(user_locs[i][3]) + ' where id == ' + str(user_locs[j][0])
                j = j + 1
        i = i + 1
    conn2.commit()
    conn2.close()
    conn.commit()
    conn.close()
    print "Successfully geocode the tabels!"
    return True

def getOpinionLeadersByDelphi(score_threshold,database):
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    #                       0              1            2            3
    cursor.execute('select id, followers_count, friends_count, verified from users')
    users = cursor.fetchall()
    opinion_leaders = []

    import math
    for user in users:
        score = 0
        if user[3] == 'True':
            score = 3
        else:
            score = 0
        #==========================Calculating the Score============================
        score = round(score + math.log10(float(user[1])/float(user[2]+1)), 2)
        #===========================================================================
        #print score
        if score >= score_threshold:
            opinion_leaders.append({'id': user[0],'score':score})
    
    print 'The list of opinon leaders: ' + str(opinion_leaders)
    #print opinion_leaders[0]['id']
    conn.commit()
    conn.close()            
    return opinion_leaders

def getOpinionLeadersByCentrality(num, database):
    import networkx as nx
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    cursor.execute('select id, source, target from user_edges')
    edges = cursor.fetchall()
    cursor.execute('select id, node from user_nodes')
    nodes = cursor.fetchall()
    conn.commit()
    conn.close()

    G = nx.DiGraph()
    for node in nodes: 
        G.add_node(node[0])
    for edge in edges: 
        G.add_edge(edge[1],edge[2]) 
    
    centrality = nx.degree_centrality(G)
    sorted_centrality = sorted(centrality.items(), key=lambda centrality:centrality[1])[-1*num:]
    return sorted_centrality
