# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

from httplib import BadStatusLine as BS
import time

from bs4 import BeautifulSoup

from pymongo import errors

from settings import TIMEOUT, FLOW_CONTROL_DAYS, TZCHINA, UTC
from utils import *
from decode import mid_to_token
from geo import geocode
from weibo import get_response_as_human


def parse_keyword(db, keyword, browser):
    url = 'http://s.weibo.com/weibo/' + keyword  # + '&nodup=1'
    rd = get_response_as_human(browser, url)
    soup = BeautifulSoup(rd, 'html5lib')

    # Test
    # f = open("../data/parse_keyword_" + toPinyin(keyword) + ".html", "w")
    # f.write(rd)
    # f.close()

    # Page number
    try:
        pages = len((soup.find('div', {'node-type': 'feed_list_page_morelist'})).findAll('li'))
    except AttributeError:
        print "no related posts have been found."
        return 0

    print "%s: %d pages in total" % (keyword.decode("utf-8"), pages)

    stop_flag = False
    for i in range(pages):
        url = 'http://s.weibo.com/weibo/' + keyword + '&page=' + str(i + 1)  # + '&nodup=1'
        print url.decode("utf-8")
        rd = get_response_as_human(browser, url)
        soup = BeautifulSoup(rd, 'html5lib')
        posts = soup.findAll('div', {'action-type': 'feed_list_item'})

        # Test
        # f = open("../data/parse_keyword_posts" + toPinyin(keyword) + ".html", "w")
        # f.write(rd)
        # f.close()

        start = datetime.datetime.now()

        print "%d posts in Page %d" % (len(posts), pages)
        for post in posts:
            json_data = parse_post(post, keyword)
            try:
                db.users.insert_one(json_data['user'])
            except errors.DuplicateKeyError, e:
                print "Duplicated user. " + e.message

            try:
                db.posts.insert_one(json_data['post'])
            except KeyError, e:
                print "BeautifulSoup does not working properly. " + e.message
            except errors.DuplicateKeyError:
                print "===================UPDATING==================="
                # update
                # timestamp of a post
                # 2015-10-07 00:26:00+08:06
                timestamp = json_data['post']['timestamp']
                now = datetime.datetime.now(TZCHINA)
                delta = now - timestamp
                # (1) i = 0, the first page might have selected posts (精选),
                #            the reposts might update very often.
                # (2) delta.days < 3 flow control. Keep the program manageable,
                #            if not, too many queries if run the program for a while.
                if i == 0 or delta.days < FLOW_CONTROL_DAYS:
                    db.posts.update({'mid': json_data['post']['mid']},
                                    {'$set': {'fwd_count': json_data['post']['fwd_count'],
                                              'cmd_count': json_data['post']['cmt_count'],
                                              'like_count': json_data['post']['like_count'],
                                              }
                                     })
                else:
                    stop_flag = True
                    break
        if stop_flag:
            ######################################################################
            # important here, for others, I need to design a collecting mechanism.
            update_keyword(keyword, now)
            ######################################################################
            print "Unneccessary to collect historical data."
            break
            # print "The keyword %s has been parsed." % keyword.decode('utf-8')
        print 'Time for processing page %d: %d sec(s).' % (i + 1, int((datetime.datetime.now() - start).seconds))


def update_keyword(keyword, now):
    print keyword, now


