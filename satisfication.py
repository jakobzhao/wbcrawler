# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from snownlp.sentiment import Sentiment
from snownlp import SnowNLP as sn
from pymongo import MongoClient
from wbcrawler.log import *
from wbcrawler.utils import get_name_from_content

# import re

address = "localhost"
port = 27017
project = 'five_local'
client = MongoClient(address, port)
# db = client[project]
db = client['five']

posts = db.posts.find().skip(100).limit(1000)
b = []
# pattern = r'@.+[ |:]'
# pattern = r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"
for post in posts:
    a = post['content']

    names = get_name_from_content(a)

    if len(names) > 0:
        try:
            # print names[0].encode('gbk', 'ignore')
            pass
        except UnicodeEncodeError, e:
            pass

    url = ''
    if u'http://t.cn/' in a:
        url_start = a.find(u'http://t.cn/')
        url = a[url_start:url_start + 19]
        print url

    a = a.replace(url, '').replace(u'//', '').replace(u'转发微博', '').replace(u'轉發微博', '').replace(u'repost', '')

    i = 1
    for name in names:
        a = a.replace(name, u'用户' + unicode(i))
        i += 1
    if a == '':
        continue

    try:
        s_t = Sentiment()
        s_t.load(fname=project + '/sentiment.marshal')
        s_t.handle(a)
    except ZeroDivisionError:
        pass
    b.append(a)
    log(NOTICE, '%f, %s' % (s_t.classify(a), a.encode('gbk', 'ignore')))

if __name__ == '__main__':
    pass
