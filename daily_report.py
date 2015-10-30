# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

# Important: Before deploying the program, compare the deploying version with
# a normal debugging version, especially checkking which path is not loaded in
# sys.path. Other than the root of the program, I noticed that another path as
# show below is not attached as well. (I cost almost 24 hours to find it out..)

import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")

from wbcrawler.report import brief_report
from settings import SETTINGS

brief_report(SETTINGS)
