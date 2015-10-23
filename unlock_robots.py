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
import platform
import os

if "Linux" in platform.platform():
    sys.path.append(os.getcwd())
    # Important: Before deploying the program, compare the deploying version with
    # a normal debugging version, especially checkking which path is not loaded in
    # sys.path. Other than the root of the program, I noticed that another path as
    # show below is not attached as well. (I cost almost 24 hours to find it out..)
    sys.path.append("/home/bo/.local/lib/python2.7/site-packages")

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
