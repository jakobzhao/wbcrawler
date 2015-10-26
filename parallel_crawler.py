# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

# libraries
from wbcrawler.parallel import parallel_crawling
from settings import SETTINGS

# variables
repost, path, info = 1, 0, 0

# funcs
parallel_crawling(repost, path, info, SETTINGS)

if __name__ == '__main__':
    pass
