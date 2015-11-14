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

address = 'localhost'
port = 27017
project = 'five_bkp'


def delete(post):
    replies = post['replies']
    userid = post['user']['userid']
    for reply in replies:
        delete(reply)

    db.posts.delete_many({'mid': post['mid']})

    db.users.delete_many({'userid': userid})

    log(NOTICE, "The specified post %d and its replies have been deleted" % post['mid'])


client = MongoClient(address, port)

db = client['five_bkp']

utc_end = datetime.datetime(2015, 11, 11, 0, 0, 0, 0, tzinfo=TZCHINA)

utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=30)
search_json = {"timestamp": {"$gt": utc_end}}
search_json = {"mid": 3900745600059327}
posts = db.posts.find(search_json)
print posts.count()

for p in posts:
    delete(p)
