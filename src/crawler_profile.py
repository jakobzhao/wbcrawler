# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from utils import parse_profile, weibo_manual_login


# ProjectName
project_name = "weibo"

# Variables
keyword = '雾霾'

# V10 hc563blnsg@163.com
ck = 'SINAGLOBAL=71.233.245.138_1443916664.306643; UOR=,login.sina.com.cn,; ULV=1444533746724:6:6:6:128.103.193.220_1444533692.708269:1444533691849; U_TRS1=0000008a.31b230f.5611503b.60a80b4a; sso_info=v02m6alo5qztY2alrmpl7WIpZGTlKWQo4CljoSYpZGTnKWOk5ilkJSYpZGTlKWQlJCljpOAto6DmLiJp5WpmYO0tYyTkLKNg4yxjbOQtQ==; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYTG863MkPLheimog5d7c_; Apache=128.103.193.220_1444533692.708269; SUB=_2A257HaZQDeTxGeNP71AV8y_LzzmIHXVYapCYrDV_PUNbuNBuLRXhkW95xZNoC3_KW-_S44QmUoB0s3tVOQ..; SUS=SID-5142431745-1444533760-GZ-1tq85-fa3ae86b47c6ec5ceaab4ca6dee65772; SUE=es%3Dee63ed2ef156ea0f69060e2e3d880f76%26ev%3Dv1%26es2%3Da3c8149d6982eecc3a8d08e71de4d052%26rs0%3DI%252Bnn3ddtLTnULoBjVJ0gd74Rs%252B6xEUdQbhw%252F4FVVv90lcXhE0xEYQyj%252F0KgGvwveuSLo5GM8jVdb2mNDp3ZNgzX0l6T0GdXAQl8HzxRSMCzqubkLGciyyKaO%252FO3uslMF9YmzN2pUMFyK%252BoSVjQbUjAA4y%252BsjstYQuLyIoUfdRtQ%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1444533760%26et%3D1444620160%26d%3D40c3%26i%3D5772%26us%3D1%26vf%3D1%26vt%3D4%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5142431745%26user%3Dhc563blnsg%2540163.com%26ag%3D4%26name%3Dhc563blnsg%2540163.com%26nick%3DMini_R%25E5%25B0%258F%25E7%2596%25AF%25E5%25AD%25906868%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dhc563blnsg%2540163.com%26os%3D%26fmp%3D%26lcp%3D2015-08-21%252014%253A21%253A57; ALF=1476069760; cREMloginname=hc563blnsg%40163.com; tgc=TGT-NTE0MjQzMTc0NQ==-1444533760-hk-D0E3413E59F324F00D4018D60EBD1BA3; ALC=ac%3D59%26bt%3D1444533760%26cv%3D5.0%26et%3D1476069760%26uid%3D5142431745%26vf%3D1%26vt%3D4%26es%3D43bf3c8f217a250b6bb21b7a731ecefd; LT=1444533760'
# jakobzhao
ck = 'SINAGLOBAL=1884590915869.9214.1438381097619; __gads=ID=df5a0ca866aad3b1:T=1443921627:S=ALNI_MbwlKae7qpSR_eBjgPf-hmr21zUBg; __utma=15428400.166963640.1438485640.1438485640.1444192045.2; __utmz=15428400.1438485640.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); lzstat_uv=2573527597108302786|2893156; myuid=5142431745; _s_tentry=news.ifeng.com; UOR=news.ifeng.com,widget.weibo.com,news.ifeng.com; Apache=4986512395553.291.1444535043133; ULV=1444535043157:58:19:13:4986512395553.291.1444535043133:1444499285539; SUHB=0sqAlwmC6BDULE; SRT=E.vAfoiqzpJDJqiOvnv!yOAvmBvXvCvXMdF52-vnEXBvzvvv4mXFaB3vRmvvvm8XVmPYkBWXXFvRvvvXN1CXzvBvrBJAtBvA0BvMmCvvzNvAz7*B.vAflW-P9Rc0lR-ykADvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsT8uGiF0uSQYKJdi6OEEdVFMwi!ugi49ndDPIJeA7; SRF=1444540406; un=jakobzhao@gmail.com; wvr=6; _ga=GA1.2.166963640.1438485640'
br = weibo_manual_login()
parse_profile(project_name, keyword, br)
if __name__ == '__main__':
    pass
