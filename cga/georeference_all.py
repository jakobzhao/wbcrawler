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
sys.path.append("/home/bo/wbcrawler")
sys.path.append("/home/bo/wbcrawler/cga")

sys.path.append("C:/Workspace/wbcrawler")
sys.path.append("C:/Workspace/wbcrawler/cga")

from wbcrawler.geo import estimate_location_by_path, geocode_locational_info, geocode_by_semantics, georeference
from wbcrawler.log import *
from pymongo import MongoClient

# Variables
# before executing this script, I need to collect the path.
# if having the path, then I can tell the location. A mark is necessary.
# if no path, then I need to use the locational information in the profile. So before the second step(-2.py), I need to collect the profile inforamtion.
# sometimes, the semantic content can be used as well.

address = "localhost"
port = 27017
project = 'cga'

# [1st of GEOREFERENCE]: geo_est_path
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

# [2nd of GEOREFERENCE]: geocode by locationalinfo
geocode_locational_info(project, address, port)

# [3rd of GEOREFERENCE]: geocode by semantics
geocode_by_semantics(project, address, port)

# [4th of GEOREFERENCE]: georeference
georeference(project, address, port)

log(NOTICE, 'mission completes.')
