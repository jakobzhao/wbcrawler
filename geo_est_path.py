# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.geo import estimate_location_by_path
from pymongo import MongoClient

# Variables

address = "localhost"
port = 27017
project = 'gov'

client = MongoClient(address, port)
db = client[project]
users = db.users.find({"path": {"$ne": []}})
print "total user number is %d" % users.count()
latlng = [0, 0]
for user in users:
    latlng = estimate_location_by_path(user)
    if latlng != [0, 0]:
        db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})
