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
import json

import mechanize
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
from pytz import timezone

from settings import *

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
    return br


def get_response(browser, url, waiting):
    rd = {}
    import httplib
    time.sleep(waiting)
    i = 0
    while rd == {} and i < 3:
        i += 1
        print "original url: %s" % url.decode("utf-8")
        try:
            rd = browser.open(url, timeout=20)
            final_url = rd.geturl().decode("utf-8")
            # print "final url: %s" % final_url
            if "login" in final_url:
                print "cookie temporarily expired."
                exit(-1)
            rd = rd.read()
        except urllib2.URLError, e:
            rd = {}
            print e
            print "urlib2 error. get_response."
        except socket.timeout, e:
            rd = {}
            print e.message
            print "get_response"
        except httplib.IncompleteRead, e:
            rd = {}
            print e.message
            print "Incompleted read."
    return rd

def parse_keyword(keyword, project, browser):
    import json
    client = MongoClient('localhost', 27017)
    db = client[project]

    # http://s.weibo.com/weibo/%25E7%2588%25B1%25E6%2583%2585&page=9
    # nodup=1 real time
    url = 'http://s.weibo.com/weibo/' + keyword.decode("utf-8")
    # print url

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
            ######################################################################
            # important here, for others, I need to design a collecting mechanism.
            update_keyword(keyword, now)
            ######################################################################
            print "Complete! Does not continue to process historical data."
            break
    print "keyword parsed."


def update_keyword(keyword, now):
    pass


def parse_post(post, keyword):
    mid = post.attrs['mid']

    username = post.find('a', class_='W_texta W_fb').attrs['title']
    print username
    try:
        userid_tmp = post.find('a', class_='W_texta W_fb').attrs['usercard']
    except KeyError, e:
        print e.message
        userid_tmp = post.find('img', class_='W_face_radius').attrs['usercard']

    userid = userid_tmp[3:userid_tmp.index("&")]

    if post.find('a', class_='approve') is None:
        user_verified = False
    else:
        user_verified = True

    content = post.find('p', class_='comment_txt').get_text()
    t = post.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']

    fwd_count = int(post.find('a', {'action-type': 'feed_list_forward'}).get_text().replace("转发", "0"))
    cmt_count = int(post.find('a', {'action-type': 'feed_list_comment'}).get_text().replace("评论", "0"))
    like_count = int("0" + post.find('a', {'action-type': 'feed_list_like'}).get_text())

    # location
    loc = ""
    if post.find('span', class_='W_btn_tag') is not None:
        if post.find('span', class_='W_btn_tag').attrs.has_key('title'):
            loc = post.find('span', class_='W_btn_tag').attrs['title']
            latlng = geocode(loc)

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
            "latlng": latlng,
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
            "verified": user_verified,
            "verified_info": '',
            "gender": "",
            "birthday": 1900,
            "location": loc,
            "latlng": latlng,
            "follower_count": 0,
            "friend_count": 0,
            "verified_info": "",
            "path": []
        }
    }

    print username, " ", t_china, " ", fwd_count, cmt_count, like_count, " ", content.decode("utf-8", "ignore").encode(
        "gbk", "ignore")
    return result_json


def parse_profile(project, keyword, browser):
    client = MongoClient('localhost', 27017)
    db = client[project]
    # STEP ONE：already got the latlng from the content
    # users = db.users.find({'latlng': [0, 0]}, no_cursor_timeout=True).limit(100)
    users = db.users.find({'$or': [{'latlng': [0, 0]}, {'path': [[0, 0, 0]]}]}).limit(100)
    for user in users:
        url = "http://weibo.cn/%s/info" % user['userid']
        rd = get_response(browser, url, 20)
        gender = ''
        birthday = 1900
        verified = False
        verified_info = ''
        loc = ''
        if rd != {}:
            f = open("parse_profile_%s.html" % user['userid'], "w")
            f.write(str(rd))
            f.close()
            tabs = BeautifulSoup(rd, 'html5lib').findAll("div", class_="c")
            for tab in tabs:
                info = tab.get_text()
                if '昵称' in info:
                    info = info.replace('认证信息：', '认信:')
                    flds = info.split(":")
                    i = 0
                    while i < len(flds) - 1:
                        if '性别' in flds[i]:
                            if '男' in flds[i + 1]:
                                gender = 'M'
                            else:
                                gender = 'F'
                                # print gender
                        if '地区' in flds[i]:
                            loc = flds[i + 1][:-2]
                            # print loc
                        if '认信' in flds[i]:
                            verified = True
                            verified_info = flds[i + 1][:-2]
                            # print verified_info
                        if '生日' in flds[i]:
                            birthday = flds[i + 1][:-2]
                            # print birthday
                        i += 1
                    if '地区' not in info:
                        loc = "none"
        else:
            continue

        print loc

        latlng = geocode(loc)
        db.users.update({'userid': user['userid']}, {'$set': {
            'gender': gender,
            'birthday': birthday,
            'loc': loc,
            'verified': verified,
            'verified_info': verified_info,
            'latlng': latlng
        }})
        print "%s %s %r %s %s %f %f" % (gender, birthday, verified, verified_info, loc, latlng[0], latlng[1])


