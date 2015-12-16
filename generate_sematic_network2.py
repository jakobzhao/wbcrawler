# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
from wbcrawler.sna import generate_sematic_network2

keyword = u'商业保险'
# related_keywords = [u'收益率', u'缺口', u'入市', u'财政补贴', u'养老金', u'多交', u'稳健', u'安全感', u'交够', u'国产', u'白干', u'药丸', u'交满', u'耍无赖', u'办事效率', u'咒骂', u'决策层', u'少领', u'当权者', u'八成', u'财', u'人情', u'疑问', u'叫好', u'国有资产']
related_keywords = []

f = open("sb-60.txt", 'r')
lines = f.readlines()
f.close()
for line in lines:
    related_keywords.append(unicode(line.split(' ')[0]))
generate_sematic_network2(keyword, related_keywords, threshold=0.80, w2v_file=u'insurance/w2v.bin', gexf_file=u"商业保险-3.gexf")
