# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''



import urllib2,urllib
import json
import sqlite3, time
import sys, os

import ssl, socket

from shutil import copy

import mechanize
import cookielib

from settings import *


query_header_statuses  = 'INSERT INTO statuses  (id, status_type, text, created_at, source, geo, thumbnail_pic, user_id, user_screen_name, reposts_count, comments_count) VALUES ( '
query_header_comments  = 'INSERT INTO statuses  (id, status_type, text, created_at, source, user_id, user_screen_name) VALUES ( '
query_header_users     = 'INSERT INTO users     (id, screen_name, province, city, location, description, url, profile_image_url, profile_url, domain, weihao, gender, created_at, geo_enabled, verified, avatar_large, verified_reason, lang, bi_followers_count, followers_count, friends_count, statuses_count, favourites_count) VALUES ( '
query_header_retweets  = 'INSERT INTO retweets  (id, retweet_type, from_status_id, from_status_user_id, from_status_user_screen_name, to_status_id, to_status_user_id,to_status_user_screen_name, created_at) VALUES ( '



reload(sys)
sys.setdefaultencoding('utf-8')
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]


def weibo_login():

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
    return(br)

def parse_keyword(keyword, browser):
    browser.open('http://s.weibo.com/weibo/'+keyword)

    print browser.response().geturl().decode('utf-8')
    t = browser.response().read()
    f = open("html2.html","w")
    f.write(t)
    f.close()
    print "complete"


def createDB(database, refresh):
    current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    if os.path.exists(database):
        if refresh:
            copy(current_path + '/' + 'weibo_crawler_template.db', database)
    else: 
        copy(current_path + '/' + 'weibo_crawler_template.db', database)

def sendEmail(reciever, msg, attached_filename):
    import smtplib
    sender = 'snsgis@gmail.com'
    username = 'snsgis@gmail.com'
    password = email_password
    msg = '''From: Crawler Server <snsgis@gmail.com>
To: Administrator <''' + reciever + '''>
Subject: Warning from Crawler Server
MIME-Version: 1.0

To whom it concerns,

''' + msg + '''
--
sent from crawler server
notice: Please don't reply to this email, nobody would notice your email. However, don't hesitate to 
contact the administrator Bo Zhao <jakobzhao@gmail.com> at your convenience.
'''
    # The actual mail send
    try:
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com','587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(sender, reciever, msg)
        server.quit()
    except socket.gaierror, e:
        print str(e) + "/n error raises when sending E-mails."

def uploadToDropbox(inputfile, outputfile):
    # Include the Dropbox SDK libraries
    import dropbox as dbox
    # Get your app key and secret from the Dropbox developer website
    APP_KEY = 'rw5taat0dfl2ryf'
    APP_SECRET = 'pxfb5itmmy7quyi'
    
    # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
    ACCESS_TYPE = 'app_folder'
    TOKENS = 'dropbox_token.ini'
    token_file = open(current_path + '/' + TOKENS)
    token_key,token_secret = token_file.read().split('|')
    token_file.close()
    
    sess = dbox.session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE )
    sess.set_token(token_key,token_secret)
    client = dbox.client.DropboxClient(sess)
    
    print "linked account:", client.account_info()
    f = open(inputfile,'rb')
    response = client.put_file(outputfile, f, True ) #put_file(full_path, file_obj, overwrite=False, parent_rev=None)    
    print response
    


def getResponseObject(url):
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    request = urllib2.Request(url = url,headers = headers)
    content = "{}"
    msg = 'Something wrong with this crawler server.'
    #print url
    #time.sleep(1)
    try:
        response = urllib2.urlopen(request, timeout = 5)
        content = response.read()
    except urllib2.URLError, e:
        msg = msg + '\n' + url + '\n' + str(e)
        if str(e) == 'HTTP Error 403: Forbidden':
            #over the limits
            #sendEmail('jakobzhao@gmail.com', msg, '')
            print "this service has been shut down."
            sys.exit(0)
        if str(e) == 'HTTP Error 400: Bad Request':
            sendEmail('jakobzhao@gmail.com', msg, '')
            print "this service has been shut down."
            sys.exit(0)
    except ssl.SSLError,e:
        msg = msg + '\n' + url + '\n' + str(e)
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
    if 'error' in json.loads(content):
        msg = msg + json.loads(content)['error'] + '\n' + url
        print msg
        #sendEmail('jakobzhao@gmail.com', msg, '')
        sys.exit(0)
    try:
        obj = json.loads(content)
    except ValueError, e:
        print "********************************************"
        print "the content of the response is:" + content
        obj = json.loads('{}')
        print  "json loading value error!", e.args[0]
    return obj

