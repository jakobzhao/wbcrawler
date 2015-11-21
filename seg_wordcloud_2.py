# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from wbcrawler.log import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
project = 'five'


def main():
    f = open('%s/freq_all.txt' % project, 'r')
    f2 = open('%s/five_all2.txt' % project, 'w')
    for line in f.readlines():
        # print line
        # print line
        a = line.split(u' ')
        w = a[0]
        print w.encode('gbk', 'ignore')
        times = int(int(a[1]) / 20.0)
        print times
        # print a
        t = ''
        for i in range(times):
            t += w + ' '
        f2.write(t + '\n')
    log(NOTICE, 'mission completes.')

if __name__ == '__main__':
    main()
