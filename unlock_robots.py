# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import sys
sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")

# libraries
from pymongo import MongoClient
from wbcrawler.log import *

# variables
address = "localhost"
port = 27017


# funcs
def unlock_robots(address, port):
    client = MongoClient(address, port)
    db = client['local']
    db.accounts.update_many({'inused': True}, {'$set': {'inused': False}})
    log(NOTICE, "All the robots have been unlocked.")

if __name__ == '__main__':
    unlock_robots(address, port)
