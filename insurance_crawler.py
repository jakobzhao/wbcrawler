# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

from wbcrawler.parser import parse_keyword
from wbcrawler.weibo import sina_login
from wbcrawler.database import register, unregister, create_database
from wbcrawler.log import *

# First Round: 129 minutes

project = 'insurance'
address = 'localhost'
port = 27017
# fresh = True


KEYWORDS = ['社会保险', '社保', '商业保险', '医疗保险', '医保', '医院 报销']

start = datetime.datetime.now()
account = register('local', address, port)
browser = sina_login(account)
try:
    db = create_database(project, address, port)
    for keyword in KEYWORDS:
        round_start = datetime.datetime.now()
        parse_keyword(db, keyword, browser)
        log(NOTICE, 'The completion of processing the keyword "%s". Time: %d sec(s)' % (keyword.decode('utf-8'), int((datetime.datetime.now() - round_start).seconds)))
        # except KeyboardInterrupt, e:
except:
    try:
        browser.close()
    except:
        pass
finally:
    unregister('local', address, port, account)

log(NOTICE, 'The completion of processing all keywords. Time: %d min(s)' % int((datetime.datetime.now() - start).seconds / 60))

if __name__ == '__main__':
    pass
