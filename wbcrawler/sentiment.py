# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import urllib
import json
import requests
import sys
from settings import TENCENT_SECRET_ID, TENCENT_SECRET_KEY, RE_EQUALTO, RE_STARTWITH
from log import *
import datetime

# https://wenzhi.api.qcloud.com/v2/index.php?Action=TextSentiment&Nonce=345122&Region=sz&SecretId=AKIDkK8N0pa9JwjCtALjuFqhiti6xYeebSJ6&Timestamp=1408704141&Signature=MpSkDDMYmbsYsYJPozJYD42PcjvBPaZp&content=双万兆服务器就是好，只是内存小点

reload(sys)
sys.setdefaultencoding('utf-8')
from pymongo import MongoClient
import time
from math import fabs
import mechanize
import random
from urllib2 import URLError
from httplib import BadStatusLine
from socket import timeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

address = 'localhost'
port = 27017
project = 'five'


def tencent_sentiment(id, robot_num, project, address, port):
    TIMEOUT = 10
    url = "http://182.254.136.27/yunapi/tools/index.php"
    browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')
    client = MongoClient(address, port)
    search_json = {'msg': {'$eq': ''}}
    count = client[project].posts.find(search_json).count()
    slc = count / robot_num
    posts = client[project].posts.find(search_json).skip(count * id / robot_num).limit(slc)
    count /= robot_num
    log(NOTICE, "Total #: %d" % count)
    i = 0
    for post in posts:
        post = client[project].posts.find_one({'mid': post['mid']})
        if post['msg'] != '':
            continue
        i += 1
        c = post['content']
        stop = False
        round_start = datetime.datetime.now()
        for re in RE_EQUALTO:
            if c == re:
                log(NOTICE, c.encode('gbk', 'ignore'))
                stop = True
                client[project].posts.update({'mid': post['mid']}, {'$set': {'msg': 'Processed. A Reply'}})
                break
        if stop:
            continue
        for re in RE_STARTWITH:
            if c[:len(re)] == re:
                log(NOTICE, c.encode('gbk', 'ignore'))
                stop = True
                client[project].posts.update({'mid': post['mid']}, {'$set': {'msg': 'Processed. A Reply'}})
                break
        if stop:
            continue
        rdm = random.randint(0, 999999999)
        timestamp = str(int(time.time()))
        try:
            browser.get(url)
            requst_id = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.NAME, 'requestSecretId')))
            requst_id.clear()
            requst_id.send_keys(TENCENT_SECRET_ID, Keys.ARROW_DOWN)

            # input the passowrd
            secret_key = browser.find_element_by_name('requestSecretKey')
            secret_key.clear()
            secret_key.send_keys(TENCENT_SECRET_KEY, Keys.ARROW_DOWN)

            browser.find_elements_by_css_selector("input[type='radio'][value='GET']")[0].click()
            request_domain = browser.find_element_by_name('requestDomain')
            request_domain.clear()
            request_domain.send_keys('wenzhi.api.qcloud.com', Keys.ARROW_DOWN)

            request_interface = browser.find_element_by_name('requestInterfaceName')
            request_interface.clear()
            request_interface.send_keys('TextSentiment', Keys.ARROW_DOWN)

            request_region = browser.find_element_by_name('requestRegion')
            request_region.clear()
            request_region.send_keys('sz', Keys.ARROW_DOWN)

            request_params = browser.find_element_by_name('requestParams')
            request_params.clear()
            request_params.send_keys('Action=TextSentiment&Nonce=%d&Timestamp=%s&content=%s' % (rdm, timestamp, c), Keys.ARROW_DOWN)

            # press click and then the vcode appears.
            browser.find_element_by_class_name('tsubmit').click()

        except URLError:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue
        except BadStatusLine:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue
        except timeout:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue
        r = browser.page_source
        try:
            result = r.split(u"请求结果")[1][51:-15]
        except IndexError:
            continue
        sentiment = json.loads(result)
        # print sentiment
        try:
            sentiment['code']
        except TypeError:
            continue

        if sentiment['code'] == 0:
            neg = float(sentiment['negative'])
            pos = float(sentiment['positive'])
            msg = sentiment['message']
            client[project].posts.update({'mid': post['mid']}, {'$set': {'pos': pos, 'neg': neg, 'msg': 'Processed.' + msg}})
            try:
                log(NOTICE, "#%d, %d remains. time: %d sec(s). %s, %s" % (i, count - i, int((datetime.datetime.now() - round_start).seconds), result, c.encode('utf-8', 'ignore')))
            except UnicodeDecodeError:
                pass
            except UnicodeEncodeError:
                pass
        else:
            client[project].posts.update({'mid': post['mid']}, {'$set': {'msg': 'Processed. Warning'}})
            log(NOTICE, "#%d, %d remains. time: %d sec(s). A Warning: %s, %s" % (i, count - i, int((datetime.datetime.now() - round_start).seconds), result, c.encode('utf-8', 'ignore')))
    browser.close()
    log(NOTICE, 'Mission compeltes.')


