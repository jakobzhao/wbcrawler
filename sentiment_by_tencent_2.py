# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Nov 19, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from wbcrawler.sentiment import tencent_sentiment_2

reload(sys)
sys.setdefaultencoding('utf-8')

tencent_sentiment_2('five', 'localhost', 27017)
