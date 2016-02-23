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
from gensim.models import Word2Vec
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
        user = db.users.find_one({'userid': post['user']['userid']})
        if user and 'verified' in user.keys():
            g.add_node(post['user']['username'], weight=post['fwd_count'], verified=str(user['verified']))
        else:
            g.add_node(post['user']['username'], weight=post['fwd_count'], verified='False')
        for reply in post['replies']:
            re_user = db.users.find_one({'userid': reply['user']['userid']})
            if re_user and 'verified' in re_user.keys():
                g.add_node(reply['user']['username'], weight=reply['fwd_count'], verified=str(re_user['verified']))
            else:
                g.add_node(reply['user']['username'], weight=reply['fwd_count'], verified='False')
            g.add_edge(reply['user']['username'], post['user']['username'])

    nx.write_gexf(g, output, prettyprint=True)
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))


def generate_sematic_network(keywords=[], depth=[10, 10, 10], w2v_file='', gexf_file=''):
    model = Word2Vec.load(w2v_file)
    g = nx.DiGraph()
    for keyword in keywords:
        g.add_node(keyword)
        for w, i in model.most_similar(keyword, topn=depth[0]):
            if w in keywords:
                w = keyword
            g.add_node(w)
            g.add_edge(w, keyword, weight=i * i * 100)
            notice = (w + ' ' + str(i)).encode('gbk', 'ignore')
            log(NOTICE, notice)
            for t, j in model.most_similar(w, topn=depth[1]):
                g.add_node(t)
                g.add_edge(t, w, weight=j * j * 100)
                notice = (t + ' ' + str(j)).encode('gbk', 'ignore')
                log(NOTICE, notice)
                for s, k in model.most_similar(t, topn=depth[2]):
                    g.add_node(s)
                    g.add_edge(s, t, weight=k * k * 100)
                    notice = (s + ' ' + str(k)).encode('gbk', 'ignore')
                    log(NOTICE, notice)

    nx.write_gexf(g, gexf_file, prettyprint=True)
    log(NOTICE, 'the nework file is suceessfully stored in %s.' % gexf_file)


def generate_sematic_network2(keyword, related_keywords, threshold=0.5, w2v_file='', gexf_file=''):
    model = Word2Vec.load(w2v_file)
    g = nx.DiGraph()
    g.add_node(keyword)
    for related in related_keywords:
        g.add_node(related)
        w = model.similarity(keyword, related)
        print keyword, related, w
        g.add_edge(related, keyword, weight=int(w * w * 100 / threshold / threshold))

    for related_1 in related_keywords:
        for related_2 in related_keywords:
            if related_1 != related_2:
                w = model.similarity(related_1, related_2)
                if w > threshold:
                    g.add_edge(related_2, related_1, weight=int(w * w * 100))
                    print related_1, related_2, w
    nx.write_gexf(g, gexf_file, prettyprint=True)
    log(NOTICE, 'the nework file is suceessfully stored in %s.' % gexf_file)