def geocode(loc):
    lat, lng = 0, 0
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' % (loc, BAIDU_AK)
    response = urllib2.urlopen(url)
    try:
        loc_json = json.loads(response.read())
        lat = loc_json[u'result'][u'location'][u'lat']
        lng = loc_json[u'result'][u'location'][u'lng']
    except ValueError, e:
        print e.message + "No JSON object could be decoded"
    return [lat, lng]

def parse_location(project, keyword, browser):

    client = MongoClient('localhost', 27017)
    db = client[project]
    # STEP ONE：already got the latlng from the content
    # users = db.users.find({'latlng': [0, 0]}, no_cursor_timeout=True).limit(100)
    users = db.users.find({'$or': [{'latlng': [0, 0]}, {'path': [[0, 0, 0]]}]}).limit(100)
    for user in users:
        # http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=1644114654&starttime=2013-01-01&endtime=2013-12-31
        url = "http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=%s&starttime=2014-01-01" % user['userid']
        # print url
        rd = get_response(browser, url, WAITING_TIME)
        # output for testing
        f = open("parse_location_%s.html" % user['userid'], "w")
        f.write(rd)
        f.close()

        path = []
        if "noUserFeed" not in rd:
            # STEP TWO: Assigning location the path api
            posts = BeautifulSoup(rd, 'html5lib').findAll("div", class_="time_feed_box")

            for post in posts:
                # '2013-12-6 18:14'
                t = post.find("a", class_="date").get_text().lstrip()
                tzchina = timezone('Asia/Chongqing')
                if "-" in t:
                    t1 = t.split("-")
                    t2 = t1[2].split(" ")
                    t3 = t2[1].split(":")
                    t_china = datetime.datetime(int(t1[0]), int(t1[1]), int(t2[0]), int(t3[0]), int(t3[1]), 0, 0,
                                                tzinfo=tzchina)
                else:
                    t1 = t.split("æœˆ")[0]
                    t2 = t.split("æœˆ")[1].split("æ—¥")[0]
                    t3 = t.split(" ")[1].split(":")
                    t_china = datetime.datetime(2015, int(t1), int(t2), int(t3[0]), int(t3[1]), 0, 0, tzinfo=tzchina)

                # path
                if post.find("div", class_="time_map_pao2") is not None:
                    ll = post.find("div", class_="time_map_pao2")
                    # if ll.find("a", {'target': '_blank'}).attrs['href'] is not None:
                    tmp = ll.find("a", {'target': '_blank'}).attrs['href']
                    tmp = tmp.split('/')[2]
                    tmp = tmp.split(",")
                    lng = tmp[1]
                    lat = tmp[0]
                elif post.find("div", class_="time_mapsite") is not None:
                    ll = post.find("div", class_="time_mapsite")
                    tmp = ll.find("img", class_="bigcursor").attrs["onclick"]
                    tmp = tmp.split(",")
                    lat = tmp[1]
                    lng = tmp[0].split("(")[1]
                elif post.find("div", class_="time_mapsite2") is not None:
                    ll = post.find("div", class_="time_mapsite2")
                    tmp = ll.find("img", class_="bigcursor").attrs["onclick"]
                    tmp = tmp.split(",")
                    lat = tmp[1]
                    lng = tmp[0].split("(")[1]
                else:
                    lat = 0
                    lng = 0

                path.append([float(lat), float(lng), t_china])
                print lat, lng, t_china
        else:
            # 提取path
            path.append([0, 0, 0])
        db.users.update({'userid': user['userid']}, {'$set': {'path': path}})
        # 更新user 的latlng,
        # 对于post的latlng的更新，我认为可以不着急？
        latlng = [path[0][0], path[0][1]]  # 临时策略
        db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})
        #最后一个是对于本身帖子没有位置，path也没有的。

        # 针对一人多贴的情况，对个人的扫描。地址重要，所以扫了，然后每一个人的主页？？验证类型。其实可以不要。


        #所以，只去找回帖，report就好？
    pass

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


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num