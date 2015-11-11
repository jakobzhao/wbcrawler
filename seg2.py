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
import nltk
from nltk.probability import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    address = "localhost"
    port = 27017
    project = 'five'
    client = MongoClient(address, port)
    db = client[project]
    words = []

    posts = db.posts.find()
    count = db.posts.find().count()
    i = 0
    for post in posts:
        a = post['content']
        a = preprocess_content(a)
        if a != '':
            s = sn(a)
            t = u''
            for word in s.words:
                # print word.encode('gbk', 'ignore')
                if u'http' in word or u'#' in word or u'【' in word or u'】' in word or u'，' in word or u'。' in word:
                    continue
                words.append(word)
                t += unicode(word) + u' '
        log(NOTICE, 'parsing post #%d, %d remains. post content: %s' % (i, count - i, a[:20].encode('gbk', 'ignore')))
        i += 1
    fd = nltk.FreqDist(words)
    for m in fd.most_common(2000):
        print m[0].encode('gbk', 'ignore'), ' ', m[1]

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
