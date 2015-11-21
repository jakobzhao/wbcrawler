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

jieba.load_userdict('wbcrawler/training_set/dict.txt')

seg_list = jieba.cut(u"「台中」正确应该不会被切开", HMM=False)  # 默认是精确模式
print(", ".join(seg_list))
