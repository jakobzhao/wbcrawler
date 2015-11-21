# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys
from wbcrawler.log import *
from wbcrawler.seg import seg_sentence_tag

reload(sys)
sys.setdefaultencoding('utf-8')

project = 'five'
fname = project + '/negative.txt'
nname = project + '/neg.txt'
f2 = open(nname, 'w')

with open(fname) as f:
    lines = f.readlines()
i = 0
s = []
for line in lines:
    sentence = seg_sentence_tag(line)
    log(NOTICE, sentence.encode('gbk', 'ignore'))
    print i
    if sentence == '':
        print "========================"
        continue
    f2.write(sentence[:-1] + '\n')
    i += 1
f.close()
f2.close()

log(NOTICE, 'mission completes.')

if __name__ == '__main__':
    # main()
    pass
