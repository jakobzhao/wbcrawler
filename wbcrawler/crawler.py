# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''


# 16.7 minutes per keyword in average
# so, if there are 10 keywords, 2 hour and 50 minutes in total
# I will suggest to implement this script every six hour per day.
# running per 6 hours
import datetime

from wbcrawler.utils import parse_keyword, sina_login, register, unregister, create_database
from settings import *


# First Round: 20 + 88 mins: 2 hours
# Second Round: 76 mins
# a following Round: 65 mins
# 10/15/2015 64 mins

# 剔除重复项
# 任务布置
# 加入logging system

# wbcrawler="http://login.sina.com.cn/cgi/pin.php?r=35157368&s=0"

fresh = False


start = datetime.datetime.now()
account = register('local', address, port)
browser = sina_login(account)

db = create_database(project, address, port, fresh)
for keyword in KEYWORDS:
    round_start = datetime.datetime.now()
    parse_keyword(db, keyword, browser)
    print 'The keyword "%s" has been processed in %d seconds.' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds))
# except KeyboardInterrupt, e:
try:
    browser.close()
except:
    pass
unregister('local', address, port, account)

print 'The keywords have been processed in "%d" minutes.' % int((datetime.datetime.now() - start).seconds / 60)
if __name__ == '__main__':
    pass
