# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

import datetime

from wbcrawler.parser import parse_repost
from wbcrawler.weibo import sina_login
from wbcrawler.database import register, unregister, create_database
from wbcrawler.log import *

project = 'five'
address = 'localhost'
port = 27017

start = datetime.datetime.now()
account = register('local', address, port)
browser = sina_login(account)

db = create_database(project, address, port)
i = 0
while True:
    round_start = datetime.datetime.now()
    posts = db.posts.find({"fwd_count": {"$gt": 10}})  # .limit(COUNT)
    parse_repost(db, browser, posts)
    log(NOTICE, 'The completion of this round. Time: %d sec(s)' % int((datetime.datetime.now() - round_start).seconds))
    i += 1
browser.close()
unregister('local', address, port, account)
log(NOTICE, 'Complete. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass