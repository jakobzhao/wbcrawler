# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys

sys.path.append("/home/bo/.local/lib/python2.7/site-packages")
sys.path.append("/home/bo/Workspace/wbcrawler")
sys.path.append("/home/bo/Workspace/wbcrawler/five")

from wbcrawler.parser import parse_keyword
from wbcrawler.weibo import sina_login
from wbcrawler.database import register, unregister, create_database, unlock_robots
from wbcrawler.log import *
from settings import SETTINGS

# First Round: 129 minutes
# unlock the unreleased robots
unlock_robots(SETTINGS)

# start to crawl
start = datetime.datetime.now()
account = register(SETTINGS)
browser = sina_login(account)
accounts = [account]
try:
    db = create_database(SETTINGS)
    for keyword in SETTINGS['keywords']:
        round_start = datetime.datetime.now()
        t = SETTINGS['robot_num']
        for i in range(0, t):
            response = parse_keyword(keyword, browser, SETTINGS)
            if response:
                log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
            else:
                # 入栈
                account = register(SETTINGS)
                browser = sina_login(account)
                accounts.append(account)
            i += 1
        # except KeyboardInterrupt, e:
except:
    browser.close()
    log(ERROR, 'An error occurs.', 'crawler.py')
finally:
    # 出栈
    for account in accounts:
        unregister(SETTINGS, account)
    log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
