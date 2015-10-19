# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

# libraries
from pymongo import MongoClient

from wbcrawler.log import *


# variables
project = 'local'
address = "localhost"
port = 27017


# funcs
def unlock_robots(address, port, project):
    client = MongoClient(address, port)
    db = client[project]
    db.accounts.update_many({'inused': True}, {'$set': {'inused': False}})
    log(NOTICE, "All the robots have been unlocked.")


if __name__ == '__main__':
    unlock_robots(address, port, project)
