# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

from pytz import timezone
TZCHINA = timezone('Asia/Chongqing')
UTC = timezone('UTC')
DEBUG_PATH = '../log/'

BAIDU_AK = 'Y4wB8DznamkwhY8RxDiYNSHS'
PB_KEY = 'bYJFjyvIYWbn5vg2eNiFmcapjLu1PUTL'

COUNT = 200
FLOW_CONTROL_DAYS = 365  # at the very beginning, I used 30 days.
MIN_FWD_COUNT = 5
TIMEOUT = 60
