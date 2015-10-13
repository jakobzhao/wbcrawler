# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2012
@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

import sqlite3

import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

#--------------------------------build network-----------------------------------


database = '../data/薄熙来.db'

conn = sqlite3.connect(database)#to name it with a specific word

cursor = conn.cursor()
cursor.execute('select Id, Source_Name, Target_Name from user_edges')
edges = cursor.fetchall()
cursor.execute('select Id, Nodes from user_nodes')
nodes = cursor.fetchall()
conn.commit()
conn.close()


G = nx.DiGraph()
for node in nodes:
    G.add_node(node[1])
for edge in edges:
    G.add_edge(edge[1],edge[2])

#print G.nodes()
#nx.draw(G,node_size=160,font_size=16) 
#nx.draw(G) 
nx.draw(G,pos = nx.spectral_layout(G))

degree = nx.degree_histogram(G) #返回图中所有节点的度分布序列（从1至最大度的出现频次）

#print nx.average_clustering(G) #平均群聚系数
#print nx.clustering(G) #各个节点的群聚系数


#centrality_str = json.dumps(nx.degree_centrality(G), encoding="UTF-8", ensure_ascii=False)

#centrality_json = json.loads(centrality_str)
#centrality_json2 = nx.degree_centrality(G)
centrality = nx.degree_centrality(G)
sorted_centrality = sorted(centrality.items(), key=lambda centrality:centrality[1])[-3:]
#sorted_centrality2 = sorted(centrality_json2.items(), key=lambda centrality_json2:centrality_json2[1])[-3:]

#plt.show()