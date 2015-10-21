# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import sys

from pymongo import MongoClient
import networkx as nx

from log import *

reload(sys)
sys.setdefaultencoding('utf-8')


def generate_network(project, address, port, output="wbcrawler.gexf"):
    client = MongoClient(address, port)
    db = client[project]
    posts = db.posts.find()
    g = nx.DiGraph()
    # Now the network is generated in correct source-target relations.
    # source is the repliers, while the target is the original post.
    for post in posts:
        g.add_node(post['user']['username'])
        for reply in post['replies']:
            g.add_node(reply['user']['username'])
            g.add_edge(reply['user']['username'], post['user']['username'])

    nx.write_gexf(g, output, prettyprint=True)
    # plt.savefig("path2.png")
    log(NOTICE, 'the nework file of "%s" is suceessfully stored in %s.' % (project, output))


if __name__ == '__main__':
    pass
