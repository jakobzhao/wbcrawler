# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from snownlp import sentiment
from wbcrawler.log import *
from os import remove

proj = "five"


def sentiment_training(project):
    start = datetime.datetime.now()
    path = '../%s/' % project

    neg_file = '%snegative.txt' % path
    pos_file = '%spositive.txt' % path

    neg_tmpfile = '%snegative_tmp.txt' % path
    pos_tmpfile = '%spositive_tmp.txt' % path

    f_s = open(pos_file, 'r')
    data_pos = f_s.read()
    f_s = open('training_set/keenage_positive.txt', 'r')
    data_keenage_pos = f_s.read()
    f_s = open('training_set/ntusd_positive.txt', 'r')
    data_ntusd_pos = f_s.read()

    f_t = open(pos_tmpfile, 'w')
    f_t.write(data_pos + '\n' + data_keenage_pos + '\n' + data_ntusd_pos + '\n')

    f_s = open(neg_file, 'r')
    data_neg = f_s.read()
    f_s = open('training_set/keenage_negative.txt', 'r')
    data_keenage_neg = f_s.read()
    f_s = open('training_set/ntusd_negative.txt', 'r')
    data_ntusd_neg = f_s.read()

    f_t = open(neg_tmpfile, 'w')
    f_t.write(data_neg + '\n' + data_keenage_neg + '\n' + data_ntusd_neg + '\n')

    f_t.close()
    f_s.close()

    sentiment.train(neg_tmpfile, pos_tmpfile)
    sentiment.save(path + 'sentiment.marshal')

    remove(neg_tmpfile)
    remove(pos_tmpfile)
    log(NOTICE, 'the sentiment file has generated. Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))
    return


sentiment_training(proj)
