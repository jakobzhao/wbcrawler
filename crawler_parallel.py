# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

# libraries
from wbcrawler.parallel import parallel_crawling

# variables
project = 'five'
address = "localhost"
port = 27017
repost, info, path = 0, 5, 0

# funcs
parallel_crawling(repost, info, path, project, address, port)

if __name__ == '__main__':
    pass