def parse_item(post, keyword):
    userid, user_name, fwd_count, like_count, content = 0, '', 0, 0, ''
    # unique vavlue
    mid = int(post.attrs['mid'])

    # userid, username
    try:
        face_icon = post.find('div', class_="WB_face W_fl")
        userid = int(face_icon.find("a").attrs['usercard'][3:])
        user_name = face_icon.find("img").attrs['alt']
    except AttributeError, e:
        print e.message

    # verification
    if post.find('i', class_='W_icon icon_approve') is not None:
        user_verified = True
    else:
        user_verified = False

    # content
    post_content = post.find('div', class_='list_con')
    try:
        content = post_content.find('span', {'node-type': 'text'}).get_text()
    except AttributeError, e:
        print e.message

    # counts：cmt_count does not exist
    try:
        ul = post_content.find('ul', class_='clearfix')
        for li in ul.findAll('li'):
            txt = li.get_text().lstrip().rstrip()
            if "转发" in txt:
                fwd_count = int("0" + txt.replace("转发", "").lstrip().rstrip())
        # the last one is the like count.
        like_count = int("0" + ul.findAll("li")[-1].get_text().lstrip().rstrip())
    except AttributeError:
        print e.message


    # timestamp
    # t = '2015-10-05 08:51'   timestamp from weibo example
    t = post_content.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']
    t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=TZCHINA)

    # location: no location information for the reposts.

    # return resultin json.
    result_json = {
        "reply": {
            "keyword": keyword,
            "mid": mid,
            "content": content.encode('utf-8', 'ignore'),
            "timestamp": t_china,
            "fwd_count": fwd_count,
            "cmt_count": 0,
            "like_count": like_count,
            "sentiment": 0,
            "user": {
                "userid": userid,
                "username": user_name.encode('utf-8', 'ignore'),
                "user_verified": user_verified,
                "location": "",
                "follower_count": 0,
                "friend_count": 0,
                "verified_info": "",
                "path": []
            },
            "comments": [],
            "replies": []
        },
        "user": {
            "userid": userid,
            "username": user_name.encode('utf-8', 'ignore'),
            "verified": user_verified,
            "verified_info": '',
            "gender": "",
            "birthday": 1900,
            "follower_count": 0,
            "friend_count": 0,
            "path": []
        }
    }

    try:
        print t, user_name, user_verified, fwd_count, content
    except UnicodeEncodeError, e:
        print e.message

    return result_json


def parse_post(post, keyword):
    userid, fwd_count, cmt_count, like_count, user_name = 0, 0, 0, 0, ''
    # primary key mid
    mid = int(post.attrs['mid'])

    # user_name, userid
    try:
        if post.find('img', class_='W_texta W_fb') is not None:
            user_name = post.find('img', class_='W_texta W_fb').attrs['title']
        else:
            user_name = post.find("img", class_="W_face_radius").attrs['alt']

        if "usercard" in post.find('a', class_='W_texta W_fb').attrs.keys():
            userid_tmp = post.find('a', class_='W_texta W_fb').attrs['usercard']
            userid = int(userid_tmp[3:userid_tmp.index("&")])
        elif "usercard" in post.find('img', class_='W_face_radius').attrs.keys():
            userid_tmp = post.find('img', class_='W_face_radius').attrs['usercard']
            userid = int(userid_tmp[3:userid_tmp.index("&")])
        else:
            userid_tmp = post.find('img', class_='W_face_radius').attrs['wbcrawler']
            userid = int(userid_tmp.split("/")[3])
    except KeyError, e:
        print e.message

    # user verification
    if post.find('a', class_='approve') is None:
        user_verified = False
    else:
        user_verified = True

    # the content of a weibo (tweet)
    content = post.find('p', class_='comment_txt').get_text()

    # counts: relies, cmts, likes
    if post.find('a', {'action-type': 'feed_list_forward'}) is not None:
        fwd_count = int(post.find('a', {'action-type': 'feed_list_forward'}).get_text().replace("转发", "0"))
        cmt_count = int(post.find('a', {'action-type': 'feed_list_comment'}).get_text().replace("评论", "0"))
        like_count = int("0" + post.find('a', {'action-type': 'feed_list_like'}).get_text())
    else:
        lis_panel = post.find("ul", class_="feed_action_info feed_action_row4")
        lis = lis_panel.findAll("li")
        for li in lis:
            if "转发" in li.get_text():
                fwd_count = int("0" + li.get_text().replace("转发", ""))
            if "评论" in li.get_text():
                cmt_count = int("0" + li.get_text().replace("评论", ""))
            like_count = int("0" + lis[len(lis) - 1].get_text())

    # location
    loc, latlng = '', [0, 0]
    if post.find('span', class_='W_btn_tag') is not None:
        if post.find('span', class_='W_btn_tag').attrs.has_key('title'):
            loc = post.find('span', class_='W_btn_tag').attrs['title']
            latlng = geocode(loc)

    # timestamp
    # t = '2015-10-05 08:51'
    try:
        if len(post.findAll('a', {'node-type': 'feed_list_item_date'})) == 2:
            t = post.findAll('a', {'node-type': 'feed_list_item_date'})[1].attrs['title']
        else:
            t = post.find('a', {'node-type': 'feed_list_item_date'}).attrs['title']
        t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=TZCHINA)
    except ValueError:
        t = str(datetime.datetime.now(TZCHINA))
        t_china = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=TZCHINA)

    # build the return result in json
    result_json = {
        "post": {
            "mid": mid,
            "keyword": keyword,
            "content": content.encode('utf-8', 'ignore'),
            "timestamp": t_china,
            "fwd_count": fwd_count,
            "cmt_count": cmt_count,
            "like_count": like_count,
            "location": loc,
            "latlng": latlng,
            "sentiment": 0,
            "user": {
                "userid": userid,
                "username": user_name.encode('utf-8', 'ignore'),
            },
            "comments": [],
            "replies": []
        },
        "user": {
            "userid": userid,
            "username": user_name.encode('utf-8', 'ignore'),
            "verified": user_verified,
            "verified_info": '',
            "gender": "",
            "birthday": 1900,
            "location": loc,
            "latlng": latlng,
            "follower_count": 0,
            "friend_count": 0,
            "path": []
        }
    }

    try:
        print user_name.decode('utf-8', 'ignore'), " ", t_china, " ", fwd_count, cmt_count, like_count, " ", content
    except UnicodeEncodeError, e:
        print e.message
    return result_json


