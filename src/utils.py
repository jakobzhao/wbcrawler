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
import time
import sys
import os
import datetime
import json

from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import *

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

TZCHINA = timezone('Asia/Chongqing')
UTC = timezone('UTC')

reload(sys)
sys.setdefaultencoding('utf-8')


def sina_login(username, password):

    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)

    # visit the sina login page
    browser.get("https://login.sina.com.cn/")

    # input username
    # user = browser.find_element_by_id('username')
    user = WebDriverWait(browser, WAITING_TIME).until(EC.presence_of_element_located((By.ID, 'username')))
    user.send_keys(username, Keys.ARROW_DOWN)

    # input the passowrd
    passwd = browser.find_element_by_id('password')
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # press click and then the vcode appears.
    browser.find_element_by_class_name('smb_btn').click()
    vcode = browser.find_element_by_id('door')

    if vcode:
        code = raw_input("verify code:")
        if code:
            vcode.send_keys(code, Keys.ARROW_DOWN)

    browser.find_element_by_class_name('smb_btn').click()

    weibo_tab = '//*[@id="service_list"]/div[2]/ul/li[1]/a'
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, weibo_tab)))
    browser.find_element_by_xpath(weibo_tab).click()
    print "logged in successfully."
    return browser


def get_response(browser, url, waiting):
    browser.get(url)
    time.sleep(waiting)
    rd = browser.page_source
    return rd


def parse_keyword(project, keyword, browser):
    client = MongoClient('localhost', 27017)
    db = client[project]

    url = 'http://s.weibo.com/weibo/' + keyword  # + '&nodup=1'
    rd = get_response(browser, url, WAITING_TIME)
    soup = BeautifulSoup(rd, 'html5lib')

    # Test
    # f = open("../data/parse_keyword_" + toPinyin(keyword) + ".html", "w")
    # f.write(rd)
    # f.close()


    # Page number
    pages = len((soup.find('div', {'node-type': 'feed_list_page_morelist'})).findAll('li'))
    print "total pages = %d" % pages
    stop_flag = False
    for i in range(pages):
        url = 'http://s.weibo.com/weibo/' + keyword + '&page=' + str(i + 1)  # + '&nodup=1'
        print url.decode("utf-8")
        rd = get_response(browser, url, WAITING_TIME)
        soup = BeautifulSoup(rd, 'html5lib')
        posts = soup.findAll('div', {'action-type': 'feed_list_item'})

        # Test
        # f = open("../data/parse_keyword_posts" + toPinyin(keyword) + ".html", "w")
        # f.write(rd)
        # f.close()

        # posts in one page
        print "total posts = %d" % len(posts)
        for post in posts:
            json_data = parse_post(post, keyword)
            try:
                db.users.insert_one(json_data['user'])
            except errors.DuplicateKeyError, e:
                print "Duplicated user. " + e.message

            try:
                db[toPinyin(keyword)].insert_one(json_data['post'])
            except KeyError, e:
                print "BeautifulSoup does not working properly. " + e.message
            except errors.DuplicateKeyError:
                print "======Update====="
                # update
                # timestamp of a post
                # 2015-10-07 00:26:00+08:06
                timestamp = json_data['post']['timestamp']
                now = datetime.datetime.now(TZCHINA)
                delta = now - timestamp
                # (1) i = 0, the first page might have selected posts (精选),
                #            the reposts might update very often.
                # (2) delta.days < 3 flow control. Keep the program manageable,
                #            if not, too many queries if run the program for a while.
                if i == 0 or delta.days < 3:
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
    print "The keyword %s has been parsed." % keyword


def update_keyword(keyword, now):
    print keyword, now
    pass


