# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

from wbcrawler.report import brief_report

reciever_string = 'jakobzhao@gmail.com;bo_zhao@hks.harvard.edu'
project = "weibo"
address = "localhost"
port = 27017
brief_report(reciever_string, project, address, port)
