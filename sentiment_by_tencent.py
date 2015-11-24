# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Nov 19, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from wbcrawler.sentiment import tencent_sentiment

reload(sys)
sys.setdefaultencoding('utf-8')

tencent_sentiment(0, 1, 'insurance', 'localhost', 27017)
