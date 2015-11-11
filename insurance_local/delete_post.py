# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")
sys.path.append("/home/bo/Workspace/wbcrawler/insurance")

from wbcrawler.log import *
from settings import SETTINGS

# from wbcrawler.robot import mark_delete_time

mids = []

# for mid in mids:
#    mark_delete_time(mid, SETTINGS)
#    log(NOTICE, 'the post %d and its accompanying replies have been deleted' % mid)
