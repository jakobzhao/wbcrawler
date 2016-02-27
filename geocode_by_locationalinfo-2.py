# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

sys.path.append("C:/Workspace/wbcrawler")

from wbcrawler.geo import geocode_locational_info

# Variables

address = "localhost"
port = 27017
project = 'donor'

geocode_locational_info(project, address, port)
