# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from utils import parse_repost, sina_login
from settings import *

br = sina_login(u3, p3)
parse_repost(project_name, keyword, br)
if __name__ == '__main__':
    pass
