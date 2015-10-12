# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from utils import parse_repost, weibo_manual_login


# ProjectName
project_name = "weibo"

# Variables
keyword = '乡政府'

br = weibo_manual_login()

parse_repost(project_name, keyword, br)
if __name__ == '__main__':
    pass
