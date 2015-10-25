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
sys.path.append("/home/bo/Workspace/wbcrawler/insurance")

# libraries
from settings import SETTINGS
from wbcrawler.parallel import parallel_crawling
from wbcrawler.database import unlock_robots

# repost, path, info = 2, 0, 0

# funcs
parallel_crawling(SETTINGS['robot_num'], 0, 0, SETTINGS)
unlock_robots(SETTINGS)
parallel_crawling(0, SETTINGS['robot_num'], 0, SETTINGS)
unlock_robots(SETTINGS)
parallel_crawling(0, 0, SETTINGS['robot_num'], SETTINGS)
unlock_robots(SETTINGS)

if __name__ == '__main__':
    pass
