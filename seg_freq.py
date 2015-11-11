# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from pymongo import MongoClient, DESCENDING, ASCENDING
from wbcrawler.log import *
from wbcrawler.utils import get_name_from_content
from snownlp import SnowNLP as sn
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    f = open('five_freq.txt', 'r')
    f2 = open('five_freq2.txt', 'a')
    for line in f.readlines():
        # print line
        # print line
        a = line.split(u' ')
        w = a[0]
        print w
        times = int(int(a[1]) / 10.0)
        print times
        # print a
        t = ''
        for i in range(times):
            t += w + ' '
        f2.write(t)
    log(NOTICE, 'mission completes.')


if __name__ == '__main__':
    main()
