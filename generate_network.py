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
address = "localhost"
port = 27017
project = 'five'

generate_network(project, address, port, output="sample_five.gexf")
