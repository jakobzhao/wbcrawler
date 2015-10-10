# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from utils import parse_profile, weibo_login


# ProjectName
project_name = "weibo"

# Variables
keyword = '雾霾'

br = weibo_login()
parse_profile(project_name, keyword, br)
if __name__ == '__main__':
    pass
