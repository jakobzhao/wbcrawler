# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import datetime

from pushbullet import Pushbullet

from settings import TZCHINA
from settings import PB_KEY

NOTICE, RECORD, WARNING, ERROR, FATALITY = 0, 1, 2, 3, 4
pb = Pushbullet(PB_KEY)


def log(level, output, func_name=''):
    t = datetime.datetime.now(TZCHINA).strftime('%Y-%m-%d %H:%M')
    if level == NOTICE:
        print ('[NOTICE] %s %s' % (t, output))
    elif level == WARNING:
        print ('[NOTICE] %s in func %s %s' % (t, func_name, output))
    elif ERROR:
        print ('[NOTICE] %s in func %s %s' % (t, func_name, output))
    else:
        pb.push_note("Lord", output, func_name)
        print ('[FATAL] %s %s' % (t, output))
