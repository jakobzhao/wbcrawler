#*-* coding:utf-8 *-*
import cookielib

import mechanize

br = mechanize.Browser()

#cookie jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
#加上各种协议
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#加上自己浏览器头部，和登陆了通行证的cookie
# hc563blnsg@163.com
ck = 'SINAGLOBAL=23.127.5.35_1438381099.222158; UOR=www.google.com,blog.sina.com.cn,; U_TRS1=00000023.58191642.55bccd5d.3f434700; vjuids=-28335e30f.14ee982b46a.0.7a397cda; SGUID=1438436749265_34644990; lxlrtst=1443666296_o; vjlast=1443843509; ArtiFSize=14; lxlrttp=1443792570; Apache=71.233.245.138_1443914418.595857; ULV=1443937801395:23:4:1:71.233.245.138_1443914418.595857:1443843507572; U_TRS2=0000008a.a4996c2f.5610bec3.0dd368b8; ULOGIN_IMG=hk-de60d3a40d3c439670f4ebb206095a58194b; tgc=TGT-NTE0MjQzMTc0NQ==-1443952354-hk-EAF5A7F011845C1043763FB3C58DC89E; SUS=SID-5142431745-1443952354-GZ-yw0gl-5c286e1d5544d30efcb661d7f98b4b4a; SUE=es%3D31ff80c152ecd789ab979ce7e7d07780%26ev%3Dv1%26es2%3D605d32b6033920d10bd530456df529cd%26rs0%3DvEntLMM3muzxD8wo8PTk%252B2JqoSSe01nJ4Pws3ElaNrdZYAB3rt0XkdPshE%252FjEvpYBeEBwj4nO99lfMmXK6047x%252FzuvDGmtgbz84n5kp5U6fyPB5GFGcZPC00UWE1Q4AdWsRfNmD%252BdRmI06LLjdITkJxzeKT%252BhbPDLPStWeK%252BTEI%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1443952354%26et%3D1444038754%26d%3D40c3%26i%3D4b4a%26us%3D1%26vf%3D1%26vt%3D4%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5142431745%26user%3Dhc563blnsg%2540163.com%26ag%3D4%26name%3Dhc563blnsg%2540163.com%26nick%3DMini_R%25E5%25B0%258F%25E7%2596%25AF%25E5%25AD%25906868%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dhc563blnsg%2540163.com%26os%3D%26fmp%3D%26lcp%3D2015-08-21%252014%253A21%253A57; SUB=_2A257FIayDeTxGeNP71AV8y_LzzmIHXVYY_96rDV_PUNbuNBuLXmkkW9naha8kdoqULx9pA_56WHEcKNlmw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYTG863MkPLheimog5d7c_; ALC=ac%3D59%26bt%3D1443952354%26cv%3D5.0%26et%3D1475488354%26uid%3D5142431745%26vf%3D1%26vt%3D4%26es%3D3cda7502049157e1d67ec31830566746; ALF=1475488354; LT=1443952354; sso_info=v02m6alo5qztY2alrmpl7WIpZGTlKWQo4CljoSYpZGTnKWOk5ilkJSYpZGTlKWQlJCljpOAto6DmLiJp5WpmYO0tYyTkLKNg4yxjbOQtQ=='
#'v8 ' vcjmi41976504@126.com
#ck = 'SINAGLOBAL=23.127.5.35_1438381099.222158; UOR=www.google.com,blog.sina.com.cn,; U_TRS1=00000023.58191642.55bccd5d.3f434700; vjuids=-28335e30f.14ee982b46a.0.7a397cda; SGUID=1438436749265_34644990; lxlrtst=1443666296_o; vjlast=1443843509; ArtiFSize=14; lxlrttp=1443792570; Apache=71.233.245.138_1443973993.75309; U_TRS2=0000008a.9220435b.561159d4.b891503c; ULV=1443977692349:24:5:2:71.233.245.138_1443973993.75309:1443937801395; cREMloginname=jakobzhao%40gmail.com; ULOGIN_IMG=hk-e3ba998849f593c2dec00b17b83c843939ac; tgc=TGT-NTMyNzIyMjI0MQ==-1443977917-hk-B7095F8DF24C91B364DFD44E4BC6742C; SUS=SID-5327222241-1443977917-GZ-4nmq7-ae7d665b4c418c843103ae2105454b4a; SUE=es%3Da805b635d3de38fab70a63c4d70bfbde%26ev%3Dv1%26es2%3Da9d8433f78f048c65039a70952f11ddc%26rs0%3D7SSobvTSWHGSJ81XyqblgMQjTh3%252F2I4YbNiDnFJaponzQebkJeVhHWQLH%252BwMvBsPGfP3VIN0%252FaEVb17Q8ouNxYcDZY9T1VEvXDqRgzdRGZJJLjKfptws3a6Q89rVQMyvgQq4GbfzYDJwSzvwHn01tbedg2%252B82hFYI55C32YIAG4%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1443977917%26et%3D1444064317%26d%3D40c3%26i%3D4b4a%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D59%26st%3D0%26lt%3D1%26uid%3D5327222241%26user%3Dvcjmi41976504%2540126.com%26ag%3D4%26name%3Dvcjmi41976504%2540126.com%26nick%3Dtwwetii793256%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3Dvcjmi41976504%2540126.com%26os%3D%26fmp%3D%26lcp%3D2015-09-21%252012%253A12%253A26; SUB=_2A257FSrtDeTxGeNN6VUT8izOzz2IHXVYYxslrDV_PUNbuNBuLUv-kW90DH6S0nu_TzZzcQArXHvlqhNsYQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.49SfQ89T4PqZKkwsSCmT; ALC=ac%3D59%26bt%3D1443977917%26cv%3D5.0%26et%3D1475513917%26uid%3D5327222241%26vf%3D0%26vt%3D0%26es%3Dd9a6acf0647c9a179854164feea48e51; ALF=1475513917; LT=1443977917; sso_info=v02m6alo5qztbSdt52lnYalqY2zpLOMo5S2iaeVqZmDtLWMs4i3jKOIsoyjkLE='
br.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'),('Cookie',ck) ]

# for f in br.forms():
#     print f
# br.select_form(nr=0)
# print br
# br.form['username']='13580491531'
# br.form['password']='buhui1314iliting'
# br.submit()
# br.add_password('http://login.sina.com.cn/signup/signin.php?entry=sso','13580491531','buhui1314iliting')
#登陆新浪通行证
br.open('http://login.sina.com.cn/signup/signin.php?entry=sso')

t = br.response().read()
f = open("ht.html","w")
f.write(t)
f.close()


#keyword
query = "地方政府"
br.open('http://s.weibo.com/weibo/'+query)
print br.response().geturl().decode('utf-8')
t = br.response().read()
f = open("html4.html","w")
f.write(t)
f.close()
print "complete"