def tencent_sentiment_2(project, address, port):
    client = MongoClient(address, port)
    search_json = {'msg': {'$ne': ''}}
    count = client[project].posts.find(search_json).count()
    posts = client[project].posts.find(search_json)
    log(NOTICE, "Total #: %d" % count)
    i = 0
    for post in posts:
        round_start = datetime.datetime.now()
        i += 1
        replies = post['replies']
        if len(replies) == 0:
            continue
        pos = post['pos']
        neg = post['neg']
        for reply in replies:
            search_json = {'mid': reply['mid']}
            repost = client[project].posts.find_one(search_json)
            if repost is not None:
                c = repost['content']
            else:
                continue
            find = False
            for re in RE_EQUALTO:
                if c == re:
                    log(NOTICE, c.encode('gbk', 'ignore'))
                    find = True
                    client[project].posts.update({'mid': reply['mid']}, {'$set': {'pos': pos, 'neg': neg, 'msg': 'Processed.'}})
                    break
            if find:
                continue
            for re in RE_STARTWITH:
                if c[:len(re)] == re:
                    log(NOTICE, c.encode('gbk', 'ignore'))
                    find = True
                    client[project].posts.update({'mid': reply['mid']}, {'$set': {'pos': pos, 'neg': neg, 'msg': 'Processed.'}})
                    break
            if find:
                continue

        log(NOTICE, "#%d, %d remains. time: %d sec(s)." % (i, count - i, int((datetime.datetime.now() - round_start).seconds)))
    log(NOTICE, 'Mission compeltes.')


def tencent_sentiment_3(project, address, port):
    client = MongoClient(address, port)
    search_json = {'msg': {'$ne': ''}}
    count = client[project].posts.find(search_json).count()
    posts = client[project].posts.find(search_json)
    log(NOTICE, "Total #: %d" % count)
    i = 0
    for post in posts:
        round_start = datetime.datetime.now()
        i += 1
        pos = float(post['pos'])
        neg = float(post['neg'])

        if fabs(pos - 0) < 0.000001 and fabs(neg - 0) < 0.000001:
            client[project].posts.update({'mid': post['mid']}, {'$set': {'sentiment': 0}})
        elif fabs(pos - 0.5) < 0.000001 and fabs(neg - 0.5) < 0.000001:
            client[project].posts.update({'mid': post['mid']}, {'$set': {'sentiment': 10}})
        elif pos - neg > 0:
            client[project].posts.update({'mid': post['mid']}, {'$set': {'sentiment': 15}})
        elif pos - neg < 0:
            client[project].posts.update({'mid': post['mid']}, {'$set': {'sentiment': 5}})
        log(NOTICE, "#%d, %d remains. time: %d sec(s)." % (i, count - i, int((datetime.datetime.now() - round_start).seconds)))
    log(NOTICE, 'Mission compeltes.')


