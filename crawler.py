# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


from wbcrawler.parser import parse_keyword
from wbcrawler.weibo import sina_login
from wbcrawler.database import register, unregister, create_database
from wbcrawler.log import *
from settings import SETTINGS

# First Round: 129 minutes
# First Round: 20 + 88 mins: 2 hours
# Second Round: 76 mins
# a following Round: 65 mins
# 10/15/2015 64 mins


# KEYWORDS = ['政府', '中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会']
# KEYWORDS_CLIMATE = ['气候变化', '全球变暖']
# KEYWORDS = ['政府', '中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会']
# KEYWORDS = ['中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会']
# KEYWORDS = ['县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会']
# KEYWORDS = ['气候变化', '全球变暖']


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
