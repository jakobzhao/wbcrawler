# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

# retweet type
# 1: reply
# 2: comment
# 3: reply to a comment
# 4: a reply and a comment


# status type
# 0: original
# 1: reply
# 2: comments

TOKEN = '2.00UjtoID_vpWMD6803c07a48xPUuYC'
# TOKEN = '2.00UjtoID_vpWMD1961e78a7fdHoBSB' # 旧梦

COUNT = 50
COUNT2 = 100

WAITING_TIME = 18
EMAIL_PASSWORD = 'nanjing1212'

# V10 hc563blnsg@163.com
ck = 'SINAGLOBAL=23.127.5.35_1438381099.222158; UOR=www.google.com,blog.sina.com.cn,; U_TRS1=00000023.58191642.55bccd5d.3f434700; vjuids=-28335e30f.14ee982b46a.0.7a397cda; SGUID=1438436749265_34644990; lxlrtst=1443666296_o; vjlast=1443843509; ArtiFSize=14; lxlrttp=1443792570; Apache=71.233.245.138_1443914418.595857; ULV=1443937801395:23:4:1:71.233.245.138_1443914418.595857:1443843507572; U_TRS2=0000008a.a4996c2f.5610bec3.0dd368b8; ULOGIN_IMG=hk-de60d3a40d3c439670f4ebb206095a58194b; tgc=TGT-NTE0MjQzMTc0NQ==-1443952354-hk-EAF5A7F011845C1043763FB3C58DC89E; SUS=SID-5142431745-1443952354-GZ-yw0gl-5c286e1d5544d30efcb661d7f98b4b4a; SUE=es%3D31ff80c152ecd789ab979ce7e7d07780%26ev%3Dv1%26es2%3D605d32b6033920d10bd530456df529cd%26rs0%3DvEntLMM3muzxD8wo8PTk%252B2JqoSSe01nJ4Pws3ElaNrdZYAB3rt0XkdPshE%252FjEvpYBeEBwj4nO99lfMmXK6047x%252FzuvDGmtgbz84n5kp5U6fyPB5GFGcZPC00UWE1Q4AdWsRfNmD%252BdRmI06LLjdITkJxzeKT%252BhbPDLPStWeK%252BTEI%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1443952354%26et%3D1444038754%26d%3D40c3%26i%3D4b4a%26us%3D1%26vf%3D1%26vt%3D4%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5142431745%26user%3Dhc563blnsg%2540163.com%26ag%3D4%26name%3Dhc563blnsg%2540163.com%26nick%3DMini_R%25E5%25B0%258F%25E7%2596%25AF%25E5%25AD%25906868%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dhc563blnsg%2540163.com%26os%3D%26fmp%3D%26lcp%3D2015-08-21%252014%253A21%253A57; SUB=_2A257FIayDeTxGeNP71AV8y_LzzmIHXVYY_96rDV_PUNbuNBuLXmkkW9naha8kdoqULx9pA_56WHEcKNlmw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYTG863MkPLheimog5d7c_; ALC=ac%3D59%26bt%3D1443952354%26cv%3D5.0%26et%3D1475488354%26uid%3D5142431745%26vf%3D1%26vt%3D4%26es%3D3cda7502049157e1d67ec31830566746; ALF=1475488354; LT=1443952354; sso_info=v02m6alo5qztY2alrmpl7WIpZGTlKWQo4CljoSYpZGTnKWOk5ilkJSYpZGTlKWQlJCljpOAto6DmLiJp5WpmYO0tYyTkLKNg4yxjbOQtQ=='
# 'v8 ' vcjmi41976504@126.com
# ck = 'SINAGLOBAL=23.127.5.35_1438381099.222158; UOR=www.google.com,blog.sina.com.cn,; U_TRS1=00000023.58191642.55bccd5d.3f434700; vjuids=-28335e30f.14ee982b46a.0.7a397cda; SGUID=1438436749265_34644990; lxlrtst=1443666296_o; ArtiFSize=14; lxlrttp=1443792570; Apache=71.233.245.138_1444060264.797192; U_TRS2=0000008a.417f4a43.5612acdf.a2f005e1; rotatecount=1; ULV=1444064489714:25:6:3:71.233.245.138_1444060264.797192:1443977692349; SessionID=17ma3rp8l85lcm38jdcht2sli2; vjlast=1443843509.1444064538.10; tgc=TGT-NTMyNzIyMjI0MQ==-1444064615-hk-4CBBCBCF9852ADCAEE36074A18BA5AE3; SUS=SID-5327222241-1444064615-GZ-06p1o-c8680828e7b5bf34ec19c5ff3c414b4a; SUE=es%3D3eb57f79b2478142c1c163f1f04dd320%26ev%3Dv1%26es2%3D58e03d54fcf56e4b26a0ec869846a600%26rs0%3DoUxbAw2fWw9dVeT0SP7yZSkyFBQ2xG%252B%252FYHIC1jMWqK5lcTTEAJW%252FpUwgDLCtYItNBXlbmlt%252FpbZ0ETvhndzqgvBduu8E7e5gyUOqieHyegZln0ixdC0GrL%252FR2PgG23i5YfVoGTJGmjYacAdqdpNZpe9i1Pu2CVp9UbU8CTm2zvw%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1444064615%26et%3D1444151015%26d%3D40c3%26i%3D4b4a%26us%3D1%26vf%3D1%26vt%3D2%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5327222241%26user%3Dvcjmi41976504%2540126.com%26ag%3D4%26name%3Dvcjmi41976504%2540126.com%26nick%3Dtwwetii793256%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dvcjmi41976504%2540126.com%26os%3D%26fmp%3D%26lcp%3D2015-09-21%252012%253A12%253A26; SUB=_2A257Ft03DeTxGeNN6VUT8izOzz2IHXVYYkn_rDV_PUNbuNBuLVnhkW8y8EtsqeTGpAdC1CuIzl_GkgZhFQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.49SfQ89T4PqZKkwsSCmT; ALC=ac%3D59%26bt%3D1444064615%26cv%3D5.0%26et%3D1475600615%26uid%3D5327222241%26vf%3D1%26vt%3D2%26es%3D5f8496c44c9f9c0b5c3af5fa3d563bdc; ALF=1475600615; LT=1444064615; sso_info=v02m6alo5qztbSdt52lnYalqY2zpLOMo5S2iaeVqZmDtLWMs4i3jKOIsoyjkLE=; cREMloginname=vcjmi41976504%40126.com'
# ck2= 'SINAGLOBAL=23.127.5.35_1438381099.222158; UOR=www.google.com,blog.sina.com.cn,; U_TRS1=00000023.58191642.55bccd5d.3f434700; vjuids=-28335e30f.14ee982b46a.0.7a397cda; SGUID=1438436749265_34644990; lxlrtst=1443666296_o; ArtiFSize=14; lxlrttp=1443792570; Apache=71.233.245.138_1444060264.797192; U_TRS2=0000008a.417f4a43.5612acdf.a2f005e1; rotatecount=1; ULV=1444064489714:25:6:3:71.233.245.138_1444060264.797192:1443977692349; SessionID=17ma3rp8l85lcm38jdcht2sli2; vjlast=1443843509.1444064538.10; tgc=TGT-NTMyNzIyMjI0MQ==-1444064615-hk-4CBBCBCF9852ADCAEE36074A18BA5AE3; SUS=SID-5327222241-1444064615-GZ-06p1o-c8680828e7b5bf34ec19c5ff3c414b4a; SUE=es%3D3eb57f79b2478142c1c163f1f04dd320%26ev%3Dv1%26es2%3D58e03d54fcf56e4b26a0ec869846a600%26rs0%3DoUxbAw2fWw9dVeT0SP7yZSkyFBQ2xG%252B%252FYHIC1jMWqK5lcTTEAJW%252FpUwgDLCtYItNBXlbmlt%252FpbZ0ETvhndzqgvBduu8E7e5gyUOqieHyegZln0ixdC0GrL%252FR2PgG23i5YfVoGTJGmjYacAdqdpNZpe9i1Pu2CVp9UbU8CTm2zvw%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1444064615%26et%3D1444151015%26d%3D40c3%26i%3D4b4a%26us%3D1%26vf%3D1%26vt%3D2%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5327222241%26user%3Dvcjmi41976504%2540126.com%26ag%3D4%26name%3Dvcjmi41976504%2540126.com%26nick%3Dtwwetii793256%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dvcjmi41976504%2540126.com%26os%3D%26fmp%3D%26lcp%3D2015-09-21%252012%253A12%253A26; SUB=_2A257Ft03DeTxGeNN6VUT8izOzz2IHXVYYkn_rDV_PUNbuNBuLVnhkW8y8EtsqeTGpAdC1CuIzl_GkgZhFQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.49SfQ89T4PqZKkwsSCmT; ALC=ac%3D59%26bt%3D1444064615%26cv%3D5.0%26et%3D1475600615%26uid%3D5327222241%26vf%3D1%26vt%3D2%26es%3D5f8496c44c9f9c0b5c3af5fa3d563bdc; ALF=1475600615; LT=1444064615; sso_info=v02m6alo5qztbSdt52lnYalqY2zpLOMo5S2iaeVqZmDtLWMs4i3jKOIsoyjkLE=; cREMloginname=vcjmi41976504%40126.com'
