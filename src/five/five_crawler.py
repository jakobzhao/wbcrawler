# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import datetime

from src.settings import *
from src.utils import parse_keyword, sina_login, register, unregister, create_database

project = 'five'

start = datetime.datetime.now()
account = register('local', address, port)
browser = sina_login(account)

db = create_database(project, address, port, fresh)
for keyword in KEYWORDS_FIVE:
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
