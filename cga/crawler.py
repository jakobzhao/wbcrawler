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
# sys.path.append("/home/bo/Workspace/wbcrawler")
# sys.path.append("/home/bo/Workspace/wbcrawler/cga")
sys.path.append("/home/bo/wbcrawler")
sys.path.append("/home/bo/wbcrawler/cga")

from wbcrawler.parser import parse_discovery
from wbcrawler.robot import register, unregister, create_database, unlock_robots
from wbcrawler.log import *
from settings import SETTINGS

# unlock the unreleased robots
# unlock_robots(SETTINGS)

# start to crawl
start = datetime.datetime.now()
t = SETTINGS['robot_num']

robot = {}
accounts = []
for i in range(t):
    if robot == {}:
        robot = register(SETTINGS)
    else:
        break

try:
    db = create_database(SETTINGS)
    # for d_type in SETTINGS['d_types']:
    for d_type_num in range(len(SETTINGS['d_types'])):
        round_start = datetime.datetime.now()
        parse_discovery(SETTINGS['d_types'][d_type_num], robot, db)
        log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (SETTINGS['d_types'][d_type_num].keys()[0].decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
except:
    log(ERROR, 'An error occurs.', 'crawler.py')
finally:
    # out of the stak
    unregister(robot)
    log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
