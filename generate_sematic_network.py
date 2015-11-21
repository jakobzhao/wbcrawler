# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from wbcrawler.sna import generate_sematic_network

generate_sematic_network(input='shebao.txt', output="sematic_shebao.gexf")
