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
# numpy
import numpy
import jieba
# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
# classifier
from sklearn.linear_model import LogisticRegression

reload(sys)
sys.setdefaultencoding('utf-8')
