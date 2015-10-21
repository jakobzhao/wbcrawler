# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

from pymongo import MongoClient, DESCENDING

from log import *


def register(project, address, port):
    client = MongoClient(address, port)
    db = client[project]

    if db.accounts.find({"inused": False}).count() == 0:
        occupied_msg = "All the accounts are occupied, please try again later."
        log(FATALITY, occupied_msg)
        exit(-1)

    account_raw = db.accounts.find({"inused": False}).limit(1)[0]
    account = [account_raw['username'], account_raw['password'], account_raw['id']]

    db.accounts.update({'username': account_raw['username']}, {'$set': {"inused": True}})
    log(NOTICE, 'ROBOT %d is registering...' % account_raw['id'])

    return account


def unregister(project, address, port, account):
    # {'$set': {'inused': false}}
    client = MongoClient(address, port)

    db = client[project]

    db.accounts.update({'username': account[0]}, {'$set': {"inused": False}})
    log(NOTICE, 'ROBOT %d has successfully unregistered.' % account[2])
    return True


def create_database(project, address, port, fresh=False):
    client = MongoClient(address, port)
    # client.the_database.authenticate()
    # client.the_database.authenticate('bo', 'f', source="C:\MongoDB\data")
    # client = MongoClient('mongodb://bo:f@localhost:27017')
    # db.add_user('bo','f')
    # from the address level, I have to define the url by myself. seems we cannot reply on pyton
    # from the database level, what we can do? And how to do that?
    db = client[project]
    posts = db.posts
    users = db.users

    if fresh:
        db.posts.delete_many({})
        db.users.delete_many({})

    posts.create_index([("mid", DESCENDING)], unique=True)
    users.create_index([("userid", DESCENDING)], unique=True)
    return db