def parse_item(post, keyword):
    userid, user_name, fwd_count, like_count, content = 0, '', 0, 0, ''
    # unique vavlue
    mid = int(post.attrs['mid'])

    # userid, username
    try:
        face_icon = post.find('div', class_="WB_face W_fl")
        userid = int(face_icon.find("a").attrs['usercard'][3:])
        user_name = face_icon.find("img").attrs['alt']
    except AttributeError, e:
        print e.message

    # verification
    if post.find('i', class_='W_icon icon_approve') is not None:
        user_verified = True
    else:
        user_verified = False

    # content
    post_content = post.find('div', class_='list_con')
    try:
        content = post_content.find('span', {'node-type': 'text'}).get_text()
    except AttributeError, e:
        print e.message

    # counts, comments number does not exist
    ul = post_content.find('ul', class_='clearfix')
    for li in ul.findAll('li'):
        txt = li.get_text().lstrip().rstrip()
        if "转发" in txt:
            fwd_count = int("0" + txt.replace("转发", "").lstrip().rstrip())
    # the last one is the like count.
    like_count = int("0" + ul.findAll("li")[-1].get_text().lstrip().rstrip())

    # timestamp
    # t = '2015-10-05 08:51'   timestamp from weibo example
    t = post_content.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']
    t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=TZCHINA)

    # location: no location information for the reposts.

    # return resultin json.
    result_json = {
        "reply": {
            "keyword": keyword,
            "mid": mid,
            "content": content.encode('utf-8', 'ignore'),
            "timestamp": t_china,
            "fwd_count": fwd_count,
            "cmt_count": 0,
            "like_count": like_count,
            "sentiment": 0,
            "user": {
                "userid": userid,
                "username": user_name.encode('utf-8', 'ignore'),
                "user_verified": user_verified,
                "location": "",
                "follower_count": 0,
                "friend_count": 0,
                "verified_info": "",
                "path": []
            },
            "comments": [],
            "replies": []
        },
        "user": {
            "userid": userid,
            "username": user_name.encode('utf-8', 'ignore'),
            "verified": user_verified,
            "verified_info": '',
            "gender": "",
            "birthday": 1900,
            "follower_count": 0,
            "friend_count": 0,
            "path": []
        }
    }

    try:
        print mid, userid, t, user_name, user_verified, fwd_count, content
    except UnicodeEncodeError, e:
        print e.message

    return result_json


def parse_post(post, keyword):
    userid, fwd_count, cmt_count, like_count, user_name = 0, 0, 0, 0, ''
    # primary key mid
    mid = int(post.attrs['mid'])

    # user_name, userid
    try:
        if post.find('img', class_='W_texta W_fb') is not None:
            user_name = post.find('img', class_='W_texta W_fb').attrs['title']
        else:
            user_name = post.find("img", class_="W_face_radius").attrs['alt']

        if "usercard" in post.find('a', class_='W_texta W_fb').attrs.keys():
            userid_tmp = post.find('a', class_='W_texta W_fb').attrs['usercard']
            userid = int(userid_tmp[3:userid_tmp.index("&")])
        elif "usercard" in post.find('img', class_='W_face_radius').attrs.keys():
            userid_tmp = post.find('img', class_='W_face_radius').attrs['usercard']
            userid = int(userid_tmp[3:userid_tmp.index("&")])
        else:
            userid_tmp = post.find('img', class_='W_face_radius').attrs['src']
            userid = int(userid_tmp.split("/")[3])
    except KeyError, e:
        print e.message

    # user verification
    if post.find('a', class_='approve') is None:
        user_verified = False
    else:
        user_verified = True

    # the content of a weibo (tweet)
    content = post.find('p', class_='comment_txt').get_text()

    # counts: relies, cmts, likes
    if post.find('a', {'action-type': 'feed_list_forward'}) is not None:
        fwd_count = int(post.find('a', {'action-type': 'feed_list_forward'}).get_text().replace("转发", "0"))
        cmt_count = int(post.find('a', {'action-type': 'feed_list_comment'}).get_text().replace("评论", "0"))
        like_count = int("0" + post.find('a', {'action-type': 'feed_list_like'}).get_text())
    else:
        lis_panel = post.find("ul", class_="feed_action_info feed_action_row4")
        lis = lis_panel.findAll("li")
        for li in lis:
            if "转发" in li.get_text():
                fwd_count = int("0" + li.get_text().replace("转发", ""))
            if "评论" in li.get_text():
                cmt_count = int("0" + li.get_text().replace("评论", ""))
            like_count = int("0" + lis[len(lis) - 1].get_text())

    # location
    loc, latlng = '', [0, 0]
    if post.find('span', class_='W_btn_tag') is not None:
        if post.find('span', class_='W_btn_tag').attrs.has_key('title'):
            loc = post.find('span', class_='W_btn_tag').attrs['title']
            latlng = geocode(loc)

    # timestamp
    # t = '2015-10-05 08:51'
    try:
        if len(post.findAll('a', {'node-type': 'feed_list_item_date'})) == 2:
            t = post.findAll('a', {'node-type': 'feed_list_item_date'})[1].attrs['title']
        else:
            t = post.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']
    except ValueError, e:
        t = datetime.datetime.now(TZCHINA)
    t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=TZCHINA)

    # build the return result in json
    result_json = {
        "post": {
            "mid": mid,
            "keyword": keyword,
            "content": content.encode('utf-8', 'ignore'),
            "timestamp": t_china,
            "fwd_count": fwd_count,
            "cmt_count": cmt_count,
            "like_count": like_count,
            "location": loc,
            "latlng": latlng,
            "sentiment": 0,
            "user": {
                "userid": userid,
                "username": user_name.encode('utf-8', 'ignore'),
                "user_verified": user_verified,
                "location": "",
                "follower_count": 0,
                "friend_count": 0,
                "verified_info": "",
                "path": []
            },
            "comments": [],
            "replies": []
        },
        "user": {
            "userid": userid,
            "username": user_name.encode('utf-8', 'ignore'),
            "verified": user_verified,
            "verified_info": '',
            "gender": "",
            "birthday": 1900,
            "location": loc,
            "latlng": latlng,
            "follower_count": 0,
            "friend_count": 0,
            "path": []
        }
    }

    try:
        print user_name, " ", t_china, " ", fwd_count, cmt_count, like_count, " ", content, "\n"
    except UnicodeEncodeError, e:
        print e.message
    return result_json


