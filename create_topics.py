# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Nov 22, 2015
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
project = 'insurance'


def update(post):
    replies = post['replies']
    if len(replies) > 0:
        topic = post['topic']
        for reply in replies:
            db.posts.update({'mid': reply['mid']}, {'$set': {'topic': topic}})
            update(reply)
    log(NOTICE, "The specified post %d and its replies have been updated" % post['mid'])


client = MongoClient(address, port)
db = client[project]

search_json = {'topic': {'$ne': []}}
posts = db.posts.find(search_json)
count = posts.count()
i = 0
for p in posts:
    i += 1
    update(p)
    log(NOTICE, "#%d, %d posts remain." % (i, count - i))
log(NOTICE, "mission completes.")

# mids = [3899946640489118, 3901059736974417, 3899646466774778, 3899581202733456, 3899581202733456, 3899952872556369, 3899977241686419, 3900052386611726, 3899669883184301, 3899711620152467, 3899722978803879, 3899776196006785, 3899576475963561, 3899656172051338, 3899665269510963, 3900755192932235, 3899706826563531, 3899703231943367, 3899364571470764, 3899703231943367, 3899781417656859]
# for mid in mids:
#     search_json = {"mid": mid}
#     posts = db.posts.find(search_json)
#     print posts.count()
#     for p in posts:
#         delete(p)
