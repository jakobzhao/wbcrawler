# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''
import cookielib

import mechanize

from settings import *

br = mechanize.Browser()
# cookie jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# 加上各种协议
br.set_handle_equiv(True)
# br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.set_proxies({"http": "165.139.179.225:8080"})
# 加上自己浏览器头部，和登陆了通行证的cookie
br.addheaders = [('User-Agent',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'),
                 ('Cookie', ck)]

# for f in br.forms():
#     print f
# br.select_form(nr=0)
# print br
# br.form['username']='13580491531'
# br.form['password']='buhui1314iliting'
# br.submit()
# br.add_password('http://login.sina.com.cn/signup/signin.php?entry=sso','13580491531','buhui1314iliting')
# 登陆新浪通行证
# br.open('http://login.sina.com.cn/signup/signin.php?entry=sso')

url = "http://weibo.cn/5367032743/info?rl=100"
url = "http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F5367032743%2Finfo%3Frl%3D100&backTitle=%CE%A2%B2%A9&vt="
url = "http://www.baidu.com"
rd = br.open(url, timeout=20)
final_url = rd.geturl().decode("utf-8")
rd = br.open(final_url, timeout=20)
f = open("1.html", "w")
f.write(rd.read())
f.close()
print br.geturl()
for
    print "32"