def parse_repost(project, keyword, browser):
    client = MongoClient('localhost', 27017)
    db = client[project]

    # flow control
    # As for now, only calculate the reposts with a fwd count larger than 10
    posts = db[toPinyin(keyword)].find({"fwd_count": {"$gt": 10}}).limit(100)
    for post in posts:

        # token url exmple: http://weibo.com/3693685493/CEtFjkHwM?type=repost
        token = mid_to_token(post['mid'])
        # 1. Determine the URL
        url = "http://weibo.com/%s/%s?type=repost" % (str(post['user']['userid']), token)
        print url

        # 2. Parsing the data
        rd = get_response(browser, url, WAITING_TIME)
        # test
        # f = open("../data/parse_repost_%s.html" % post['mid'], "w")
        # f.write(str(rd))
        # f.close()
        repost_panel = BeautifulSoup(rd, 'html5lib').find("div", class_="WB_feed WB_feed_profile")

        # 2.1 the counts
        # counts
        for li in repost_panel.find("div", class_="WB_handle").findAll("li"):
            txt = li.get_text().lstrip().rstrip()
            if "转发" in txt:
                fwd_count = int("0" + txt.replace("转发", "").lstrip().rstrip())
            if "评论" in txt:
                cmt_count = int("0" + txt.replace("评论", "").lstrip().rstrip())
        # the last one is the like count.
        like_txt = repost_panel.find("div", class_="WB_handle").findAll("li")[-1].get_text().lstrip().rstrip()
        like_count = int("0" + like_txt)

        # update counts when any count number changes
        if cmt_count != post['cmt_count'] or fwd_count != post['fwd_count'] or like_count != post['like_count']:
            db[toPinyin(keyword)].update({'mid': post['mid']}, {'$set': {
                'fwd_count': fwd_count,
                'cmt_count': cmt_count,
                'like_count': like_count
            }})

        # 2.2
        # harvest and flow size control
        i, num_replies, stop_flag = 0, 0, False
        while post['fwd_count'] < fwd_count or num_replies < fwd_count * 0.5:
            mid = []
            for reply in db[toPinyin(keyword)].find_one({'mid': post['mid']})['replies']:
                mid.append(reply['mid'])

            # 20% of all the reposts (even more) might be purposedly hidden by the author
            num_replies = len(mid)

            # Acquring all the repost items in a page, ignore the first one
            reposts = repost_panel.findAll("div", {'action-type': 'feed_list_item'})[1:]
            for item in reposts:

                item_json = parse_item(item, keyword)
                if item_json['reply']['mid'] not in mid:
                    # insert user
                    try:
                        db.users.insert_one(item_json['user'])

                    except errors.DuplicateKeyError, e:
                        print "Duplicated User." + e.message
                    # the time interval between the repost and the original post
                    # the first repost page might have selected replies.
                    t = str(post['timestamp'])
                    t_utc = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=UTC)
                    delta = item_json['reply']['timestamp'] - t_utc
                    if i == 0 or (post['mid'] not in mid and delta.days < 3):
                        db[toPinyin(keyword)].update(
                            {'mid': post['mid']},
                            {'$push': {'replies': item_json['reply']
                                       }
                             }
                        )
                    else:
                        print "already inserted, meaning all the previous replies has been inserted."
                        stop_flag = True
                        break

                    # insert post
                    try:
                        db[toPinyin(keyword)].insert_one(item_json['reply'])
                    except errors.DuplicateKeyError, e:
                        print "Duplicated post." + e.message

            # stop harvesting
            if stop_flag:
                print "the reposts of this post have been successfully processed."
                break

            # Turn to the next page
            page_lis = repost_panel.findAll("span", {'action-type': 'feed_list_page'})
            if len(page_lis) > 0:
                next_page = page_lis[-1].get_text()
            else:
                next_page = ''
            if next_page == '下一页':
                browser.find_element_by_link_text("下一页").click()
                # try:
                #     WebDriverWait(browser, WAITING_TIME).until(EC.staleness_of((By.CLASS_NAME, 'repeat_list')))
                # except AttributeError, e:
                #     print e.message
                # repost_panel = BeautifulSoup(browser.page_source, 'html5lib').find("div", class_= "WB_feed WB_feed_profile")
                while True:
                    time.sleep(20)
                    # WebDriverWait(browser, WAITING_TIME).until(EC.staleness_of((By.CLASS_NAME, 'repeat_list')))
                    repost_panel = BeautifulSoup(browser.page_source, 'html5lib').find("div", class_="WB_feed WB_feed_profile")
                    # pages_flag = repost_panel.findAll("a", {'action-type': 'feed_list_page'})
                    if reposts != repost_panel.findAll("div", {'action-type': 'feed_list_item'}):
                        break
            print "===============page %d============" % i
            i += 1