def deleted(mid, db):
    print "this post has been deleted."
    t_china = datetime.datetime.now(TZCHINA)
    db.posts.update(
        {'mid': mid},
        {'$set': {
            'deleted_time': t_china
        }
        })
    return 0


def parse_repost(db, browser, posts):
    # flow control
    # As for now, only calculate the reposts with a fwd count larger than 10
    # 时间上也要做flow control？需要吗？
    count = posts.count()
    cur = 0
    print "total posts: %d" % count
    # Error pymongo.errors.CursorNotFound:
    for post in posts:
        print "%d posts remain." % (count - cur)
        cur += 1
        if 'deleted_time' in post.keys():
            "the post in process has been deleted. directly jump to the next repost."
            continue
        # token url exmple: http://weibo.com/3693685493/CEtFjkHwM?type=repost
        token = mid_to_token(post['mid'])
        # 1. Determine the URL
        url = "http://weibo.com/%s/%s?type=repost" % (str(post['user']['userid']), token)
        print url

        # 2. Parsing the data
        # 2.0 this post has been deleted.
        rd = get_response_as_human(browser, url)
        # http://weibo.com/sorry?pagenotfound or the user's home page
        # http://weibo.com/u/2953377041/home?wvr=5
        if "home" in browser.current_url or "sorry?pagenotfound" in browser.current_url or "weibo.com/login.php" in browser.current_url:
            deleted(post['mid'], db)
            continue
        # test
        # f = open("../data/parse_repost_%s.html" % post['mid'], "w")
        # f.write(str(rd))
        # f.close()

        repost_panel = BeautifulSoup(rd, 'html5lib').find("div", class_="WB_feed WB_feed_profile")
        if repost_panel == None:
            deleted(post['mid'], db)
            continue

        # 2.1 the counts
        # counts
        if repost_panel.find("div", class_="WB_feed_handle") == None:
            deleted(post['mid'], db)
            continue

        for li in repost_panel.find("div", class_="WB_feed_handle").findAll("li"):
            txt = li.get_text().lstrip().rstrip()
            if "转发" in txt:
                fwd_count = int("0" + txt.replace("转发", "").lstrip().rstrip())
            if "评论" in txt:
                cmt_count = int("0" + txt.replace("评论", "").lstrip().rstrip())
        # the last one is the like count.
        like_txt = repost_panel.find("div", class_="WB_handle").findAll("li")[-1].get_text().lstrip().rstrip()
        like_count = int("0" + like_txt)

        # update counts when any count number changes
        if cmt_count != post['cmt_count'] or fwd_count != post['fwd_count'] or like_count != post['like_count']:
            db.posts.update({'mid': post['mid']}, {'$set': {
                'fwd_count': fwd_count,
                'cmt_count': cmt_count,
                'like_count': like_count
            }})

        # 2.2  harvest and flow size control
        # num_replies = 0

        if repost_panel.find('div', class_="WB_empty") == None:
            continue

        stop = False
        page_list = repost_panel.findAll("a", class_="page")

        if len(page_list) == 0:
            pages = 1
            stop = True
        elif '下一页' in page_list[-1].get_text():
            pages = int(page_list[-2].get_text())
        else:
            pages = 1
            stop = True

        for i in range(pages):
            # all the replies in the database.
            mids = [reply['mid'] for reply in db.posts.find_one({'mid': post['mid']})['replies']]
            # num_replies = len(mid)
            reposts = repost_panel.findAll("div", {'action-type': 'feed_list_item'})[1:]
            flag = repost_panel.findAll("div", {'action-type': 'feed_list_item'})[-1].attrs['mid']
            for item in reposts:
                item_json = parse_item(item, post['keyword'])

                # the time interval between the repost and the original post
                # the first repost page might have selected replies.

                # stop harvesting based on time
                t = str(datetime.datetime.now(UTC))
                t_utc_now = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), 0, 0, tzinfo=UTC)
                delta = (t_utc_now - item_json['reply']['timestamp']).days
                if delta > FLOW_CONTROL_DAYS and i != 0:
                    stop = True
                    break

                if item_json['reply']['mid'] not in mids:  # and delta < FLOW_CONTROL_DAYS:

                    # insert a user
                    try:
                        db.users.insert_one(item_json['user'])
                    except errors.DuplicateKeyError, e:
                        print "Duplicated User." + e.message

                    # insert a reply. In the end, delete the duplicated ones.
                    db.posts.update(
                        {'mid': post['mid']},
                        {'$push': {'replies': item_json['reply']
                                   }
                         })

                    # insert the reply as a new post
                    try:
                        db.posts.insert_one(item_json['reply'])
                    except errors.DuplicateKeyError, e:
                        print "Duplicated post." + e.message

            if stop:
                break
            else:
                print "===============Page %d has been processed.===============" % (i + 1)
                if i != pages - 1:
                    # browser.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]/span').click()
                    # WebDriverWait(browser, TIMEOUT).until(EC.staleness_of(browser.find_element_by_class_name('list_ul')))
                    # repost_panel = BeautifulSoup(browser.page_source, 'html5lib').find("div", class_="WB_feed WB_feed_profile")
                    while True:
                        if 'undefined' in repost_panel.find('div', class_="list_ul"):
                            stop = True
                            break
                        if repost_panel.find("a", class_="page next S_txt1 S_line1") == None:
                            break

                        browser.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]/span').click()
                        time.sleep(get_interval_as_human())

                        try:
                            repost_panel = BeautifulSoup(browser.page_source, 'html5lib').find("div", class_="WB_feed WB_feed_profile")
                        except BS, e:
                            log(ERROR, e.message)
                            break
                        if flag != repost_panel.findAll("div", {'action-type': 'feed_list_item'})[-1].attrs['mid']:
                            break
        print "the reposts of this post have been successfully processed."


