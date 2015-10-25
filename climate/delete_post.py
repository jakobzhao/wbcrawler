# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


from wbcrawler.log import *
from settings import SETTINGS
from wbcrawler.database import delete_post

mids = []

for mid in mids:
    delete_post(mid, SETTINGS)
    log(NOTICE, 'the post %d and its accompanying replies have been deleted')
