# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

# libraries
import socket
import smtplib
from pymongo import MongoClient

from wbcrawler.settings import EMAIL_PASSWORD
from wbcrawler.log import *


# receiver string
# example rief_report('jakobzhao@gmail.com;bo_zhao@hks.harvard.edu', "weibo")
# funcs

def brief_report(settings):
    pis = settings['pis']
    project = settings['project']
    address = settings['address']
    port = settings['port']
    robot_table = settings['robot_table']

    sender = 'snsgis@gmail.com'
    username = 'snsgis@gmail.com'
    t = datetime.datetime.now().strftime('%Y-%m-%d')

    pi_str = ''
    for pi in pis:
        pi_str += (pi + ';')

    now = datetime.datetime.now()
    utc_now_1 = now - datetime.timedelta(days=1)
    utc_now_2 = now - datetime.timedelta(days=2)
    utc_now_5 = now - datetime.timedelta(days=5)

    # For robot information
    if 'remote' not in settings.keys():
        client = MongoClient(settings['address'], settings['port'])
        robot_table = settings['robot_table']
    else:
        client = MongoClient(settings['remote']['address'], settings['remote']['port'])
        robot_table = settings['remote']['robot_table']

    inused = client.local[robot_table].find({'inused': True}).count()
    total = client.local[robot_table].find().count()

    # For post information
    client = MongoClient(address, port)
    db = client[project]

    total_posts = db.posts.find().count()
    total_users = db.users.find().count()

    count_1 = db.posts.find({"timestamp": {"$gt": utc_now_1}}).count()
    count_2 = db.posts.find({"timestamp": {"$gt": utc_now_2}}).count()
    count_5 = db.posts.find({"timestamp": {"$gt": utc_now_5}}).count()
    count_6 = db.users.find({"latlng": {"$ne": [0, 0]}}).count()
    count_7 = db.users.find({"path": {"$ne": []}}).count()

    line_1 = "Occupied / total Robots: %d / %d" % (inused, total)
    line_2 = "Total posts: %d" % total_posts
    line_3 = "Within the past 24 hours: %d collected" % count_1
    line_4 = "Within the past 2 days: %d collected" % count_2
    line_5 = "Within the past 5 days: %d collected" % count_5
    line_6 = "Users with paths / not: %d / %d" % (count_7, total_users - count_7)
    line_7 = "Geocoded users / not: %d / %d" % (count_6, total_users - count_6)

    msg = '''From: Weibo Crawler Server <snsgis@gmail.com>
To: ''' + pi_str[:-1] + '''
Subject: [''' + t + '''] Daily Briefing for ''' + project.capitalize() + ''' Project
MIME-Version: 1.0

Dear PI(s),

Here is a briefing about the progress of Weibo data harvest:

     ''' + line_1 + '''
     ''' + line_2 + '''
     ''' + line_3 + '''
     ''' + line_4 + '''
     ''' + line_5 + '''
     ''' + line_6 + '''
     ''' + line_7 + '''
--
Sent from the Weibo Cralwer Server.'''
    # The actual mail send
    try:
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com', '587')
        server.ehlo()
        server.starttls()
        server.login(username, EMAIL_PASSWORD)
        server.sendmail(sender, pis, msg)
        server.quit()
    except socket.gaierror, e:
        print str(e) + "/n error raises when sending E-mails."
