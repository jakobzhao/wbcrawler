# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 11, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

from shutil import copy
import os,sys
from utils import *


topic = 'zhaobo.6'
terms = ['t']

refresh = False
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
database = current_path + '/../data/' + topic +'.db'
#--------------------------------------------------------------------------------------------------------

createDB(database, refresh)


#opinion_leaders = getOpinionLeadersByCentrality(10, database)
#print opinion_leaders

#num = len(opinion_leaders)
#print "there are "+ str(num) + " opinion leaders."

#i = 1
#for leader in opinion_leaders:
#    print "------------------------No." + str(i) + ", " +str(num)+" in total.---------------------------"
#    searchTopicFromUser(leader[0], terms, database)
#    i = i + 1

searchTermsFromUser(1722033500, terms, database, 1)
geocoding(database)
sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')

if __name__ == '__main__':
    pass