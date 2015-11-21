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
from pymongo import MongoClient
from wbcrawler.seg import seg_sentence

reload(sys)
sys.setdefaultencoding('utf-8')

project = 'insurance'
address = "localhost"
port = 27017

model = Doc2Vec.load('%s/d2v.bin' % project)
# model = Doc2Vec.load('d2v_sentiment.bin')
# line_count = 10000
line_count = 350
model_size = 200

# print model.docvecs.most_similar(['NEG_0'])
# for w, i in model.most_similar(u'赞'):
#     print w + ' ' + str(i)
#     pass


train_arrays = numpy.zeros((line_count * 2, model_size))
train_labels = numpy.zeros(line_count * 2)

for i in range(line_count):
    prefix_train_pos = 'POS_' + str(i)
    prefix_train_neg = 'NEG_' + str(i)
    # prefix_train_mid = 'MID_' + str(i)
    train_arrays[i] = model.docvecs[prefix_train_pos]
    train_arrays[line_count + i] = model.docvecs[prefix_train_neg]
    # train_arrays[line_count * 2 + i] = model.docvecs[prefix_train_mid]
    train_labels[i] = 1.0
    train_labels[line_count + i] = 0
    # train_labels[line_count * 2 + i] = 5

# 　print train_arrays
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
# from wbcrawler.NNet import NeuralNet
# from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

# classifier = RandomForestClassifier(n_estimators=100)
# classifier = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True, intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
# classifier = GaussianNB()
# classifier = SVC()
# classifier = KNeighborsClassifier()
# classifier = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', n_neighbors=5, p=2, weights='uniform')
classifier = DecisionTreeClassifier()
# classifier = NeuralNet(50, learn_rate=1e-2)
# classifier = SGDClassifier(loss='log', penalty='l1')


# classifier.fit(train_arrays, train_labels, fine_tune=False, maxiter=500, SGD=True, batch=150, rho=0.9)
classifier.fit(train_arrays, train_labels)
# print train_arrays, train_labels

log(NOTICE, "score: %f" % classifier.score(train_arrays, train_labels))
# from sklearn.manifold import TSNE
# import numpy as np
# import matplotlib.pyplot as plt
#
# ts = TSNE(2)
# reduced_vecs = ts.fit_transform(np.concatenate((train_arrays[0:line_count], train_arrays[line_count:line_count * 2])))
#
# #color points by word group to see if Word2Vec can separate them
# for i in range(line_count * 2):
#     if i < len(train_arrays[0:line_count]):
#         #food words colored blue
#         color = 'b'
#     else:
#         color = 'g'
#     plt.plot(reduced_vecs[i, 1], reduced_vecs[i, 0], marker='o', color=color, markersize=4)
#
# plt.show()

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


client = MongoClient(address, port)
db = client[project]
words = []
# search_json = {'$or': [{'keyword': '社会保险'},{'keyword': '社保'}]}
# search_json = {'keyword': '医疗保险'}
# utc_end = datetime.datetime(2015, 10, 26, 0, 0, 0, 0, tzinfo=TZCHINA)
# utc_start = datetime.datetime(2015, 10, 1, 0, 0, 0, 0, tzinfo=TZCHINA)
# search_json = {'$and': [{"timestamp": {"$lt": utc_end}}, {"timestamp": {"$gt": utc_start}}]}
# search_json = {"timestamp": {"$gt": utc_end}}
search_json = {}

posts = db.posts.find(search_json)
count = db.posts.find(search_json).count()

# Round One, parsing those with replies
log(NOTICE, 'Round One')
# adding sentiment is 0 is a temporary strategy. since the number of replies are increasing.
posts = db.posts.find({"replies": {"$ne": []}, "sentiment": {"$eq": 0}})
count = db.posts.find({"replies": {"$ne": []}}).count()
i = 0
for post in posts:
    line = seg_sentence(post['content'])
    a = model.infer_vector(line.split(u' '))
    s_index = classifier.predict(a)
    log(NOTICE, '%d %s' % (s_index, post['content'].encode('gbk', 'ignore')))

    f_flag = False
    # db.posts.update({'mid': post['mid']}, {'$set': {'sentiment': s_index}})
    re_count = len(post['replies'])
    re_i = 1

    for reply in post['replies']:
        re = reply['content']
        if len(reply['content']) >= 2:
            if reply['content'][:2] == u'//':
                f_flag = True
        if len(reply['content']) >= 4:
            if reply['content'][:4] == u'转发微博' or reply['content'][:4] == u'轉發微博' or str(reply['content'][:4]).lower() == u'repo':
                f_flag = True
        if reply['content'] == '':
            f_flag = True

        if f_flag is True:
            re_index = s_index
        else:
            line = seg_sentence(reply['content'])
            a = model.infer_vector(line.split(u' '))
            re_index = classifier.predict(a)
            log(NOTICE, '%d %s' % (re_index, post['content'].encode('gbk', 'ignore')))
        # db.posts.update({'mid': reply['mid']}, {'$set': {'sentiment': re_index}})
        # log(NOTICE, 'Reply #%d of post #%d, %d remains. Content: %s' % (re_i, i, count - re_i, re.encode('gbk', 'ignore')))
        re_i += 1

    # log(NOTICE, '#%d, %d remains. Content: %s' % (i, count - i, a.encode('gbk', 'ignore')))
    i += 1

# Round Two, parsing those without replies
log(NOTICE, 'Round Two')
posts = db.posts.find({"replies": {"$eq": []}, "sentiment": {"$eq": 0}})
count = db.posts.find({"replies": {"$ne": []}}).count()
i = 1
for post in posts:
    line = seg_sentence(post['content'])
    a = model.infer_vector(line.split(u' '))
    s_index = classifier.predict(a)
    log(NOTICE, '%d %s' % (s_index, post['content'].encode('gbk', 'ignore')))
    # db.posts.update({'mid': post['mid']}, {'$set': {'sentiment': s_index}})
    # log(NOTICE, '#%d, %d remains. Content: %s' % (i, count - i, a.encode('gbk', 'ignore')))
    i += 1

log(NOTICE, 'mission completes.')

# a = model.infer_vector(u'医疗 改革 不错'.split(u' '))
# b = model.infer_vector(u'最 恶毒 不足以 形容'.split(u' '))
# print classifier.score(train_arrays, train_labels)
# # print classifier.predict(train_arrays[130])
# print classifier.predict([a, b, model.docvecs['NEG_2'], model.docvecs['POS_2']])
# for i in range(100):
#     print classifier.predict([model.docvecs['NEG_' + str(i)]])
# print "========POS=============="
# for i in range(100):
#     print classifier.predict([model.docvecs['POS_' + str(i)]])
# # print classifier.predict_proba([a, b, model.docvecs['NEG_2'], model.docvecs['POS_2']])