def generate_sematic_network3(keyword, related_keywords, threshold=0.5, depth=10, w2v_file='', gexf_file=''):
    model = Word2Vec.load(w2v_file)
    g = nx.DiGraph()
    g.add_node(keyword)
    for related in related_keywords:
        g.add_node(related)
        w = model.similarity(keyword, related)
        g.add_edge(related, keyword, weight=int(w * w * 100 / threshold / threshold))
        print keyword, related, w

    # for related_1 in related_keywords:
    #     for related_2 in related_keywords:
    #         if related_1 != related_2:
    #             p = model.similarity(related_1, related_2)
    #             g.add_edge(related_2, related_1, weight=int(p*p*100))
    #             print related_1, related_2, w

    for related in related_keywords:
        g.add_node(related)
        for w, i in model.most_similar(related, topn=depth):
            if i > threshold:
                g.add_node(w)
                g.add_edge(w, related, weight=int(i * i * 100))
                notice = (w + ' ' + str(i)).encode('gbk', 'ignore')
                log(NOTICE, notice)
                for t, j in model.most_similar(w, topn=depth):
                    if j > threshold:
                        g.add_node(t)
                        g.add_edge(t, w, weight=int(j * j * 100))
                        notice = (t + ' ' + str(j)).encode('gbk', 'ignore')
                        log(NOTICE, notice)
    # notice = (s + ' ' + str(k)).encode('gbk', 'ignore')
    # log(NOTICE, notice)
    nx.write_gexf(g, gexf_file, prettyprint=True)
    log(NOTICE, 'the nework file is suceessfully stored in %s.' % gexf_file)


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
        reposts = [u'repost', u'转发微博', u'轉發微博']
        for repost in reposts:
            if repost in post['content'] or post['content'] == u'':
                stop = True
                break
        if stop:
            continue

        # username = post['user']['username'].encode('utf-8', 'ignore')
        username = post['user']['username']
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
            line = '%s, %s, %s, %d\n' % (user, str(users[user]['verified']), users[user]['verified_info'], users[user]['fwd_count'])
            f.write(line)
            log(NOTICE, line)
        except:
            pass
    f.close()
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))


def export_posts(project, address, port, output="op.csv"):
    client = MongoClient(address, port)
    db = client[project]
    f = open(output, 'w')
    f.write('mid, topic, keyword, lat, lng, sentiment, pos, neg, timestamp, fwd_count, username, verified, verified_info, content \n')
    # f.write('mid, topic, keyword, lat, lng, sentiment, pos, neg, timestamp, fwd_count, username, verified \n')
    posts = db.posts.find()
    count = posts.count()
    i = 0
    for post in posts:
        i += 1
        log(NOTICE, "#%d, %d post remain." % (i, count - i))
        username = post['user']['username'].encode('utf-8', 'ignore')
        userid = post['user']['userid']
        user = db.users.find_one({'userid': userid})
        if user is not None:
            verified = str(user['verified'])
            verified_info = user['verified_info']

        content = post['content'].encode('gbk', 'ignore').decode('gbk', 'ignore')

        # =================IF HAVING TOPIC==============================
        # if post['topic'] == []:
        #     topics = ['none']
        # else:
        #     topics = post['topic']
        # for topic in topics:
        #     # line = '%d, %s, %s, %f, %f, %f, %f, %f, %s, %d, %s, %s, %s, %s\n' % (post['mid'], topic, post['keyword'], post['latlng'][0], post['latlng'][1], float(post['sentiment']), float(post['pos']), float(post['neg']), str(post['timestamp']), int(post['fwd_count']), username, verified, verified_info, content)
        #     line = '%d, %s, %s, %f, %f, %f, %f, %f, %s, %d, %s, %s\n' % (
        #     post['mid'], topic, post['keyword'], post['latlng'][0], post['latlng'][1], float(post['sentiment']), float(post['pos']), float(post['neg']), str(post['timestamp']), int(post['fwd_count']), username, verified)
        #     f.write(line)
        #     try:
        #         log(NOTICE, line)
        #     except:
        #         pass
        # =================IF HAVING TOPIC==============================
        try:
            line = '%d, %s, %f, %f, %s, %d, %s, %s, %s, %s\n' % (post['mid'], post['keyword'], post['latlng'][0], post['latlng'][1], str(post['timestamp']), int(post['fwd_count']), username, verified, verified_info, content)
            # line = '%d, %s, %f, %f, %s, %d, %s, %s, %s\n' % (post['mid'], post['keyword'], post['latlng'][0], post['latlng'][1],  str(post['timestamp']), int(post['fwd_count']), username, verified, verified_info)
        except KeyError:
            pass

        f.write(line)
        try:
            log(NOTICE, line)
        except:
            pass
    f.close()
    log(NOTICE, 'mission completes')
if __name__ == '__main__':
    pass
