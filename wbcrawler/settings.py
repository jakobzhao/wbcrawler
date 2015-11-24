# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from pytz import timezone
TZCHINA = timezone('Asia/Chongqing')
UTC = timezone('UTC')

BAIDU_AK = 'Y4wB8DznamkwhY8RxDiYNSHS'
# BAIDU_AK = 'fGnFQVLoY6AgmPM1spgYvsD9'
PB_KEY = 'bYJFjyvIYWbn5vg2eNiFmcapjLu1PUTL'
EMAIL_PASSWORD = 'nanjing1212'
TIMEOUT = 60
STOP_WORDS = list(u' ：@:～~：:。·-—，,？?！!&*#[]；;：:、“”【】[]《》<>|()（）⊙▽…/↓→=_的了吗咯哦呗')
# STOP_WORDS = list(u'：:～~：:。·-—，,？?！!&*#[]；;：:、“”【】[]《》<>|()（）…/↓→=_的了吗咯哦是呗交买卖说就有都也要这和能看到给个为上得把只用与着将做拿中事从打点')
STOP_WORDS.extend([u'http', u'...'])
# STOP_WORDS.extend([u'http', u'...', u'应该', u'一个', u'买', u'知道'])

RE_STARTWITH = [u'//', u'收藏', u'轉發微博', u'轉發微博', u'转了', u'转发', u'转发微博', u'转发微薄', u'转发收藏', u'转吧', u'转来', u'转播', u'转走', u'转起', u'转转', u'转需', u'Repost', u'repost', u'mark']
RE_EQUALTO = [u' //', u'马', u'转', u'马克', u'', u' ']

# my id and key
# TENCENT_SECRET_ID = 'AKID8afsi3KB4SaFEgTFtBJpyVjGJOB5uawg'
# TENCENT_SECRET_KEY = 'W6OpvVwoIJ2rsHVPZnzlfHv8JiYeQdRf'

# fenglin

TENCENT_SECRET_ID = 'AKID3isJNqT56hlSiIPEM3NP7v3RQLchrA7a'
TENCENT_SECRET_KEY = 'KCjkjm8fjym4u8pVyMFREZTJiuGFKGo2'
