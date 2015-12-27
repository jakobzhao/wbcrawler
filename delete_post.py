# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")

from wbcrawler.log import *
from wbcrawler.settings import UTC, TZCHINA
from pymongo import MongoClient

address = '192.168.1.12'
port = 27017
project = 'climate'


def delete(post):
    replies = post['replies']
    # userid = post['user']['userid']
    for reply in replies:
        delete(reply)

    db.posts.delete_many({'mid': post['mid']})
    # db.users.update({'userid': userid}, {'$set': {'latlng': [-2, -2]}})
    # db.users.delete_many({'userid': userid})

    log(NOTICE, "The specified post %d and its replies at %s have been deleted" % (post['mid'], post['timestamp']))


client = MongoClient(address, port)

db = client[project]

utc_end = datetime.datetime(2015, 11, 11, 0, 0, 0, 0, tzinfo=TZCHINA)
utc_start = datetime.datetime(2015, 10, 1, 0, 0, 0, 0, tzinfo=TZCHINA)
deleted = datetime.datetime(2015, 11, 1, 0, 0, 0, 0, tzinfo=UTC)

# utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=33)
# search_json = {"timestamp": {"$lt": utc_start}}
# search_json = {"timestamp": {"$gt": utc_end}}
# search_json = {"timestamp": deleted}
# search_json = {"keyword": u'新兴城镇化'}
# posts = db.posts.find(search_json)
# print posts.count()
# for p in posts:
#     delete(p)




mids = [3905322391123229, 3914974474721923, 3915341056969597, 3911413346950667, 3918053303334125, 3922568845542198, 3803933145362799, 3921839019899913, 3921886213719738, 3916256795108931, 3916255155360979]
for mid in mids:
    search_json = {"mid": mid}
    posts = db.posts.find(search_json)
    print posts.count()
    for p in posts:
        delete(p)