def parse_info(db, browser, users):
    # STEP ONE：already got the latlng from the content
    # users = db.users.find({'latlng': [0, 0]}, no_cursor_timeout=True).limit(100)
    count = users.count()
    cur = 0
    log(NOTICE, "total users: %d" % count)
    for user in users:
        log(NOTICE, "%d users remain." % (count - cur))
        cur += 1
        start = datetime.datetime.now()
        if 'location' in user.keys():
            if user['location'] == '其他' or user['location'] == '未知':
                continue
        url = "http://weibo.cn/%s/info" % user['userid']
        rd = get_response_as_human(browser, url, 20)
        gender, birthday, verified, verified_info, loc, latlng = '', 1900, False, '', '', [0, 0]

        # test
        # f = open("../data/parse_profile_%s.html" % user['userid'], "w")
        # f.write(str(rd))
        # f.close()

        tabs = BeautifulSoup(rd, 'html5lib').findAll("div", class_="c")
        for tab in tabs:
            try:
                info = tab.get_text()
            except AttributeError:
                continue

            if '昵称' in info:
                info = info.replace('认证信息：', '认信:').replace('感情状况：', '感情:').replace('性取向：', '取向:')
                flds = info.split(":")
                i = 0
                while i < len(flds) - 1:
                    if '性别' in flds[i]:
                        if '男' in flds[i + 1]:
                            gender = 'M'
                        else:
                            gender = 'F'
                            # print gender
                    if '地区' in flds[i]:
                        loc = flds[i + 1][:-2]
                        loc = loc.replace("海外 ", "")
                    if '认信' in flds[i]:
                        verified = True
                        verified_info = flds[i + 1][:-2]
                        verified_info = verified_info.replace('官方微博', '')
                        # print verified_info
                    if '生日' in flds[i]:
                        birthday = flds[i + 1][:-2]
                        # print birthday
                    i += 1

                # location could be the very last one
                if '地区' in flds[len(flds) - 2]:
                    loc = flds[len(flds) - 1]
                # the value of 地区 could be 未知, 其他.
                if '地区' not in info:
                    loc = "未知"
                elif loc == "其他":
                    pass
                else:
                    latlng = geocode(loc)
                break

        db.users.update({'userid': user['userid']}, {'$set': {
            'gender': gender,
            'birthday': birthday,
            'location': loc,
            'verified': verified,
            'verified_info': verified_info,
            'latlng': latlng
        }})

        # print unicode(gender), birthday, verified_info, loc, latlng[0], latlng[1]
        try:
            print user['username'], loc, latlng[0], latlng[1]
        except UnicodeEncodeError, e:
            print "Error: " + e.message
        finally:
            print "Time: %d sec(s)." % int((datetime.datetime.now() - start).seconds)


