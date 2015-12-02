# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys
from pymongo import MongoClient
from wbcrawler.log import *
from wbcrawler.seg import seg_sentence, seg_sentence_tag
import nltk

reload(sys)
sys.setdefaultencoding('utf-8')

address = "localhost"
port = 27017
project = 'insurance'

words = []
client = MongoClient(address, port)
db = client[project]
search_json = {'$or': [{'keyword': u'国有企业改革'}, {'keyword': u'国企改革'}]}
search_json = {}
posts = db.posts.find(search_json)
count = posts.count()

for post in posts:
    sentence = seg_sentence(post['content'])
    # sentence = seg_sentence_tag(post['content'])
    log(NOTICE, sentence.encode('gbk', 'ignore'))
    words.extend(sentence.split(u' '))
    print ''

fd = nltk.FreqDist(words)
for m in fd.most_common(2000):
    print m[0].encode('gbk', 'ignore'), u' ', m[1]

log(NOTICE, 'mission completes.')

if __name__ == '__main__':
    # main()
    pass
