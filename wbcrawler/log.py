# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

import datetime

from settings import TZCHINA, pb

NOTICE = 0
RECORD = 1
WARNING = 2
ERROR = 3
FATALITY = 4

for line in open("../../keys.conf"):
    if "BAIDU_AK" in line:
        BAIDU_AK = line.split("=")[1]
    if "PB_KEY" in line:
        PB_KEY = line.split("=")[1]


def log(level, output):
    t = datetime.datetime.now(TZCHINA)
    if level == NOTICE:
        print output
        print ('[NOTICE] %d-%d-%d %d:%d] %s' % (t.year, t.month, t.day, t.hour, t.minute, output))
    elif level == WARNING:
        print output
    elif ERROR:
        print output
    else:
        pb.push_note("Lord,", output)
        print output
