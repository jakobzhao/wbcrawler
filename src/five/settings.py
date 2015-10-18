# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

KEYWORDS_FIVE = ['五中全会']

COUNT = 200
FLOW_CONTROL_DAYS = 3000  # at the very beginning, I used 30 days.
TIMEOUT = 30

address = "localhost"
port = 27017
fresh = False

project = "five"
