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

from utils import parse_keyword, weibo_login

start = datetime.datetime.now()

# ProjectName
project_name = "weibo"
#Variables
keyword = '奇怪'

pages = 1

br = weibo_login()
parse_keyword(keyword, br, project_name)

end = datetime.datetime.now()

print "This program costs %d seconds." % (end - start).seconds

print "all finished"

if __name__ == '__main__':
    pass