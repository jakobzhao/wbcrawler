# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

import numpy as np #导入numpy
import pandas as pd
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')


def yuchuli(s, m): #导入文本，文本预处理
    wenjian = pd.read_csv(s, delimiter='     xxx     ', encoding='utf-8', header= None, names=['comment']) #导入文本
    wenjian = wenjian['comment'].str.replace('(<.*?>.*?<.*?>)', '').str.replace('(<.*?>)','').str.replace('(@.*?[ :])',' ') #替换无用字符
    wenjian = pd.DataFrame({'comment':wenjian[wenjian != '']})
    wenjian.to_csv(s, header=False, index=False)
    wenjian['mark'] = m #样本标记
    return wenjian.reset_index()

neg = yuchuli('five/negative.txt', -1)
pos = yuchuli('five/positive.txt', 1)

mydata = pd.concat([neg, pos], ignore_index=True)[['comment', 'mark']] #结果文件
#预处理基本结束


#开始加载情感词典
negdict = [] #消极情感词典
posdict = [] #积极情感词典
nodict = [] #否定词词典
plusdict = [] #程度副词词典
dpath = 'wbcrawler/training_set'
sl = pd.read_csv('%s/ntusd_negative.txt' % dpath, header=None, encoding='utf-8')
for i in range(len(sl[0])):
    negdict.append(sl[0][i])
sl = pd.read_csv('%s/ntusd_positive.txt' % dpath, header=None, encoding='utf-8')
for i in range(len(sl[0])):
    posdict.append(sl[0][i])
sl = pd.read_csv('%s/no.txt' % dpath, header=None, encoding='utf-8')
for i in range(len(sl[0])):
    nodict.append(sl[0][i])
# sl = pd.read_csv('dict/plus.txt', header=None, encoding='utf-8')
# for i in range(len(sl[0])):
#     plusdict.append(sl[0][i])
#加载情感词典结束


#预测函数
#def predict(s, negdict, posdict, nodict, plusdict):
def predict(s, negdict, posdict, nodict):
    p = 0
    sd = list(jieba.cut(s))
    for i in range(len(sd)):
        if sd[i] in negdict:
            if i>0 and sd[i-1] in nodict:
                p = p + 1
            elif i>0 and sd[i-1] in plusdict:
                p = p - 2
            else: p = p - 1
        elif sd[i] in posdict:
            if i>0 and sd[i-1] in nodict:
                p = p - 1
            elif i>0 and sd[i-1] in plusdict:
                p = p + 2
            elif i>0 and sd[i-1] in negdict:
                p = p - 1
            elif i<len(sd)-1 and sd[i+1] in negdict:
                p = p - 1
            else: p = p + 1
        elif sd[i] in nodict:
            p = p - 0.5
    return p
#预测函数结束

#简单的测试
tol = 0
yes = 0
mydata['result'] = 0
for i in range(len(mydata)):
    print (mydata.loc[i, 'comment']).encode('gbk', 'ignore')
    tol = tol + 1
    print "score: %f" % predict(mydata.loc[i, 'comment'], negdict, posdict, nodict)*mydata.loc[i, 'mark']
