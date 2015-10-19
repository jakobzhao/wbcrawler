# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 9, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

import datetime

from wbcrawler.utils.utils import sina_login, register, unregister, create_database, parse_path
from backup.five.settings import *

start = datetime.datetime.now()
account = register('local', address, port)
browser = sina_login(account)

try:
    db = create_database(project, address, port)
    i = 0
    while True:
        round_start = datetime.datetime.now()
        parse_path(db, browser, COUNT)
        print "This is the %d rounds. the paths fo %d users will be harvested per round. Time: %d mins." % (i, COUNT, int((datetime.datetime.now() - round_start).seconds / 60))
        i += 1

# except KeyboardInterrupt:
except:
    print "Program is interrupted."

finally:
    browser.close()
    unregister('local', address, port, account)
    print "Cost Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60)

if __name__ == '__main__':
    pass
