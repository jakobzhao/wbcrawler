# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 11, 2012

@author: bo
'''

from utils import searchTopicFromUser
from shutil import copy

topic = 'pm2.5'
refresh = True
pages = 1
#--------------------------------------------------------------------------------------------------------
database = '../data/' + topic +'.db'
if refresh:
    copy('weibo_crawler_template.db', database)
searchTopicFromUser(1182391231, topic, '../data/pm2.5.db')