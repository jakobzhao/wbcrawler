# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import datetime
# from settings import TZCHINA
# from pushbullet import Pushbullet
# from settings import PB_KEY
# pb = Pushbullet(PB_KEY)

NOTICE, RECORD, WARNING, ERROR, FATALITY, PUSH = 0, 1, 2, 4, 8, 16


def log(level, output, func_name=''):
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if level == NOTICE:
        print ('[NOTICE] %s %s' % (t, output))
    elif level == WARNING:
        print ('[NOTICE] %s in func %s %s.' % (t, func_name, output))
    elif level == ERROR:
        print ('[NOTICE] %s in func %s %s.' % (t, func_name, output))
    elif level == FATALITY:
        # pb.push_note("Lord", output, func_name)
        print ('[FATAL] %s %s.' % (t, output))
    else:
        # pb.push_note("Lord", output)
        print output