def geocoding(database):
    from pygeocoder import Geocoder
    #Variables    
    
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    cursor.execute('select id, location, lat, lng from users')
    user_locs = cursor.fetchall()
    
    conn2 = sqlite3.connect(current_path + '/' + 'gazetteers.db')
    cursor2 = conn2.cursor()
    cursor2.execute('select id, location, lat, lng from gazetteers')
    gazetteers = cursor2.fetchall()
    
    a = {}
    for gazetteer in gazetteers:
        a[gazetteer[1]] = (gazetteer[0],gazetteer[2],gazetteer[3])
    i = 0
    p = 0
    while i < len(user_locs):
        if user_locs[i][2] == None:
            if user_locs[i][1] in a.keys():
                cursor.execute('update users set lat = '+ str(a[user_locs[i][1]][1]) +', lng = ' + str(a[user_locs[i][1]][2]) + ' where id == ' + str(user_locs[i][0]))
                user_locs[i] = (user_locs[i][0],user_locs[i][1], a[user_locs[i][1]][1], a[user_locs[i][1]][2])
            else:
                s = user_locs[i][1].replace('其他', '').replace('海外','')
                coordinates = Geocoder.geocode(s)  
                time.sleep(1)
                cursor.execute('update users set lat = '+ str(coordinates.coordinates[0]) +', lng = ' + str(coordinates.coordinates[1]) + ' where id == ' + str(user_locs[i][0]))
                user_locs[i] = (user_locs[i][0],user_locs[i][1],coordinates.coordinates[0],coordinates.coordinates[1])
                p = p + 1
                try:
                    cursor2.execute('insert into gazetteers (location, lat, lng) values( "' + user_locs[i][1] + '", ' + str(coordinates.coordinates[0]) + ',' + str(coordinates.coordinates[1])  + ')')
                except sqlite3.Error, e:
                    print  "This gazetteer has been inserted.", e.args[0]
            print "i = " + str(i) + ", p = " + str(p)
            j = 0
            while j< len(user_locs):
                if user_locs[j][2] == None:
                    if user_locs[j][1] == user_locs[i][1]:
                        user_locs[j] = (user_locs[j][0],user_locs[j][1], user_locs[i][2], user_locs[i][3])
                        cursor.execute('update users set lat = '+ str(user_locs[i][2]) +', lng = ' + str(user_locs[i][3]) + ' where id == ' + str(user_locs[j][0]))
                        #print 'update users set lat = '+ str(user_locs[i][2]) +', lng = ' + str(user_locs[i][3]) + ' where id == ' + str(user_locs[j][0])
                j = j + 1
        i = i + 1
    conn2.commit()
    conn2.close()
    conn.commit()
    conn.close()
    print "Successfully geocode the tabels!"
    return True

def getOpinionLeadersByDelphi(score_threshold,database):
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    #                       0              1            2            3
    cursor.execute('select id, followers_count, friends_count, verified from users')
    users = cursor.fetchall()
    opinion_leaders = []

    import math
    for user in users:
        score = 0
        if user[3] == 'True':
            score = 3
        else:
            score = 0
        #==========================Calculating the Score============================
        score = round(score + math.log10(float(user[1])/float(user[2]+1)), 2)
        #===========================================================================
        #print score
        if score >= score_threshold:
            opinion_leaders.append({'id': user[0],'score':score})
    
    print 'The list of opinon leaders: ' + str(opinion_leaders)
    #print opinion_leaders[0]['id']
    conn.commit()
    conn.close()            
    return opinion_leaders

def getOpinionLeadersByCentrality(num, database):
    import networkx as nx
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    cursor.execute('select id, source, target from user_edges')
    edges = cursor.fetchall()
    cursor.execute('select id, node from user_nodes')
    nodes = cursor.fetchall()
    conn.commit()
    conn.close()

    G = nx.DiGraph()
    for node in nodes: 
        G.add_node(node[0])
    for edge in edges: 
        G.add_edge(edge[1],edge[2]) 
    
    centrality = nx.degree_centrality(G)
    sorted_centrality = sorted(centrality.items(), key=lambda centrality:centrality[1])[-1*num:]
    return sorted_centrality

