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
sys.path.append("/home/bo/Workspace/wbcrawler/insurance")

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
try:
    db = create_database(SETTINGS)
    for keyword in SETTINGS['keywords']:
        round_start = datetime.datetime.now()
        parse_keyword(db, keyword, browser)
        log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
        # except KeyboardInterrupt, e:
except:
    browser.close()
    log(ERROR, 'An error occurs.', 'Crawler.py')
finally:
    unregister(SETTINGS, account)
    log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