def parse_path(db, browser, users):
    # STEP ONE：already got the latlng from the content
    # modify the default timeout. Usually, the func parse_path takes longer than other funcs.
    browser.set_page_load_timeout(4 * TIMEOUT)
    count = users.count()
    cur = 0
    log(NOTICE, "total users: %d" % count)
    for user in users:
        log(NOTICE, "%d users remain." % (count - cur))
        cur += 1
        start = datetime.datetime.now()
        # url example: http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=1644114654&starttime=2013-01-01&endtime=2013-12-31
        url = "http://place.weibo.com/index.php?_p=ajax&_a=userfeed&uid=%s&starttime=2014-01-01" % user['userid']
        log(NOTICE, "parsing the routes from %s." % user['username'])
        rd = get_response_as_human(browser, url, page_reload=False)

        if rd == "":
            db.users.update({'userid': user['userid']}, {'$set': {'path': [0, 0, datetime.datetime.now(TZCHINA)]}})
            browser.set_page_load_timeout(TIMEOUT)
            continue
        path = []
        if "noUserFeed" not in rd:
            # STEP TWO: Assigning location the path url
            posts = BeautifulSoup(rd, 'html5lib').findAll("div", class_="time_feed_box")

            for post in posts:
                # '2013-12-6 18:14'
                t = post.find("a", class_="date").get_text().lstrip()
                if "-" in t:
                    t1 = t.split("-")
                    t2 = t1[2].split(" ")
                    t3 = t2[1].split(":")
                    t_china = datetime.datetime(int(t1[0]), int(t1[1]), int(t2[0]), int(t3[0]), int(t3[1]), 0, 0,
                                                tzinfo=TZCHINA)
                elif "月" in t:
                    # t1 = t.split("æœˆ")[0]
                    # t2 = t.split("æœˆ")[1].split("æ—¥")[0]
                    t1 = t.split("月")[0]
                    t2 = t.split("月")[1].split("日")[0]
                    t3 = t.split(" ")[1].split(":")
                    t_china = datetime.datetime(2015, int(t1), int(t2), int(t3[0]), int(t3[1]), 0, 0, tzinfo=TZCHINA)
                else:
                    t_china = datetime.datetime.now(TZCHINA)

                # path
                if post.find("div", class_="time_map_pao2") is not None:
                    ll = post.find("div", class_="time_map_pao2")
                    # if ll.find("a", {'target': '_blank'}).attrs['href'] is not None:
                    tmp = ll.find("a", {'target': '_blank'}).attrs['href']
                    tmp = tmp.split('/')[2]
                    tmp = tmp.split(",")
                    lng = tmp[1]
                    lat = tmp[0]
                elif post.find("div", class_="time_mapsite") is not None:
                    ll = post.find("div", class_="time_mapsite")
                    tmp = ll.find("img", class_="bigcursor").attrs["onclick"]
                    tmp = tmp.split(",")
                    lat = tmp[1]
                    lng = tmp[0].split("(")[1]
                elif post.find("div", class_="time_mapsite2") is not None:
                    ll = post.find("div", class_="time_mapsite2")
                    tmp = ll.find("img", class_="bigcursor").attrs["onclick"]
                    tmp = tmp.split(",")
                    lat = tmp[1]
                    lng = tmp[0].split("(")[1]
                else:
                    lat = 0
                    lng = 0

                if lat == '':
                    lat = 0
                    lng = 0
                print user['username'], lat, lng, t_china
                path.append([float(lat), float(lng), t_china])
        else:
            path.append([0, 0, 0])

        # update user path and latlng
        db.users.update({'userid': user['userid']}, {'$set': {'path': path}})
        # 更新user 的latlng,
        # 对于post的latlng的更新，我认为可以不着急？
        try:
            latlng = [path[0][0], path[0][1]]  # 临时策略
        except IndexError:
            latlng = [0, 0]
        finally:
            db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})
            print "Time: %d sec(s)." % int((datetime.datetime.now() - start).seconds)
    # change to the original timeout
    browser.set_page_load_timeout(TIMEOUT)