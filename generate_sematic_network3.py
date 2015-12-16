# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
from wbcrawler.sna import generate_sematic_network3

keyword = u'商业保险'

f = open("kuikong.txt", 'r')
lines = f.readlines()
f.close()

related_keywords = []
for line in lines:
    related_keywords.append(unicode(line.split(' ')[0]))

# related_keywords = [u'收益率', u'缺口', u'入市', u'财政补贴', u'养老金', u'多交', u'稳健', u'安全感', u'交够', u'国产', u'白干', u'药丸', u'交满', u'耍无赖', u'办事效率', u'咒骂', u'决策层', u'少领', u'当权者', u'八成', u'财', u'人情', u'疑问', u'叫好', u'国有资产']
# related_keywords = [u'买份', u'出租', u'压力', u'强制', u'很少', u'个人感觉', u'寿险', u'养家糊口', u'顾客', u'保险公司', u'出资', u'品牌', u'五险', u'出租车', u'商保', u'消费型', u'养育', u'缺位', u'独立', u'退出', u'代替', u'医托', u'基层医院', u'青蒿素', u'证券', u'保险合同', u'废除', u'东亚', u'养儿防老', u'社会主义', u'野蛮', u'小康', u'旅行', u'医疗系统', u'两孩', u'意外险', u'国税局', u'寄钱', u'跳槽', u'维持', u'保险经纪', u'开除', u'工资卡', u'上当', u'税收', u'公务人员', u'捆绑', u'不买', u'保单', u'投资方']
related_keywords = [u'风险', u'社会福利', u'意外险', u'医疗系统', u'流动人口', u'产业', u'寿险', u'社保', u'社会保险', u'延退', u'养老', u'医院', u'保险公司', u'两孩', u'消费型', u'保险合同', u'国税局', u'保单', u'公务人员', u'保险经纪', u'养儿防老', u'社会主义', u'跳槽', u'医托', u'压力', u'五险', u'退出', u'独立']
generate_sematic_network3(keyword, related_keywords, threshold=0.4, depth=10, w2v_file=u'insurance/w2v.bin', gexf_file=u"商保-3.gexf")
