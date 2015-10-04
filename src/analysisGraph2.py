# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2012

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
import matplotlib


import math
from scipy import linalg
import numpy as np
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


#--------------------------------build network-----------------------------------


database = '../data/xilaibo.db'

conn = sqlite3.connect(database)#to name it with a specific word
cursor = conn.cursor()

cursor.execute('select id, source_name, target_name from user_edges')
edges = cursor.fetchall()
cursor.execute('select id, node from user_nodes')
nodes = cursor.fetchall()
conn.commit()
conn.close()



G = nx.DiGraph()
for node in nodes:
    G.add_node(node[1])
for edge in edges:
    G.add_edge(edge[1],edge[2])


degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
##print "Degree sequence", degree_sequence
dmax=max(degree_sequence)


x, y , t = [], [] ,-1
for item in degree_sequence:
    if item != t:
        x.append(item)
        y.append(degree_sequence.count(item))
    t = item
print x
print y
print len(x)
print len(degree_sequence)
plt.loglog(degree_sequence,'b+',marker='o')
plt.loglog(x, y,'g-',marker='3')
plt.title("Degree Distribution")
plt.ylabel("degree")
plt.xlabel("count")

##===============================================
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.loglog(x,y,"o")  # 绘制实际数据的图形 x,y表示原始数据的横坐标与纵坐标，没有贴出生成这些数据的代码

#plt.loglog(x,y,"g-")

lnx = [math.log(f+.01,math.e) for f in x]   # 对x进行对数转换

lny = [math.log(f+.01,math.e) for f in y]   # 对y进行对数转换

a = np.mat([lnx,[1]*len(x)]).T          # 自变量矩阵a
b = np.mat(lny).T             # 因变量矩阵b
(t,res,rank,s) = linalg.lstsq(a,b)      # 最小二乘法求系数

print t
r = t[0][0]
c = t[1][0]
x_ = x 
y_ = [math.e**(r*a+c) for a in lnx]    # 根据求的的系数求出y*
plt.loglog(x_,y_,"r-")                  # 绘制拟合的曲线图



plt.savefig("../data/img/power_law.png")
plt.show()