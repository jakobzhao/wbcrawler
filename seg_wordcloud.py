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
from wbcrawler.seg import preprocess_content
from snownlp import SnowNLP as sn
import nltk
from nltk.probability import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from wbcrawler.settings import UTC, TZCHINA


def main():
    address = "localhost"
    port = 27017
    project = 'insurance'
    client = MongoClient(address, port)
    db = client[project]
    words = []
    # search_json = {'$or': [{'keyword': '社会保险'},{'keyword': '社保'}]}
    # search_json = {'keyword': '医疗保险'}
    # utc_end = datetime.datetime(2015, 11, 11, 0, 0, 0, 0, tzinfo=TZCHINA)
    # utc_start = datetime.datetime(2015, 11, 7, 0, 0, 0, 1, tzinfo=TZCHINA)
    # search_json = {'$and': [{"timestamp": {"$lt": utc_end}}, {"timestamp": {"$gt": utc_start}}]}
    # search_json = {"timestamp": {"$gt": utc_end}}
    search_json = {}

    posts = db.posts.find(search_json)
    count = db.posts.find(search_json).count()
    i = 0
    for post in posts:
        a = post['content']
        a = preprocess_content(a)
        if a != '':
            s = sn(a)
            t = u''
            for word in s.words:
                words.append(word)
                t += unicode(word) + u' '
        # log(NOTICE, 'parsing post #%d, %d remains. post content: %s' % (i, count - i, a[:20].encode('gbk', 'ignore')))
        i += 1
    fd = nltk.FreqDist(words)
    for m in fd.most_common(1000):
        print m[0].encode('gbk', 'ignore'), ' ', m[1]

    log(NOTICE, 'mission completes.')


if __name__ == '__main__':
    main()
