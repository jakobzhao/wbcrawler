# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

import sqlite3
import os
import sys

database = '../data/shiyipan.db'

#------------------------reading the words which will be removed--------------------------
#current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
#remove_dic = open (current_path + '/remove.dic', 'r')
#lines = remove_dic.readlines()
#words = []
#for line in lines:
#    words.append(line.replace('\n',''))

#------------------------loading the database--------------------------------------------
conn = sqlite3.connect(database)#to name it with a specific word
cursor = conn.cursor()

cursor.execute('select text from statuses order by id desc')
text = cursor.fetchall()
conn.commit()
conn.close()



#------------------------reading the words which will be removed--------------------------------------------

current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
remove_dic = open(current_path + '/./ICTCLAS/remove.dic', 'r')
lines = remove_dic.readlines()
remove =[]
for line in lines:
    remove.append(line.replace('\n',''))
#-------------------------------organize the paragraph--------------------------------------------
paragraph = ''
for item in text:
    paragraph += item[0]

#-----------------------------------segment the words-----------------------------------------------

#from pyictclas import PyICTCLAS,CodeType

from backup.pyictclas import PyICTCLAS, CodeType

pcl = PyICTCLAS()
pcl.ictclas_importUserDict('./ICTCLAS/user.txt',CodeType.CODE_TYPE_UTF8)
#pcl.ictclas_importUserDict('瓜瓜@@nr;王立军@@nr;薄瓜瓜@@nr;李庄@@nr;司马南@@nr',CodeType.CODE_TYPE_UTF8)
paragraph = pcl.ictclas_paragraphProcess(paragraph, CodeType.CODE_TYPE_UTF8, True).value
pcl.ictclas_exit()


#如果/c 你/rr 增加/v 了/ule 一些/mq 成员变量/nr ,/wd  全能/n 补全/nr 还/d 不/d 能/v 马上/d 将/d 新成员/nr 补全/nr ,/wd  需要/v 你/rr 重新/d 生成/v 
#一下/mq tags/x 文件/n ,/wd  但是/c 你/rr 不/d 用/v 重启/nr vim/x ,/wd  只/d 是/vshi 重新/d 生成/v 一下/mq tags/x 文件/n 就/d 行/vi 了/y ,/wd
#这时/rzt 全能/n 补全/nr 已经/d 可以/v 自动/b 补全/nr 了/vi ,/wd  还/d 真/d 够/v "/x 全能/n "/x 吧/y 

tokens = paragraph.split(' ')
refined_tokens = []
for item in tokens:
    if item.find('/n') >= 0:
        b = item[:item.find('/n')]
        if b not in remove:
            refined_tokens.append(b)

#-----------------------------------data analysis and visualize-----------------------------------------------
import nltk
import pylab
pylab.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #load a font for Chinese characters.

fdist1 = nltk.FreqDist(refined_tokens)
print fdist1

#plt.title("Degree Distribution")
#plt.ylabel("degree")
#plt.xlabel("count")

vocabulary1 = fdist1.keys()
print vocabulary1[:10]
fdist1.plot(50, title= "Word Frequency",  cumulative=False)