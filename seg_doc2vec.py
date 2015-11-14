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

# class LabeledLineSentence(object):
#     def __init__(self, sources):
#         self.sources = sources
#
#         flipped = {}
#
#         # make sure that keys are unique
#         for key, value in sources.items():
#             if value not in flipped:
#                 flipped[value] = [key]
#             else:
#                 raise Exception('Non-unique prefix encountered')
#
#     def __iter__(self):
#         for source, prefix in self.sources.items():
#             with utils.smart_open(source) as fin:
#                 for item_no, line in enumerate(fin):
#                     yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
#
#     def to_array(self):
#         self.sentences = []
#         for source, prefix in self.sources.items():
#             with utils.smart_open(source) as fin:
#                 for item_no, line in enumerate(fin):
#                     self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
#         return self.sentences
#
#     def sentences_perm(self):
#         return numpy.random.permutation(self.sentences)
#
# # sources = {'test-neg.txt': 'TEST_NEG', 'test-pos.txt': 'TEST_POS', 'train-neg.txt': 'TRAIN_NEG', 'train-pos.txt': 'TRAIN_POS', 'train-unsup.txt': 'TRAIN_UNS'}
# sources = {'train-neg.txt': 'TRAIN_NEG', 'train-pos.txt': 'TRAIN_POS'}
# sentences = LabeledLineSentence(sources)
#
# model = Doc2Vec(min_count=1, window=10, size=400, sample=1e-4, negative=5, workers=7)
#
# model.build_vocab(sentences.to_array())
#
# for epoch in range(10):
#     model.train(sentences.to_array())
#     model.alpha -= 0.002  # decrease the learning rate
#     model.min_alpha = model.alpha  # fix the learning rate, no decayz
#
# model = Doc2Vec.save('five.d2v')
model = Doc2Vec.load('imdb.d2v')
# sentence = LabeledSentence(words=[u'some', u'words', u'here'], labels=[u'SENT_1'])

print model.docvecs.most_similar(['TRAIN_NEG_0'])
print model.most_similar('it')

train_arrays = numpy.zeros((10, 100))
train_labels = numpy.zeros(10)

for i in range(10):
    prefix_train_pos = 'TRAIN_POS_' + str(i)
    prefix_train_neg = 'TRAIN_NEG_' + str(i)
    train_arrays[i] = model[prefix_train_pos]
    train_arrays[10 + i] = model[prefix_train_neg]
    train_labels[i] = 1
    train_labels[10 + i] = 0

print train_arrays
