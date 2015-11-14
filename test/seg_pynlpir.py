# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from pymongo import MongoClient, DESCENDING, ASCENDING
from wbcrawler.log import *
from wbcrawler.utils import get_name_from_content
import numpy as np
import pandas as pd
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')

import pynlpir
from pynlpir import nlpir as np

pynlpir.open()

# pynlpir.nlpir.

s = u'欢迎科研人员、技术工程师、企事业单位与个人参与NLPIR平台的建设工作。'
# result = pynlpir.segment(s)

for i in pynlpir.segment(s, pos_tagging=False):
    print i


for i in pynlpir.get_key_words(s, weighted=True):
    print i[0]

pynlpir.close()
