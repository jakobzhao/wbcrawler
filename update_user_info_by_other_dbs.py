# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
# @usage:        update the user table based on another established user table.
import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")

from wbcrawler.log import *
from pymongo import MongoClient

address = 'localhost'
port = 27017
project = 'five'

other_address = 'localhost'
other_port = 27017
other_project = 'gov'

client = MongoClient(address, port)
db = client[project]
users = db.users.find({'latlng': [0, 0]})
log(NOTICE, 'the total number of users: %d' % users.count())

other_client = MongoClient(other_address, other_port)
other_db = other_client['gov']
other_users = other_db.users.find()
log(NOTICE, 'the total number of users in memeory: %d' % other_users.count())

i = 0
for user in users:
    if other_db.users.find({'userid': user['userid']}).count() == 1:
        user_json = other_db.users.find({'userid': user['userid']})[0]
        db.users.delete_many({'userid': user['userid']})
        db.users.insert_one(user_json)
        log(NOTICE, '%d users has been updated.' % i)
        i += 1
log(NOTICE, "mission is completed.")
