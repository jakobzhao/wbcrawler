# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

# libraries
import socket
import smtplib

from pymongo import MongoClient

from wbcrawler.settings import EMAIL_PASSWORD
from wbcrawler.log import *


# receiver string
# example rief_report('jakobzhao@gmail.com;bo_zhao@hks.harvard.edu', "weibo")
# funcs


def brief_report(reciever_string, project, address, port):
    sender = 'snsgis@gmail.com'
    username = 'snsgis@gmail.com'
    t = datetime.datetime.now(TZCHINA).strftime('%Y-%m-%d %H:%M')

    now = datetime.datetime.now()
    utc_now_1 = now - datetime.timedelta(days=1)
    utc_now_2 = now - datetime.timedelta(days=2)
    utc_now_5 = now - datetime.timedelta(days=5)

    client = MongoClient(address, port)
    inused = client.local.accounts.find({'inused': False}).count()
    total = client.local.accounts.find().count()

    db = client[project]

    total_posts = db.posts.find().count()
    total_users = db.users.find().count()

    count_1 = db.posts.find({"timestamp": {"$gt": utc_now_1}}).count()
    count_2 = db.posts.find({"timestamp": {"$gt": utc_now_2}}).count()
    count_5 = db.posts.find({"timestamp": {"$gt": utc_now_5}}).count()
    count_6 = db.users.find({"latlng": {"$ne": [0, 0]}}).count()
    count_7 = db.users.find({"path": {"$ne": []}}).count()

    line_1 = "Occupied / total accounts: %d / %d" % (inused, total)
    line_2 = "Total posts: %d" % total_posts
    line_3 = "During the past 24 hours: %d posts collected" % count_1
    line_4 = "During the past 2 days: %d posts collected" % count_2
    line_5 = "During the past 5 days: %d posts collected" % count_5
    line_6 = "Geocoded users / not: %d / %d" % (count_6, total_users - count_6)
    line_7 = "Users with paths / not: %d / %d" % (count_7, total_users - count_7)

    msg = '''From: Crawler Server <snsgis@gmail.com>
To: ''' + reciever_string + '''
Subject: Daily Breif Report for ''' + project.upper() + ''' Project
MIME-Version: 1.0

Dear Lord,

''' + line_1 + '''
''' + line_2 + '''
''' + line_3 + '''
''' + line_4 + '''
''' + line_5 + '''
''' + line_6 + '''
''' + line_7 + '''
''' + t + '''
--
Sent from Weibo Cralwer Server
'''
    # The actual mail send
    try:
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com', '587')
        server.ehlo()
        server.starttls()
        server.login(username, EMAIL_PASSWORD)
        server.sendmail(sender, reciever_string, msg)
        server.quit()
    except socket.gaierror, e:
        print str(e) + "/n error raises when sending E-mails."
