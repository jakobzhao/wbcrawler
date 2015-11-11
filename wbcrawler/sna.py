# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys
from pymongo import MongoClient
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
        g.add_node(post['user']['username'])
        for reply in post['replies']:
            g.add_node(reply['user']['username'])
            g.add_edge(reply['user']['username'], post['user']['username'])

    nx.write_gexf(g, output, prettyprint=True)
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))


if __name__ == '__main__':
    pass
