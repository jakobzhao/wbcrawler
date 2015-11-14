# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from gensim import corpora, models, similarities
import jieba

sentences = ["我喜欢吃土豆", "土豆是个百搭的东西", "我不喜欢今天雾霾的北京"]

words = []
for doc in sentences:
    words.append(list(jieba.cut(doc)))

dic = corpora.Dictionary(words)
corpus = [dic.doc2bow(text) for text in words]
print corpus

for word, index in dic.token2id.iteritems():
    print word + u" 编号为:" + str(index)

print '=========tfidf=============='  # bag of words importance
tfidf = models.TfidfModel(corpus)  # tfidf 的建立，依赖于corpus
vec = [(0, 1), (4, 1)]  # 吃东西
print tfidf[vec]
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc

print "=========simularities======="
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=15)
sims = index[tfidf[vec]]  # sim 依赖于bow，所以先用要用tfidf 处理vec
print list(enumerate(sims))

print '===========LSI=============='  # 建立主题
# build the LSI model instance
lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=2)  # 看来tfidf是必不可少的一步
lsiout = lsi.print_topics(2)
print lsiout[0][1]
print lsiout[1][1]

corpus_lsi = lsi[corpus_tfidf]
for doc in corpus_lsi:
    print doc

print u'===========simularity 雾霾=============='
# use the LSI model to find its simularity with a specific word
index = similarities.MatrixSimilarity(lsi[corpus])
query = "雾霾"
query_bow = dic.doc2bow(list(jieba.cut(query)))
print query_bow
query_lsi = lsi[query_bow]
print query_lsi

sims = index[query_lsi]
print list(enumerate(sims))
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print sort_sims
