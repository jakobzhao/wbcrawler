# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.geo import geocode_by_semantics

# Variables

address = "localhost"
port = 27017
project = 'donor'

geocode_by_semantics(project, address, port)
