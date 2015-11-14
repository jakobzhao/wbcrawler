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
# from wbcrawler.utils import get_name_from_content

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_name_from_content(content):
    names = []
    if u'@' not in content:
        return names

    parts = content.split(u"@")

    for part in parts[1:]:
        comma_index = -1
        if u':' in part or u'：' in part:
            if part.find(u':') == -1:
                comma_index = part.find(u'：')
            elif part.find(u'：') == -1:
                comma_index = part.find(u':')
            else:
                if part.find(u':') > part.find(u'：'):
                    comma_index = part.find(u'：')
                else:
                    comma_index = part.find(u':')

        space_index = part.find(u' ')
        if part == parts[-1] and space_index == -1:
            space_index = len(part)

        if comma_index == -1 and space_index == -1:
            name = u'@' + part
        elif comma_index == -1 and space_index != -1:
            name = u'@' + part[:space_index]
        elif comma_index != -1 and space_index == -1:
            name = u'@' + part[:comma_index]
        elif comma_index < space_index:
            name = u'@' + part[:comma_index]
        elif comma_index > space_index:
            name = u'@' + part[:space_index]
        else:
            name = u'@' + part
        names.append(name)

    return names


def preprocess_content(content):
    names = get_name_from_content(content)
    url = ''
    if u'http://t.cn/' in content:
        url_start = content.find(u'http://t.cn/')
        url = content[url_start:url_start + 19]
        # print url

    if len(content) >= 2:
        content = content.split('//')[0]

    content = content.replace(url, '').replace(u'转发微博', '').replace(u'轉發微博', '').replace(u'repost', '')

    i = 1
    for name in names:
        content = content.replace(name, u'用户' + unicode(i))
        i += 1
    return content


# address = "localhost"
# port = 27017
# project = 'five'
# client = MongoClient(address, port)
# db = client[project]
# f = open('t.txt', 'a')


# posts = db.posts.find()
# count = db.posts.find().count()

words = []
t = u''
i = 0
fname = 'train-neg.txt'

with open(fname) as f:
    for line in f.readlines():
        line_tmp = preprocess_content(line)
        print line_tmp

log(NOTICE, 'mission completes.')

if __name__ == '__main__':
    # main()
    pass