#page will start from 1
def searchTermsFromUser(uid, terms, database, page):
    #heuristic searching
    #if topic ="", then it means to search all the statuses of this weibo.
    obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=1&uid=' + str(uid) + '&page=1&access_token=' + TOKEN)
    total_number = obj['total_number']
    while total_number >= COUNT2 * page:
        print "----------------------------Page" + str(page) + " starts----------------------------"
        obj = getResponseObject('https://api.weibo.com/2/statuses/user_timeline.json?source=2933540621&count=' + str(COUNT2)  + '&uid=' + str(uid) + '&page=' + str(page) +'&access_token=' + TOKEN)
        if obj == {}:
            continue
        for status in obj['statuses']:
            #if this status is related to the topic, then get it in.
            flag = False
            for term in terms:
                flag = flag or (term in status['text'])
            if flag and ('deleted' not in status.keys()):
                print status['text']
                processStatus(database, status)

        page = page + 1
        if page * COUNT2 > obj['total_number']:
            completed = 1
        else:
            completed = page * COUNT2/float(obj['total_number'])
        print "----------------------------Page" + str(page-1) + " ends.----------------------------"
        print "----------------------Retrieving Statuses:" +  str(round(completed*100,2)) + "%----------------------"
    print "Totally Finished!"

def processStatus(database, status):
    conn = sqlite3.connect(database)#to name it with a specific word
    cursor = conn.cursor()
    keys = status.keys()

    if 'thumbnail_pic' not in keys:
        status['thumbnail_pic'] = 'None'
    if str(status['geo']) == '':
        status['geo'] = 'None'
    if str(status['geo']) != 'None':
        status['geo'] = str(status['geo']['coordinates'][0]) + "," + str(status['geo']['coordinates'][1])

    ############################statuses################################
    query_body_statuses = str(status['id']) + ", 0, '" + status['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(status['created_at']) + "')" + ", '" + status['source'] + "', '" + str(status['geo']) +  "', '" + status['thumbnail_pic'] + "', '" + str(status['user']['id']) +  "', '" + status['user']['screen_name'] + "', " + str(status['reposts_count']) +  ", " + str(status['comments_count']) + ")"
    try:
        cursor.execute(query_header_statuses + query_body_statuses)
    except sqlite3.Error, e:
        #print  "This status has already been inserted.", e.args[0]
        pass
    
    ############################users################################  
    query_body_users   = str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', '" + str(status['user']['province']) + "', '" + str(status['user']['city']) + "', '" + status['user']['location'] + "', '" + status['user']['description'].replace("'", "''") + "', '" + status['user']['url'] + "', '" + status['user']['profile_image_url'] + "', '" + status['user']['profile_url'] + "', '" + status['user']['domain'] + "', '" + str(status['user']['weihao']) + "', '" + status['user']['gender'] + "', " + "datetime('" +  parseTime(status['user']['created_at']) + "')" + ", '" + str(status['user']['geo_enabled']) + "', '" + str(status['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + status['user']['verified_reason'] + "', '" + status['user']['lang'] + "', " + str(status['user']['bi_followers_count']) + ", " + str(status['user']['followers_count']) + ", " + str(status['user']['friends_count']) + ", " + str(status['user']['statuses_count']) + ", " + str(status['user']['favourites_count']) + ")"
    try:
        cursor.execute(query_header_users + query_body_users)
    except sqlite3.Error, e:
        #print  "This user has already been inserted.", e.args[0]
        pass
    
    ############################retweets################################
    if 'retweeted_status' in keys:
        cursor.execute("update statuses set status_type=1 where id == " + str(status['id']))
        if 'user' in status['retweeted_status'].keys():
            query_body_retweets = str(status['retweeted_status']['id'] + status['id']) + ", 1," + str(status['retweeted_status']['id']) + ", " + str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', " + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + "datetime('" +  parseTime(status['created_at']) + "')"  + ")"
            try:
                cursor.execute(query_header_retweets + query_body_retweets)
            except sqlite3.Error, e:                    
                #print  "This retweeted relationship has already been inserted.", e.args[0]
                pass

            query_body_users = str(status['retweeted_status']['user']['id']) + ", '" + status['retweeted_status']['user']['screen_name'] + "', '" + str(status['retweeted_status']['user']['province']) + "', '" + str(status['retweeted_status']['user']['city']) + "', '" + status['retweeted_status']['user']['location'] + "', '" + status['retweeted_status']['user']['description'].replace("'", "''") + "', '" + status['retweeted_status']['user']['url'] + "', '" + status['retweeted_status']['user']['profile_image_url'] + "', '" + status['retweeted_status']['user']['profile_url'] + "', '" + status['retweeted_status']['user']['domain'] + "', '" + str(status['retweeted_status']['user']['weihao']) + "', '" + status['retweeted_status']['user']['gender'] + "', " + "datetime('" +  parseTime(status['retweeted_status']['user']['created_at']) + "')" + ", '" + str(status['retweeted_status']['user']['geo_enabled']) + "', '" + str(status['retweeted_status']['user']['verified']) + "', '" + status['retweeted_status']['user']['avatar_large'] + "', '" + status['retweeted_status']['user']['verified_reason'] + "', '" + status['retweeted_status']['user']['lang'] + "', " + str(status['retweeted_status']['user']['bi_followers_count']) + ", " + str(status['retweeted_status']['user']['followers_count']) + ", " + str(status['retweeted_status']['user']['friends_count']) + ", " + str(status['retweeted_status']['user']['statuses_count']) + ", " + str(status['retweeted_status']['user']['favourites_count']) + ")"
            try:
                cursor.execute(query_header_users + query_body_users)
            except sqlite3.Error, e:
                #print  "This user has already been inserted.", e.args[0]
                pass

    ############################reposts##############################
    if status['reposts_count'] != 0:
        reposts_max_id = 0
        n = 0
        while status['reposts_count'] >= COUNT * n:
            if (n+1)*COUNT > status['reposts_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['reposts_count'])
            #print "Retrieving Reposts:" +  str(completed*100) + "%"
            n = n + 1
            reposts_obj = getResponseObject('https://api.weibo.com/2/statuses/repost_timeline.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(reposts_max_id) + '&access_token=' + TOKEN)
            if reposts_obj == {} or reposts_obj == []:
                continue
            reposts_max_id = reposts_obj['next_cursor']
            for repost in reposts_obj['reposts']:
                keys_repost = repost.keys()
                
                if 'deleted' in keys_repost:
                    continue
                if str(repost['geo']) == '':
                    repost['geo'] = 'None'
                if str(repost['geo']) != 'None' :
                    repost['geo'] = str(repost['geo']['coordinates'][0]) + "," + str(repost['geo']['coordinates'][1])
                
                query_body_retweets  = str(repost['id'] + status['id']) + ", 1," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(repost['id']) + ", " + str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ")"
                query_body_statuses = str(repost['id']) + ", 1, '" + repost['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(repost['created_at']) + "')" + ", '" + repost['source'] + "', '" + str(repost['geo']) +  "', '" + "None" +  "', '" + str(repost['user']['id']) +  "', '" + repost['user']['screen_name'] + "', " + str(repost['reposts_count']) +  ", " + str(repost['comments_count']) + ")"
                
                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This repost relationship has been inserted,", e.args[0]
                    pass
                
                try:
                    cursor.execute(query_header_statuses + query_body_statuses)
                except sqlite3.Error, e:
                    #print  "This repost has already been inserted.", e.args[0]
                    pass
                    
                query_body_users   = str(repost['user']['id']) + ", '" + repost['user']['screen_name'] + "', '" + str(repost['user']['province']) + "', '" + str(repost['user']['city']) + "', '" + repost['user']['location'] + "', '" + repost['user']['description'].replace("'", "''") + "', '" + repost['user']['url'] + "', '" + repost['user']['profile_image_url'] + "', '" + repost['user']['profile_url'] + "', '" + repost['user']['domain'] + "', '" + str(repost['user']['weihao']) + "', '" + repost['user']['gender'] + "', " + "datetime('" +  parseTime(repost['user']['created_at'])  + "')" + ", '" + str(repost['user']['geo_enabled']) + "', '" + str(repost['user']['verified']) + "', '" + repost['user']['avatar_large'] + "', '" + repost['user']['verified_reason'] + "', '" + repost['user']['lang'] + "', " + str(repost['user']['bi_followers_count']) + ", " + str(repost['user']['followers_count']) + ", " + str(repost['user']['friends_count']) + ", " + str(repost['user']['statuses_count']) + ", " + str(repost['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

    ############################comments################################
    if status['comments_count'] != 0:
        #print 'comments:' + str(status['comments_count'])
        #print str(status['id'])        
        comments_max_id = 0
        n = 0
        while status['comments_count'] >= COUNT*n:
            if (n+1)*COUNT > status['comments_count']:
                completed = 1
            else:
                completed = (n+1)*COUNT/float(status['comments_count'])
            #print "Retrieving Comments:" +  str(completed*100) + "%"
            n = n + 1 
            #time.sleep(2) #helpful when try to limit the request to a certain amount
            comments_obj = getResponseObject('https://api.weibo.com/2/comments/show.json?source=2933540621&id=' + str(status['id']) + '&count=' + str(COUNT) + '&max_id=' + str(comments_max_id) + '&access_token=' + TOKEN)
            if comments_obj == {}:
                continue
            comments_max_id = comments_obj['next_cursor']
                            
            for comment in comments_obj['comments']:
                keys_comment = comment.keys()
                query_body_retweets  = str(comment['id'] + status['id']) + ", 2," + str(status['id']) + ", " + str(status['user']['id']) + ", '" + status['user']['screen_name'] + "', " + str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ")"
                query_body_comments = str(comment['id']) + ", 2, '" + comment['text'].replace("'", "''") + "', " + "datetime('" +  parseTime(comment['created_at']) + "')" + ", '" + comment['source'] + "', '" + str(comment['user']['id']) +  "', '" + comment['user']['screen_name'] + "')"
                                    
                try:
                    cursor.execute(query_header_retweets + query_body_retweets)
                except sqlite3.Error, e:
                    #print "This comment relationship has already been inserted.", e.args[0]
                    pass
                
                try:
                    cursor.execute(query_header_comments + query_body_comments)
                except sqlite3.Error, e:
                    #print  "This comment has already been inserted.", e.args[0]
                    pass

                query_body_users   = str(comment['user']['id']) + ", '" + comment['user']['screen_name'] + "', '" + str(comment['user']['province']) + "', '" + str(comment['user']['city']) + "', '" + comment['user']['location'] + "', '" + comment['user']['description'].replace("'", "''") + "', '" + comment['user']['url'] + "', '" + comment['user']['profile_image_url'] + "', '" + comment['user']['profile_url'] + "', '" + comment['user']['domain'] + "', '" + str(comment['user']['weihao']) + "', '" + comment['user']['gender'] + "', " + "datetime('" +  parseTime(comment['user']['created_at'])  + "')" + ", '" + str(comment['user']['geo_enabled']) + "', '" + str(comment['user']['verified']) + "', '" + status['user']['avatar_large'] + "', '" + comment['user']['verified_reason'] + "', '" + comment['user']['lang'] + "', " + str(comment['user']['bi_followers_count']) + ", " + str(comment['user']['followers_count']) + ", " + str(comment['user']['friends_count']) + ", " + str(comment['user']['statuses_count']) + ", " + str(comment['user']['favourites_count']) + ")"
                try:
                    cursor.execute(query_header_users + query_body_users)
                except sqlite3.Error, e:
                    #print  "This user has already been inserted.", e.args[0]
                    pass

                if 'reply_comment' in keys_comment:
                    query_body_retweets  = str(comment['id'] + comment['reply_comment']['id']) + ", 3," + str(comment['reply_comment']['id']) + ", " + str(comment['reply_comment']['user']['id']) + ", '" + comment['reply_comment']['user']['screen_name'] + "', "  +  str(comment['id']) + ", " + str(comment['user']['id']) + ", '" + comment['user']['screen_name'] +  "', datetime('" +  parseTime(comment['created_at']) + "') )"
                    try:
                        cursor.execute(query_header_retweets + query_body_retweets)
                    except sqlite3.Error, e:
                        #print  "This reply-comment relationship has already been inserted.", e.args[0]
                        pass
    #t = t + 1
    #print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (t-1)*100/4) + '%' + '--------------------------------------'
    conn.commit()
    conn.close()
    
def parseTime(timestring):
    struct_time = time.strptime(timestring, '%a %b %d %H:%M:%S +0800 %Y')
    return time.strftime('%Y-%m-%d %H:%M:%S',struct_time)

def processTerms(terms, pages, database):
    for term in terms:
        processTerm(term, pages, database)

def processTerm(term, pages, database):
    i = 0
    while i < pages:
        i = i + 1
        obj = getResponseObject('https://api.weibo.com/2/search/topics.json?source=2933540621&q='+ urllib.quote(term) + '&count=50&page=' + str(i))
        if obj == {}:
            continue
        t = 0
        for status in obj['statuses']:
            if 'deleted' not in status.keys():
                processStatus(database, status)
            t = t + 1
            print '--------------------------------------' + str(round(t/float(len(obj['statuses']))*100/4,2)+ (i-1)*100/4) + '%' + '--------------------------------------'    
    print "Congrat! it's done!"