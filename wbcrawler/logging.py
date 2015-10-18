# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from pushbullet import Pushbullet

NOTICE = 0
WARNING = 1
ERROR = 2
Fatality = 3

for line in open("../../keys.conf"):
    if "BAIDU_AK" in line:
        BAIDU_AK = line.split("=")[1]
    if "PB_KEY" in line:
        PB_KEY = line.split("=")[1]

pb = Pushbullet(PB_KEY)


def log(level, output):
    time = str(datetime.datetime.now(TZCHINA))

    if level = Notice
