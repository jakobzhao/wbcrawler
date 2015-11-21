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
import numpy
from pymongo import MongoClient, DESCENDING, ASCENDING
from wbcrawler.seg import seg_sentence

reload(sys)
sys.setdefaultencoding('utf-8')

project = 'five'
address = "localhost"
port = 27017

# model2 = Doc2Vec.load('%s/d2v.bin' % project)
# model = Doc2Vec.load('d2v_sentiment.bin')
model = Doc2Vec.load('d2v-sentiment-tag.bin')
line_count = 10000
# line_count = 350
model_size = 200

# print model.docvecs.most_similar(['NEG_0'])
for w, i in model.most_similar(u'不错'):
    print w + ' ' + str(i)
    pass

# exit(-1)

train_arrays = numpy.zeros((line_count * 2, model_size))
train_labels = numpy.zeros(line_count * 2)

for i in range(line_count):
    prefix_train_pos = 'POS_' + str(i)
    prefix_train_neg = 'NEG_' + str(i)
    # prefix_train_mid = 'MID_' + str(i)
    train_arrays[i] = model.docvecs[prefix_train_pos]
    train_arrays[line_count + i] = model.docvecs[prefix_train_neg]
    # train_arrays[line_count * 2 + i] = model.docvecs[prefix_train_mid]
    train_labels[i] = 1
    train_labels[line_count + i] = 0
    # train_labels[line_count * 2 + i] = 5

# print train_arrays
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from wbcrawler.NNet import NeuralNet
# from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

# classifier = RandomForestClassifier(n_estimators=100)
# classifier = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True, intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
# classifier = GaussianNB()
classifier = SVC()
# classifier = KNeighborsClassifier()
# classifier = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',n_neighbors=5, p=2, weights='uniform')
# classifier = DecisionTreeClassifier()
# classifier = NeuralNet(50, learn_rate=1e-2)
# classifier = SGDClassifier(loss='log', penalty='l1')

# classifier.fit(train_arrays, train_labels, fine_tune=False, maxiter=500, SGD=True, batch=150, rho=0.9)
classifier.fit(train_arrays, train_labels)
# print train_arrays, train_labels


# pred_probas = lr.predict_proba(test_vecs)[:,1]
#
# fpr,tpr,_ = roc_curve(y_test, pred_probas)
# roc_auc = auc(fpr,tpr)
# plt.plot(fpr,tpr,label='area = %.2f' %roc_auc)
# plt.plot([0, 1], [0, 1], 'k--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.legend(loc='lower right')
#
# plt.show()


project = 'insurance'
# fname = project + '/train-pos.txt'
nname = project + '/neg.txt'

with open(nname) as f:
    lines = f.readlines()
i = 0
neg_s = []
neg = []
for line in lines:
    sentence = line
    if sentence != '':
        a = model.infer_vector(sentence.split(u' '))
        score = classifier.predict(a)
        # print score
        neg_s.append(score[0])
        neg.append(a)
        i += (1 - score[0])
        # i += score[0]
        # log(NOTICE, sentence.encode('gbk', 'ignore'))
print neg_s
print i / float(len(lines))
print "======================================================="

nname = project + '/pos.txt'

with open(nname) as f:
    lines = f.readlines()
i = 0
pos_s = []
pos = []
for line in lines:
    # sentence = seg_sentence(line)
    sentence = line
    if sentence != '':
        a = model.infer_vector(sentence.split(u' '))
        score = classifier.predict(a)
        # print score
        pos_s.append(score[0])
        pos.append(a)
        # i += 1 - score[0]
        i += score[0]
        # log(NOTICE, sentence.encode('gbk', 'ignore'))
print pos_s
print i / float(len(lines))

f.close()

log(NOTICE, "Misson Part One completes.")
print classifier.score(pos + neg, pos_s + neg_s)

# from sklearn.manifold import TSNE
# import numpy as np
# import matplotlib.pyplot as plt
#
# ts = TSNE(2)
# reduced_vecs = ts.fit_transform(np.concatenate((pos, neg)))
# line_count = len(pos)
# for i in range(line_count * 2):
#     if i < line_count:
#         color = 'b'
#     else:
#         color = 'g'
#     plt.plot(reduced_vecs[i, 0], reduced_vecs[i, 1], marker='o', color=color, markersize=4)
#
#
# plt.show()
# plt.savefig('foo.png')

exit(-1)

a = model.infer_vector(u'医疗 改革 不错'.split(u' '))
b = model.infer_vector(u'最 恶毒 不足以 形容'.split(u' '))

# print classifier.predict(train_arrays[130])
print classifier.predict([a, b, model.docvecs['NEG_2'], model.docvecs['POS_2']])
for i in range(100):
    print classifier.predict([model.docvecs['NEG_' + str(i)]])
print "========POS=============="
for i in range(100):
    print classifier.predict([model.docvecs['POS_' + str(i)]])
# print classifier.predict_proba([a, b, model.docvecs['NEG_2'], model.docvecs['POS_2']])


log(NOTICE, "misson completes.")
