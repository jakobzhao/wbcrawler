# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
from wbcrawler.sna import export_posts

export_posts('climate', 'localhost', 27017, 'climate-posts-with-content-20160222.csv')
