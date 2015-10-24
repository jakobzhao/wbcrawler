# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


from random import randint


# hanzi to pinyin
def to_pinyin(keyword):
    from pypinyin import lazy_pinyin
    py = lazy_pinyin(unicode(keyword))
    result = ''
    for i in py:
        result += i
    return result


def get_interval_as_human(low=18, high=22):
    return randint(low, high)

