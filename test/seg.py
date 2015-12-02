# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from pymongo import MongoClient, DESCENDING, ASCENDING
from wbcrawler.log import *
from wbcrawler.utils import get_name_from_content
from snownlp import SnowNLP as sn
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    address = "localhost"
    port = 27017
    project = 'five'
    client = MongoClient(address, port)
    db = client[project]
    # f = open('t.txt', 'a')
    words = []

    posts = db.posts.find()
    count = db.posts.find().count()

    t = u''
    i = 0
    for post in posts:
        a = post['content']
        a = preprocess_content(a)
        t += a + u'/n'
        i += 1
        print i
        if i > 100:
            break
    s = sn(t)
    for k in s.keywords(3):
        print k.encode('gbk', 'ignore')

    log(NOTICE, 'mission completes.')


def preprocess_content(a):
    names = get_name_from_content(a)

    url = ''
    if u'http://t.cn/' in a:
        url_start = a.find(u'http://t.cn/')
        url = a[url_start:url_start + 19]
        # print url

    if len(a) >= 2:
        a = a.split('//')[0]

    a = a.replace(url, '').replace(u'转发微博', '').replace(u'轉發微博', '').replace(u'repost', '')

    i = 1
    for name in names:
        a = a.replace(name, u'用户' + unicode(i))
        i += 1
    return a


if __name__ == '__main__':
    main()