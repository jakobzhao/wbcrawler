# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Nov 8, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

from shutil import copy
from utils import processTerm, getOpinionLeadersByCentrality,geocoding, sqlite2shp,createDB 
import os,sys

#Variables
topic = 'love'
term = 'love'
refresh = False
pages = 1
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
#--------------------------------------------------------------------------------------------------------
database = current_path + '/../data/' + term +'.db'

createDB(database, refresh)

processTerm(term, pages, database)

opinion_leaders = getOpinionLeadersByCentrality(4, database)
print opinion_leaders

num = len(opinion_leaders)
print "there are "+ str(num) + " opinion leaders."
geocoding(database)
sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')
print "all finished"

if __name__ == '__main__':
    pass