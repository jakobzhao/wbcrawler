# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on May 16, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

# sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/ubuntu/wbcrawler")
sys.path.append("/home/ubuntu/wbcrawler/philanthropy")

from wbcrawler.parser import parse_keyword
from wbcrawler.robot import register, unregister, create_database, unlock_robots
from wbcrawler.log import *
from settings import SETTINGS

# unlock the unreleased robots
unlock_robots(SETTINGS)

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
    for keyword in SETTINGS['keywords']:
        round_start = datetime.datetime.now()
        parse_keyword(keyword, robot, db)
        log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
        # except KeyboardInterrupt, e:
except:
    log(ERROR, 'An error occurs.', 'crawler.py')
finally:
    # out of the stak
    unregister(robot)
    log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
