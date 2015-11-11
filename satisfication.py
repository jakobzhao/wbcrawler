# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from snownlp.sentiment import Sentiment
from pymongo import MongoClient, DESCENDING, ASCENDING
from wbcrawler.log import *
from wbcrawler.utils import get_name_from_content


def main():
    address = "localhost"
    port = 27017
    project = 'five_local'
    client = MongoClient(address, port)
    # db = client[project]
    db = client['five']
    b = []

    try:
        s_t = Sentiment()
        s_t.load(fname=project + '/sentiment.marshal')
    except ZeroDivisionError:
        pass

    # Round One, parsing those with replies
    log(NOTICE, 'Round One')
    # adding sentiment is 0 is a temporary strategy. since the number of replies are increasing.
    posts = db.posts.find({"replies": {"$ne": []}, "sentiment": {"$eq": 0}})
    count = db.posts.find({"replies": {"$ne": []}}).count()
    i = 1
    for post in posts:
        a = post['content']
        a = preprocess_content(a)
        s_t.handle(a)
        s_index = s_t.classify(a)
        f_flag = False
        db.posts.update({'mid': post['mid']}, {'$set': {'sentiment': s_index}})
        re_count = len(post['replies'])
        re_i = 1

        for reply in post['replies']:
            re = reply['content']
            if len(reply['content']) >= 2:
                if reply['content'][:2] == u'//':
                    f_flag = True
            if len(reply['content']) >= 4:
                if reply['content'][:4] == u'转发微博' or reply['content'][:4] == u'轉發微博' or reply['content'][
                                                                                         :4] == u'repo':
                    f_flag = True
            if reply['content'] == '':
                f_flag = True

            if f_flag is True:
                re_index = s_index
            else:
                re = preprocess_content(reply['content'])
                s_t.handle(re)
                re_index = s_t.classify(re)
            db.posts.update({'mid': reply['mid']}, {'$set': {'sentiment': s_index}})
            log(NOTICE, 'parsing reply #%d of post #%d, %d remains. post content: %s' % (
            re_i, i, count - re_i, re.encode('gbk', 'ignore')))
            re_i += 1

        log(NOTICE, 'parsing post #%d, %d remains. post content: %s' % (i, count - i, a.encode('gbk', 'ignore')))
        i += 1

    # Round Two, parsing those without replies
    log(NOTICE, 'Round Two')
    posts = db.posts.find({"replies": {"$eq": []}, "sentiment": {"$eq": 0}})
    count = db.posts.find({"replies": {"$ne": []}}).count()
    i = 1
    for post in posts:
        a = post['content']
        a = preprocess_content(a)
        s_t.handle(a)
        s_index = s_t.classify(a)
        db.posts.update({'mid': post['mid']}, {'$set': {'sentiment': s_index}})
        log(NOTICE, 'parsing post #%d, %d remains. post content: %s' % (i, count - i, a.encode('gbk', 'ignore')))
        i += 1

    # b.append(a)
    # log(NOTICE, '%f, %s' % (s_t.classify(a), a.encode('gbk', 'ignore')))
    log(NOTICE, 'mission completes.')


def preprocess_content(a):
    names = get_name_from_content(a)

    url = ''
    if u'http://t.cn/' in a:
        url_start = a.find(u'http://t.cn/')
        url = a[url_start:url_start + 19]
        # print url

    if len(a) >= 2:
        a = a.split('//')[0]

    a = a.replace(url, '').replace(u'转发微博', '').replace(u'轉發微博', '').replace(u'repost', '')

    i = 1
    for name in names:
        a = a.replace(name, u'用户' + unicode(i))
        i += 1
    # if a == '':
    return a

if __name__ == '__main__':
    main()
