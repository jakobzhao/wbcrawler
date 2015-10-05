# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''


from utils import parse_keyword, weibo_login


#Variables
keyword = '地方政府'

pages = 1

br = weibo_login()
parse_keyword(keyword, br)


print "all finished"

if __name__ == '__main__':
    pass