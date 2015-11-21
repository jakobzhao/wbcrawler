# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from pymongo import MongoClient
from wbcrawler.log import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    address = "localhost"
    port = 27017
    project = 'insurance'
    client = MongoClient(address, port)
    # db = client[project]
    db = client[project]

    # adding sentiment is 0 is a temporary strategy. since the number of replies are increasing.
    posts = db.posts.find()
    count = posts.count()
    i = 1
    for post in posts:
        content = post['content']
        count_len = len(content)
        update = False
        if count_len >= 2:
            if content[0:2] == u"//":
                content = u'//'
                update = True
            else:
                if u"//" in content:
                    content = content[0:content.index(u'//')] + u"//"
                    update = True
        elif count_len >= 4:
            if content[0:4] == u'转发微博' or content[0:4] == u'轉發微博' or str(content[0:4]).lower() == u'repo':
                content = u'转发微博'
                update = True
        else:
            pass
        if update:
            db.posts.update({'mid': post['mid']}, {'$set': {'content': content}})

        log(NOTICE, 'parsing post #%d, %d remains. post content: %s' % (i, count - i, content.encode('gbk', 'ignore')))
        i += 1

    log(NOTICE, 'mission completes.')


if __name__ == '__main__':
    main()
