# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
import sys

from wbcrawler.sna import generate_sematic_network

# generate_sematic_network(keywords=[u'社保', u'社会保险'], depth=[10, 10, 10], w2v_file=u'insurance/w2v.bin', gexf_file=u"insurance/社保.gexf")
# generate_sematic_network(keywords=[ u'亏空', u'缺口', u'财政补贴'], depth=[10, 10, 10], w2v_file=u'insurance/w2v.bin', gexf_file=u"insurance/社保亏空.gexf") #  u'社保亏空'
# generate_sematic_network(keywords=[u'延退', u'延迟', u'65'], depth=[10, 10, 10], w2v_file=u'insurance/w2v.bin', gexf_file=u"insurance/延迟.gexf") #  u'社保亏空'
# generate_sematic_network(keywords=[u'公积金'], depth=[10, 10, 10], w2v_file=u'insurance/w2v.bin', gexf_file=u"insurance/公积金.gexf")
generate_sematic_network(keywords=[u'报销'], depth=[10, 10, 10], w2v_file=u'insurance/w2v.bin', gexf_file=u"insurance/报销.gexf")
