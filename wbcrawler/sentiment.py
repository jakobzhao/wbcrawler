# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 14, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard University
'''

import sys

from snownlp import SnowNLP as sn
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

address = "localhost"
port = 27017
client = MongoClient(address, port)
db = client['weibo']

posts = db.posts.find().limit(100)

for post in posts:
    a = post['content'].decode('utf-8').replace("转发微博", "").replace('//', '').replace("@", "")
    try:
        s_a = sn(a)
    except ZeroDivisionError:
        pass
    print "%f, %s \n" % (s_a.sentiments, a.decode('utf-8', 'ignore').encode('gbk', 'ignore'))

if __name__ == '__main__':
    pass