def parse_profile(project, keyword, browser):
    client = MongoClient('localhost', 27017)
    db = client[project]
    # STEP ONE：already got the latlng from the content
    # users = db.users.find({'latlng': [0, 0]}, no_cursor_timeout=True).limit(100)
    users = db.users.find({'$or': [{'latlng': [0, 0]}, {'path': [0, 0, 0]}]}).limit(100)
    for user in users:
        if 'location' in user.keys():
            if user['location'] == '其他' or user['location'] == '未知':
                continue
        url = "http://weibo.cn/%s/info" % user['userid']
        rd = get_response(browser, url, 20)
        gender, birthday, verified, verified_info, loc, latlng = '', 1900, False, '', '', [0, 0]

        # test
        # f = open("../data/parse_profile_%s.html" % user['userid'], "w")
        # f.write(str(rd))
        # f.close()
        tabs = BeautifulSoup(rd, 'html5lib').findAll("div", class_="c")
        for tab in tabs:
            info = tab.get_text()
            if '昵称' in info:
                info = info.replace('认证信息：', '认信:').replace('感情状况：', '感情:').replace('性取向：', '取向:')
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
                        loc = loc.replace("海外 ", "")
                    if '认信' in flds[i]:
                        verified = True
                        verified_info = flds[i + 1][:-2]
                        verified_info = verified_info.replace('官方微博', '')
                        # print verified_info
                    if '生日' in flds[i]:
                        birthday = flds[i + 1][:-2]
                        # print birthday
                    i += 1

                # location could be the very last one
                if '地区' in flds[len(flds) - 2]:
                    loc = flds[len(flds) - 1]
                # the value of 地区 could be 未知, 其他.
                if '地区' not in info:
                    loc = "未知"
                elif loc == "其他":
                    pass
                else:
                    latlng = geocode(loc)
                break

        db.users.update({'userid': user['userid']}, {'$set': {
            'gender': unicode(gender),
            'birthday': birthday,
            'location': loc,
            'verified': verified,
            'verified_info': verified_info,
            'latlng': latlng
        }})

        # print unicode(gender), birthday, verified_info, loc, latlng[0], latlng[1]
        try:
            print user['username'], loc, latlng[0], latlng[1]
        except UnicodeEncodeError, e:
            print "error" + e.message


