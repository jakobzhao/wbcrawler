# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.geo import estimate_location_by_path
from wbcrawler.log import *
from pymongo import MongoClient

# Variables

address = "localhost"
port = 27017
project = 'donor'

client = MongoClient(address, port)
db = client[project]
# search_json = {"path": {"$ne": []}}
search_json = {'$and': [{'path': {'$ne': []}}, {'path': {'$ne': [[0, 0, 0]]}}]}
# search_json = {'latlng': [-2, -2]}
users = db.users.find(search_json)
print "total user number is %d" % users.count()
latlng = [-1, -1]
for user in users:
    latlng = estimate_location_by_path(user)
    if latlng != [-1, -1]:
        db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})
log(NOTICE, 'mission completes.')
