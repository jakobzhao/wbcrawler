# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.sna import generate_network

# Variables
# address = "192.168.1.12"
address = "localhost"
port = 27017
project = 'insurance'

generate_network(project, address, port, "insurance-20160502.gexf", 2000, 11, 1)
