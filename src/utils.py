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
import urllib
import json
import sqlite3
import time
import sys
import os
import ssl
import socket
import cookielib

import mechanize
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors

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

    # 测评
    f = open("parse_keyword_" + toPinyin(keyword) + ".html", "w")
    f.write(rd)
    f.close()

    # html
    # c = d[d.index('"pid":"pl_weibo_direct"') + 188: d.index('"pid":"pl_weibo_relation"')-65]
    # json

    c = rd[rd.index('"pid":"pl_weibo_direct"') - 1: rd.index('"pid":"pl_weibo_relation"') - 61]
    soup = BeautifulSoup(json.loads(c)['html'], 'html5lib')
    posts = soup.findAll('div', {'action-type': 'feed_list_item'})

    # Currently, how many pages for this keyword in total
    pages = 1
    try:
        pages = len((soup.find('div', {'node-type': 'feed_list_page_morelist'})).findAll('li'))
    except:
        # 可缩短下次对同一个词搜索的时间间隙
        print "the total page number was not acquired. Probably need to try again."

    print "total pages = %d" % pages

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
            except errors.DuplicateKeyError, e:
                #
                # 如果这个程序只是负责加入新的数据，那么，（1）一旦发现duplicated，就停止，(或者把过去二十四小时内的搜索完毕)，要进行数据更新。（2）紧接着，转入基于时间的搜索，查看之前的页面，更新。
                # 第一天的，可以从s.weibo.com入口更新，之后，可以只是抓取页面。或者说抓取页面一般从第二天开始。这样更好一些。发现哪些是高频的，低频的只需要做为数不多的次数。
                # 可见，针对回帖的搜索，之后一点会好。
                #
                #
                # ======启动Update=====
                # 先判断段数据的

                # 一旦有duplicated 就准备要停止，怎么停止？再做24小时。
                #
                print e.message

            except KeyError, e:
                print e.message + ". BeautifulSoup does not working properly."

    print "keyword parsed."


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
    # t = '2015-10-05 08:51'   timestamp from weibo example
    import datetime
    from pytz import timezone

    tzchina = timezone('Asia/Chongqing')
    utc = timezone("UTC")
    t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0,
                                tzinfo=tzchina)
    t_utc = t_china.replace(tzinfo=tzchina).astimezone(utc)
    result_json = {
        "post": {
            "keyword": keyword,
            "mid": mid,
            "content": content,
            "timestamp": t_china,
            "location": "",
            "fwd_count": fwd_count,
            "cmt_count": cmt_count,
            "like_count": like_count,
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

def getResponseObject(url):
    request = urllib2.Request(url=url)
    content = "{}"
    msg = 'Something wrong with this crawler server.'
    #print url
    #time.sleep(1)
    try:
        response = urllib2.urlopen(request, timeout = 5)
        content = response.read()
    except urllib2.URLError, e:
        msg = msg + '\n' + url + '\n' + str(e)
        if str(e) == 'HTTP Error 403: Forbidden':
            #over the limits
            #sendEmail('jakobzhao@gmail.com', msg, '')
            print "this service has been shut down."
            sys.exit(0)
        if str(e) == 'HTTP Error 400: Bad Request':
            sendEmail('jakobzhao@gmail.com', msg, '')
            print "this service has been shut down."
            sys.exit(0)
    except ssl.SSLError,e:
        msg = msg + '\n' + url + '\n' + str(e)
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
    if 'error' in json.loads(content):
        msg = msg + json.loads(content)['error'] + '\n' + url
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
        sys.exit(0)
    try:
        obj = json.loads(content)
    except ValueError, e:
        print "********************************************"
        print "the content of the response is:" + content
        obj = json.loads('{}')
        print  "json loading value error!", e.args[0]
    return obj

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

#page will start from 1
def searchTermsFromUser(uid, terms, database, page):
    #heuristic searching
    #if topic ="", then it means to search all the statuses of this weibo.
    obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=1&uid=' + str(uid) + '&page=1&access_token=' + TOKEN)
    total_number = obj['total_number']
    while total_number >= COUNT2 * page:
        print "----------------------------Page" + str(page) + " starts----------------------------"
        obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=' + str(COUNT2)  + '&uid=' + str(uid) + '&page=' + str(page) +'&access_token=' + TOKEN)
        if obj == {}:
            continue
        for status in obj['statuses']:
            #if this status is related to the topic, then get it in.
            flag = False
            for term in terms:
                flag = flag or (term in status['text'])
            if flag and ('deleted' not in status.keys()):
                print status['text']
                processStatus(database, status)

        page = page + 1
        if page * COUNT2 > obj['total_number']:
            completed = 1
        else:
            completed = page * COUNT2/float(obj['total_number'])
        print "----------------------------Page" + str(page-1) + " ends.----------------------------"
        print "----------------------Retrieving Statuses:" +  str(round(completed*100,2)) + "%----------------------"
    print "Totally Finished!"

def processStatus(database, status):
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    keys = status.keys()

    if 'thumbnail_pic' not in keys:
        status['thumbnail_pic'] = 'None'
    if str(status['geo']) == '':
        status['geo'] = 'None'
    if str(status['geo']) != 'None':
        status['geo'] = str(status['geo']['coordinates'][0]) + "," + str(status['geo']['coordinates'][1])

    ############################statuses################################
    query_body_statuses = str(status['id']) + ", 0, '" + status['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(status['created_at']) + "')" + ", '" + status['source'] + "', '" + str(status['geo']) +  "', '" + status['thumbnail_pic'] + "', '" + str(status['user']['id']) +  "', '" + status['user']['screen_name'] + "', " + str(status['reposts_count']) +  ", " + str(status['comments_count']) + ")"
    try:
        cursor.execute(query_header_statuses + query_body_statuses)
    except sqlite3.Error, e:
        #print  "This status has already been inserted.", e.args[0]
        pass
    
    ############################users################################  
    query_body_users   = str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', '" + str(status['user']['province']) + "', '" + str(status['user']['city']) + "', '" + status['user']['location'] + "', '" + status['user']['description'].replace("'", "''") + "', '" + status['user']['url'] + "', '" + status['user']['profile_image_url'] + "', '" + status['user']['profile_url'] + "', '" + status['user']['domain'] + "', '" + str(status['user']['weihao']) + "', '" + status['user']['gender'] + "', " + "datetime('" +  parseTime(status['user']['created_at']) + "')" + ", '" + str(status['user']['geo_enabled']) + "', '" + str(status['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + status['user']['verified_reason'] + "', '" + status['user']['lang'] + "', " + str(status['user']['bi_followers_count']) + ", " + str(status['user']['followers_count']) + ", " + str(status['user']['friends_count']) + ", " + str(status['user']['statuses_count']) + ", " + str(status['user']['favourites_count']) + ")"
    try:
        cursor.execute(query_header_users + query_body_users)
    except sqlite3.Error, e:
        #print  "This user has already been inserted.", e.args[0]
        pass
    
    ############################retweets################################
    if 'retweeted_status' in keys:
        cursor.execute("update statuses set status_type=1 where id == " + str(status['id']))
        if 'user' in status['retweeted_status'].keys():
            query_body_retweets = str(status['retweeted_status']['id'] + status['id']) + ", 1," + str(status['retweeted_status']['id']) + ", " + str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', " + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + "datetime('" +  parseTime(status['created_at']) + "')"  + ")"
            try:
                cursor.execute(query_header_retweets + query_body_retweets)
            except sqlite3.Error, e:                    
                #print  "This retweeted relationship has already been inserted.", e.args[0]
                pass

            query_body_users = str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', '" + str(status['retweeted_status']['user']['province']) + "', '" + str(status['retweeted_status']['user']['city']) + "', '" + status['retweeted_status']['user']['location'] + "', '" + status['retweeted_status']['user']['description'].replace("'", "''") + "', '" + status['retweeted_status']['user']['url'] + "', '" + status['retweeted_status']['user']['profile_image_url'] + "', '" + status['retweeted_status']['user']['profile_url'] + "', '" + status['retweeted_status']['user']['domain'] + "', '" + str(status['retweeted_status']['user']['weihao']) + "', '" + status['retweeted_status']['user']['gender'] + "', " + "datetime('" +  parseTime(status['retweeted_status']['user']['created_at']) + "')" + ", '" + str(status['retweeted_status']['user']['geo_enabled']) + "', '" + str(status['retweeted_status']['user']['verified']) + "', '" + status['retweeted_status']['user']['avatar_large'] + "', '" + status['retweeted_status']['user']['verified_reason'] + "', '" + status['retweeted_status']['user']['lang'] + "', " + str(status['retweeted_status']['user']['bi_followers_count']) + ", " + str(status['retweeted_status']['user']['followers_count']) + ", " + str(status['retweeted_status']['user']['friends_count']) + ", " + str(status['retweeted_status']['user']['statuses_count']) + ", " + str(status['retweeted_status']['user']['favourites_count']) + ")"
            try:
                cursor.execute(query_header_users + query_body_users)
            except sqlite3.Error, e:
                #print  "This user has already been inserted.", e.args[0]
                pass

    ############################reposts##############################
    if status['reposts_count'] != 0:
        reposts_max_id = 0
        n = 0
        while status['reposts_count'] >= COUNT * n:
            if (n+1)*COUNT > status['reposts_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['reposts_count'])
            #print "Retrieving Reposts:" +  str(completed*100) + "%"
            n = n + 1
            reposts_obj = getResponseObject('https://api.weibo.com/2/statuses/repost_timeline.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(reposts_max_id) + '&access_token=' + TOKEN)
            if reposts_obj == {} or reposts_obj == []:
                continue
            reposts_max_id = reposts_obj['next_cursor']
            for repost in reposts_obj['reposts']:
                keys_repost = repost.keys()
                
                if 'deleted' in keys_repost:
                    continue
                if str(repost['geo']) == '':
                    repost['geo'] = 'None'
                if str(repost['geo']) != 'None' :
                    repost['geo'] = str(repost['geo']['coordinates'][0]) + "," + str(repost['geo']['coordinates'][1])
                
                query_body_retweets  = str(repost['id'] + status['id']) + ", 1," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(repost['id']) + ", " + str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ")"
                query_body_statuses = str(repost['id']) + ", 1, '" + repost['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ", '" + repost['source'] + "', '" + str(repost['geo']) +  "', '" + "None" +  "', '" + str(repost['user']['id']) +  "', '" + repost['user']['screen_name'] + "', " + str(repost['reposts_count']) +  ", " + str(repost['comments_count']) + ")"
                
                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This repost relationship has been inserted,", e.args[0]
                    pass
                
                try:
                    cursor.execute(query_header_statuses + query_body_statuses)
                except sqlite3.Error, e:
                    #print  "This repost has already been inserted.", e.args[0]
                    pass
                    
                query_body_users   = str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', '" + str(repost['user']['province']) + "', '" + str(repost['user']['city']) + "', '" + repost['user']['location'] + "', '" + repost['user']['description'].replace("'", "''") + "', '" + repost['user']['url'] + "', '" + repost['user']['profile_image_url'] + "', '" + repost['user']['profile_url'] + "', '" + repost['user']['domain'] + "', '" + str(repost['user']['weihao']) + "', '" + repost['user']['gender'] + "', " + "datetime('" +  parseTime(repost['user']['created_at'])  + "')" + ", '" + str(repost['user']['geo_enabled']) + "', '" + str(repost['user']['verified']) + "', '" + repost['user']['avatar_large'] + "', '" + repost['user']['verified_reason'] + "', '" + repost['user']['lang'] + "', " + str(repost['user']['bi_followers_count']) + ", " + str(repost['user']['followers_count']) + ", " + str(repost['user']['friends_count']) + ", " + str(repost['user']['statuses_count']) + ", " + str(repost['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

    ############################comments################################
    if status['comments_count'] != 0:
        #print 'comments:' + str(status['comments_count'])
        #print str(status['id'])        
        comments_max_id = 0
        n = 0
        while status['comments_count'] >= COUNT*n:
            if (n+1)*COUNT > status['comments_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['comments_count'])
            #print "Retrieving Comments:" +  str(completed*100) + "%"
            n = n + 1 
            #time.sleep(2) #helpful when try to limit the request to a certain amount
            comments_obj = getResponseObject('https://api.weibo.com/2/comments/show.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(comments_max_id) + '&access_token=' + TOKEN)
            if comments_obj == {}:
                continue
            comments_max_id = comments_obj['next_cursor']
                            
            for comment in comments_obj['comments']:
                keys_comment = comment.keys()
                query_body_retweets  = str(comment['id'] + status['id']) + ", 2," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ")"
                query_body_comments = str(comment['id']) + ", 2, '" + comment['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ", '" + comment['source'] + "', '" + str(comment['user']['id']) +  "', '" + comment['user']['screen_name'] + "')"
                                    
                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This comment relationship has already been inserted.", e.args[0]
                    pass
                
                try:
                    cursor.execute(query_header_comments + query_body_comments)
                except sqlite3.Error, e:
                    #print  "This comment has already been inserted.", e.args[0]
                    pass

                query_body_users   = str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', '" + str(comment['user']['province']) + "', '" + str(comment['user']['city']) + "', '" + comment['user']['location'] + "', '" + comment['user']['description'].replace("'", "''") + "', '" + comment['user']['url'] + "', '" + comment['user']['profile_image_url'] + "', '" + comment['user']['profile_url'] + "', '" + comment['user']['domain'] + "', '" + str(comment['user']['weihao']) + "', '" + comment['user']['gender'] + "', " + "datetime('" +  parseTime(comment['user']['created_at'])  + "')" + ", '" + str(comment['user']['geo_enabled']) + "', '" + str(comment['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + comment['user']['verified_reason'] + "', '" + comment['user']['lang'] + "', " + str(comment['user']['bi_followers_count']) + ", " + str(comment['user']['followers_count']) + ", " + str(comment['user']['friends_count']) + ", " + str(comment['user']['statuses_count']) + ", " + str(comment['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

                if 'reply_comment' in keys_comment:
                    query_body_retweets  = str(comment['id'] + comment['reply_comment']['id']) + ", 3," + str(comment['reply_comment']['id']) + ", " + str(comment['reply_comment']['user']['id']) + ", '" + comment['reply_comment']['user']['screen_name'] + "', "  +  str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] +  "', datetime('" +  parseTime(comment['created_at']) + "') )"
                    try:
                        cursor.execute(query_header_retweets + query_body_retweets)
                    except sqlite3.Error, e:
                        #print  "This reply-comment relationship has already been inserted.", e.args[0]
                        pass
    #t = t + 1
    #print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (t-1)*100/4) + '%' + '--------------------------------------'
    conn.commit()
    conn.close()
    
def parseTime(timestring):
    struct_time = time.strptime(timestring, '%a %b %d %H:%M:%S +0800 %Y')
    return time.strftime('%Y-%m-%d %H:%M:%S',struct_time)

def processTerms(terms, pages, database):
    for term in terms:
        processTerm(term, pages, database)

def processTerm(term, pages, database):
    i = 0
    while i < pages:
        i = i + 1
        obj = getResponseObject('https://api.weibo.com/2/search/topics.json?source=2933540621&q='+ urllib.quote(term) + '&count=50&page=' + str(i))
        if obj == {}:
            continue
        t = 0
        for status in obj['statuses']:
            if 'deleted' not in status.keys():
                processStatus(database, status)
            t = t + 1
            print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (i-1)*100/4) + '%' + '--------------------------------------'    
    print "Congrat! it's done!"