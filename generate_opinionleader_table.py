# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from wbcrawler.sna import opinion_leaders

reload(sys)
sys.setdefaultencoding('utf-8')

# Variables
# address = "192.168.1.12"
address = "localhost"
port = 27017
project = 'five'

opinion_leaders(project, address, port, "five-1117.csv", 2015, 10, 1)
