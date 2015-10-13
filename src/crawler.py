# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import datetime

from utils import parse_keyword, sina_login
from settings import *


start = datetime.datetime.now()

br = sina_login(u1, p1)
parse_keyword(keyword, project_name, br)

end = datetime.datetime.now()

print "Successfully completed.This program has costs %d seconds." % (end - start).seconds


if __name__ == '__main__':
    pass