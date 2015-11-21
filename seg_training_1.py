# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
# gensim modules
from gensim.models import Doc2Vec
from wbcrawler.log import *
from wbcrawler.seg import LabeledLineSentence

reload(sys)
sys.setdefaultencoding('utf-8')

project = 'insurance'

negfile = '%s/neg.txt' % project
posfile = '%s/pos.txt' % project
midfile = '%s/mid.txt' % project
# sources = {negfile: 'NEG', posfile: 'POS', midfile: 'MID'}
sources = {negfile: 'NEG', posfile: 'POS'}
sentences = LabeledLineSentence(sources)

model = Doc2Vec(min_count=3, window=4, size=200, sample=1e-4, negative=5, workers=7)

model.build_vocab(sentences.to_array())

for epoch in range(10):
    model.train(sentences.to_array())
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decayz

print model.docvecs.most_similar(['NEG_0'])
for w, i in model.most_similar(u'赞'):
    print w + str(i)

model = model.save('%s/d2v-sentiment-tag.bin' % project)
log(NOTICE, "misson completes.")
