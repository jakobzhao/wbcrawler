# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.geo import georeference

# Variables
# address = "192.168.1.12"
address = "localhost"
port = 27017
project = 'five'

georeference(project, address, port)
