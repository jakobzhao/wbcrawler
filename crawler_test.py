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
sys.path.append("/home/bo/Workspace/wbcrawler")

from wbcrawler.parser import parse_keyword
from wbcrawler.robot import register, unregister, create_database, unlock_robots
from wbcrawler.log import *
from settings import SETTINGS


# KEYWORDS = ['政府', '中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会']
# KEYWORDS_CLIMATE = ['气候变化', '全球变暖']
# KEYWORDS = ['政府', '中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会']
# KEYWORDS = ['中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会']
# KEYWORDS = ['县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会']
# KEYWORDS = ['气候变化', '全球变暖']

# First Round: 129 minutes

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

db = create_database(SETTINGS)
for keyword in SETTINGS['keywords']:
    round_start = datetime.datetime.now()
    parse_keyword(keyword, robot, db)
    log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
    # except KeyboardInterrupt, e:



# out of the stak
unregister(robot)
log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
