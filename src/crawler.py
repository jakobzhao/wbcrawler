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
# keyword = '雾霾'
# keyword = '地方政府'
keyword = '乡政府'

br = weibo_login()
parse_keyword(keyword, project_name, br)

end = datetime.datetime.now()

print "Successfully completed.This program has costs %d seconds." % (end - start).seconds


if __name__ == '__main__':
    pass