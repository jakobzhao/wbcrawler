# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 11, 2012

@author: bo
'''
# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 10, 2012
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
import os.path

import networkx as nx
import matplotlib.pylab as plt
from matplotlib.font_manager import fontManager

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

#--------------------------------find the chinese characters-----------------------------------

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.xticks([])
plt.yticks([])
x, y = 0.05, 0.08
fonts = [font.name for font in fontManager.ttflist if 
    os.path.exists(font.fname) and os.stat(font.fname).st_size>1e6] 
font = set(fonts)
dy = (1.0-y)/(len(fonts)/4 + (len(fonts)%4!=0))
for font in fonts:
    t = ax.text(x, y, u"中文字体"+ font, {'fontname':font, 'fontsize':14}, transform=ax.transAxes) 
    print font
    ax.text(x, y-dy/2, font, transform=ax.transAxes)
    x += 0.25
    if x >= 1.0:
        y += dy
        x = 0.05
plt.show()



#--------------------------------build network-----------------------------------


database = '../data/薄熙来.db'

conn = sqlite3.connect(database)#to name it with a specific word
cursor = conn.cursor()

G = nx.DiGraph()

cursor.execute('select Id, Source_Name, To_Name from user_edges')
edges = cursor.fetchall()
cursor.execute('select Id, Nodes from user_nodes')
nodes = cursor.fetchall()
conn.commit()
conn.close()



for node in nodes:
    G.add_node(node[1])
for edge in edges:
    G.add_edge(edge[1],edge[2])

print G.nodes()

nx.draw(G,node_size=60,font_size=8) 

#nx.draw(G) 

plt.savefig("../img/path2.png")
plt.show()