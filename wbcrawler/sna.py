# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys
from pymongo import MongoClient, DESCENDING
import networkx as nx
from settings import TZCHINA
from log import *

reload(sys)
sys.setdefaultencoding('utf-8')


def generate_network(project, address, port, output="wbcrawler.gexf", year=2015, month=10, date=20):
    client = MongoClient(address, port)
    db = client[project]
    g = nx.DiGraph()
    # Now the network is generated in correct source-target relations.
    # source is the repliers, while the target is the original post.
    # from the custmized start time
    start_time = datetime.datetime(year, month, date, 0, 0, 0, 0, tzinfo=TZCHINA)
    recent_posts = db.posts.find({"timestamp": {"$gt": start_time}})
    for post in recent_posts:
        if post['user']['username'] != u'蒋中挺':
            g.add_node(post['user']['username'], weight=post['fwd_count'])
            for reply in post['replies']:
                if reply['user']['username'] != u'蒋中挺':
                    g.add_node(reply['user']['username'], weight=post['fwd_count'])
                    g.add_edge(reply['user']['username'], post['user']['username'])

    nx.write_gexf(g, output, prettyprint=True)
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))


def generate_sematic_network(input='', output="sematic.gexf"):
    g = nx.DiGraph()
    f = open(input, 'r')
    for line in f.readlines():
        fields = line.split(',')
        g.add_node(unicode(fields[0]))
        g.add_edge(unicode(fields[0]), unicode(fields[1]), weight=float(fields[2]))

    nx.write_gexf(g, output, prettyprint=True)
    log(NOTICE, 'the nework file is suceessfully stored in %s.' % output)


def opinion_leaders(project, address, port, output="op.csv", year=2015, month=10, date=20):
    client = MongoClient(address, port)
    db = client[project]
    # g = nx.DiGraph()
    # Now the network is generated in correct source-target relations.
    # source is the repliers, while the target is the original post.
    # from the custmized start time
    # start_time = datetime.datetime(year, month, date, 0, 0, 0, 0, tzinfo=TZCHINA)
    f = open(output, 'w')
    # recent_posts = db.posts.find({'fwd_count': {'$gt': fwd}}).sort('mid', DESCENDING)
    # recent_posts = db.posts.find().sort('mid', DESCENDING)
    recent_posts = db.posts.find()
    users = {}
    i = 0
    for post in recent_posts:
        i += 1
        print i
        stop = False
        reposts = [u'//', u'repost', u'转发微博', u'轉發微博']
        for repost in reposts:
            if repost in post['content'] or post['content'] == u'':
                stop = True
                break
        if stop:
            continue
        username = post['user']['username'].encode('utf-8', 'ignore')
        userid = post['user']['userid']
        fwd_count = post['fwd_count']

        if username in users.keys():
            users[username]['fwd_count'] += fwd_count
        else:
            users[username] = {}
            users[username]['fwd_count'] = fwd_count
        if db.users.find({'userid': userid}).count() >= 1:
            user = db.users.find_one({'userid': userid})
            users[username]['verified'] = user['verified']
            users[username]['verified_info'] = user['verified_info']

    for user in users:
        try:
            line = '%s, %s, %s, %d\n' % (user.encode('gbk', 'ignore'), str(users[user]['verified']), users[user]['verified_info'].encode('gbk', 'ignore'), users[user]['fwd_count'])
            f.write(line)
            log(NOTICE, line)
        except:
            pass
    f.close()
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))

if __name__ == '__main__':
    pass
