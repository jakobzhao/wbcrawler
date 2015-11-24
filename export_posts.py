# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from wbcrawler.sna import export_posts

reload(sys)
sys.setdefaultencoding('utf-8')

# Variables
# address = "192.168.1.12"
address = "localhost"
port = 27017
project = 'insurance'

export_posts(project, address, port, output="op.csv")