def web_sentiment2(project, address, port):
    client = MongoClient(address, port)
    search_json = {'msg': {'$eq': ''}}
    count = client[project].posts.find(search_json).count()
    times = 2
    slc = count / times
    posts = client[project].posts.find(search_json).skip(count * 0 / times).limit(slc)
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36')]

    count = count / times
    log(NOTICE, "Total #: %d" % count)
    i = 0

    for post in posts:
        i += 1
        if i % 40 == 0:
            br.close()
            br = mechanize.Browser()
            br.set_handle_equiv(True)
            # br.set_handle_gzip(True)
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False)
        c = post['content']
        stop = False
        round_start = datetime.datetime.now()
        for re in RE_EQUALTO:
            if c == re:
                log(NOTICE, c.encode('gbk', 'ignore'))
                stop = True
                client[project].posts.update({'mid': post['mid']}, {'$set': {'msg': 'Processed. A Reply'}})
                break
        if stop:
            continue
        for re in RE_STARTWITH:
            if c[:len(re)] == re:
                log(NOTICE, c.encode('gbk', 'ignore'))
                stop = True
                client[project].posts.update({'mid': post['mid']}, {'$set': {'msg': 'Processed. A Reply'}})
                break
        if stop:
            continue
        rdm = random.randint(0, 999999999)
        timestamp = str(int(time.time()))
        try:
            br.open('http://182.254.136.27/yunapi/tools/index.php', timeout=10)
            br.select_form(nr=0)
            br.form['requestSecretId'] = TENCENT_SECRET_ID
            br.form['requestSecretKey'] = TENCENT_SECRET_KEY
            br.form['requestMethod'] = ['GET']
            br.form['requestDomain'] = 'wenzhi.api.qcloud.com'
            br.form['requestInterfaceName'] = 'TextSentiment'
            br.form['requestRegion'] = 'sz'
            br.form['requestParams'] = 'Action=TextSentiment&Nonce=%d&Timestamp=%s&content=%s' % (rdm, timestamp, c)
            br.submit()
        except URLError:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue
        except BadStatusLine:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue
        except timeout:
            log(WARNING, "rest for 10 seconds. %s" % c.encode('gbk', 'ignore'), "web_sentiment")
            time.sleep(10)
            continue

        r = br.response().read()

        result = r.split(u"请求结果")[1][51:-17]

        sentiment = json.loads(result)
        # log(NOTICE, str(result) + "  " + c.encode('gbk', 'ignore'))

        if sentiment['code'] == 0:
            neg = float(sentiment['negative'])
            pos = float(sentiment['positive'])
            msg = sentiment['message']
            client[project].posts.update({'mid': post['mid']}, {'$set': {'pos': pos, 'neg': neg, 'msg': 'Processed.' + msg}})
            try:
                log(NOTICE, "#%d, %d remains. time: %d sec(s). %s, %s" % (i, count - i, int((datetime.datetime.now() - round_start).seconds), result, c.encode('utf-8', 'ignore')))
            except UnicodeDecodeError:
                pass
            except UnicodeEncodeError:
                pass
    br.close()
    log(NOTICE, 'Mission compeltes.')


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


def get_sentiment(raw_content):
    import urllib
    import hmac
    import hashlib
    import random
    # import binascii
    # import base64
    rdm = random.randint(0, 999999999)
    timestamp = str(int(time.time()))

    srcStr = 'GETwenzhi.api.qcloud.com/v2/index.php?Action=TextSentiment&Nonce=%dRegion=sz&SecretId=AKID8afsi3KB4SaFEgTFtBJpyVjGJOB5uawg&Timestamp=%s' % (rdm, timestamp)
    hashed = hmac.new(TENCENT_SECRET_KEY, srcStr, hashlib.sha1)
    signature = hashed.digest().encode("base64").rstrip('\n')
    print signature
    rdm = random.randint(0, 999999999)
    search_json = {
        'Nonce': rdm,
        'Region': 'sz',
        'Action': 'TextSentiment',
        'Timestamp': int(timestamp),
        'SecretId': TENCENT_SECRET_ID,
        'content': unicode(raw_content),
        'Signature': signature
    }

    params = urllib.urlencode(ksort(search_json))
    final = r'https://wenzhi.api.qcloud.com/v2/index.php?%s' % params
    print final
    # 'https://wenzhi.api.qcloud.com/v2/index.php?Action=TextSentiment&Nonce=894686787&Region=sz&SecretId=AKID8afsi3KB4SaFEgTFtBJpyVjGJOB5uawg&Signature=mcGJxXl5dnT05GIf7HwBV3yAmXY%3D&Timestamp=1448071134&content=%E6%88%91%E7%88%B1%E4%BD%A0'
    response = requests.get(url=final)
    print response.content

# web_sentiment(project, address, port)

# get_sentiment(u'我爱你')
