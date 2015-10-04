# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Jan 2, 2013

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

from shutil import copy
import os,sys
from utils import processTopic, getOpinionLeadersByCentrality, searchTopicFromUser,geocoding, sqlite2shp




topic = 'love'

terms = ['love', 'hate']

refresh = True
pages = 1
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
#--------------------------------------------------------------------------------------------------------
database = current_path + '/../data/' + topic +'.db'

if os.path.exists(database):
    if refresh:
        copy(current_path + '/' + 'weibo_crawler_template.db', database)
else: 
    copy(current_path + '/' + 'weibo_crawler_template.db', database)

for term in terms:
    processTopic(term, pages, database)

opinion_leaders = getOpinionLeadersByCentrality(1, database)
print opinion_leaders

num = len(opinion_leaders)
print "there are "+ str(num) + " opinion leaders."

i = 1
for leader in opinion_leaders:
    print "------------------------No." + str(i) + ", " +str(num)+" in total.---------------------------"
    searchTopicFromUser(leader[0], terms, database)
    i = i + 1

geocoding(database)
sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')
if __name__ == '__main__':
    pass