def geocode(loc):
    lat, lng = 0, 0
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' % (loc, BAIDU_AK)
    response = urllib2.urlopen(url.replace(' ', '%20'))
    try:
        loc_json = json.loads(response.read())
        lat = loc_json[u'result'][u'location'][u'lat']
        lng = loc_json[u'result'][u'location'][u'lng']
    except ValueError, e:
        print url
        print e.message + "No JSON object could be decoded"
    except KeyError, e:
        print url
        print e.message
    return [lat, lng]


def parse_location(project, keyword, browser):

    client = MongoClient('localhost', 27017)
    db = client[project]
    # STEP ONE：already got the latlng from the content
    users = db.users.find({'$and': [{'latlng': [0, 0]}, {'path': []}]}).limit(100)

    for user in users:
        # http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=1644114654&starttime=2013-01-01&endtime=2013-12-31
        url = "http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=%s&starttime=2014-01-01" % user['userid']
        print url
        rd = get_response(browser, url, WAITING_TIME)
        # output for testing
        f = open("../data/parse_location_%s.html" % user['userid'], "w")
        f.write(rd)
        f.close()

        path = []
        if "noUserFeed" not in rd:
            # STEP TWO: Assigning location the path api
            posts = BeautifulSoup(rd, 'html5lib').findAll("div", class_="time_feed_box")

            for post in posts:
                # '2013-12-6 18:14'
                t = post.find("a", class_="date").get_text().lstrip()
                if "-" in t:
                    t1 = t.split("-")
                    t2 = t1[2].split(" ")
                    t3 = t2[1].split(":")
                    t_china = datetime.datetime(int(t1[0]), int(t1[1]), int(t2[0]), int(t3[0]), int(t3[1]), 0, 0,
                                                tzinfo=TZCHINA)
                elif "月" in t:
                    # t1 = t.split("æœˆ")[0]
                    # t2 = t.split("æœˆ")[1].split("æ—¥")[0]
                    t1 = t.split("月")[0]
                    t2 = t.split("月")[1].split("日")[0]
                    t3 = t.split(" ")[1].split(":")
                    t_china = datetime.datetime(2015, int(t1), int(t2), int(t3[0]), int(t3[1]), 0, 0, tzinfo=TZCHINA)
                else:
                    t_china = datetime.datetime.now(TZCHINA)

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
                if lat == '':
                    lat = 0
                    lng = 0
                print user['username'], lat, lng, t_china
                path.append([float(lat), float(lng), t_china])
        else:
            # 提取path
            path.append([0, 0, 0])
        db.users.update({'userid': user['userid']}, {'$set': {'path': path}})
        # 更新user 的latlng,
        # 对于post的latlng的更新，我认为可以不着急？
        latlng = [path[0][0], path[0][1]]  # 临时策略
        db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})


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
    import socket
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


def mid_to_token(midint):
    midint = str(midint)[::-1]
    size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
    result = []
    for i in range(size):
        s = midint[i * 7: (i + 1) * 7][::-1]
        s = base62_encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)