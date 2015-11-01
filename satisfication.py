# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from snownlp.sentiment import Sentiment
from pymongo import MongoClient
from wbcrawler.log import *

address = "localhost"
port = 27017
project = 'five'
client = MongoClient(address, port)
db = client[project]

posts = db.posts.find().skip(100).limit(500)

for post in posts:
    a = post['content'].replace(u'转发微博', '').replace(u'//', '').replace(u'@', '').replace(u'轉發微博', '').replace(u'repost', '')
    if a == '':
        continue
    try:
        s_t = Sentiment()
        s_t.load(fname=project + '_local/sentiment.marshal')
        s_t.handle(a)
    except ZeroDivisionError:
        pass

    log(NOTICE, '%f, %s' % (s_t.classify(a), a.encode('gbk', 'ignore')))

if __name__ == '__main__':
    pass
