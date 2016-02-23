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
from pymongo import MongoClient

address = 'localhost'
port = 27017
project = 'climate'

client = MongoClient(address, port)

db = client[project]

userids = set()

search_json = {}
posts = db.posts.find(search_json)
log(NOTICE, "# of total posts: %d" % posts.count())
for post in posts:
    userids.add(int(post['user']['userid']))

log(NOTICE, "# of total unique users: %d" % len(userids))

users = db.users.find()

count = users.count()
log(NOTICE, "# of total users: %d" % count)
i = 0
for user in users:
    userid = user['userid']
    if userid not in userids:
        db.users.delete_many({'userid': userid})
        try:
            log(NOTICE, "# %d, %d remain. The user %s has been deleted" % (i, count - i, user['username']))
        except:
            pass
    i += 1
