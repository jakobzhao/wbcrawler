# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 26, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
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
import sqlite3
import networkx as nx
import matplotlib.pylab as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


#--------------------------------build network-----------------------------------


database = '../data/pm2.5.db'

conn = sqlite3.connect(database)#to name it with a specific word
cursor = conn.cursor()

cursor.execute('select Id, Source_Name, Target_Name from user_edges')
edges = cursor.fetchall()
cursor.execute('select Id, Node from user_nodes')
nodes = cursor.fetchall()
conn.commit()
conn.close()



G = nx.DiGraph()
for node in nodes:
    G.add_node(node[1])
for edge in edges:
    G.add_edge(edge[1],edge[2])

#print G.nodes()

#nx.draw(G,node_size=60,font_size=8) 
#nx.draw(G)
nx.write_gexf(G,'test2.gexf',prettyprint = True) 

plt.savefig("../data/img/path2.png")