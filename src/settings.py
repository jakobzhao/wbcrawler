# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

COUNT = 200
FLOW_CONTROL_DAYS = 3  # at the very beginning, I used 30 days.
TIMEOUT = 30

KEYWORDS = ['政府', '中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会']
KEYWORDS_CLIMATE = ['气候变化', '全球变暖']

# ProjectName
project = "weibo"
address = "localhost"
port = 27017

fp = open("../keys.conf")
for line in fp:
    if "BAIDU_AK" in line:
        BAIDU_AK = line.split("=")[1]
    if "PB_KEY" in line:
        PB_KEY = line.split("=")[1]
