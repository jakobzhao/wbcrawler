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
from utils import processTerm, processTerms,getOpinionLeadersByCentrality,geocoding, sqlite2shp, createDB
import os,sys

#import socket
#socket.setdefaulttimeout(20)
#Variables
topic = 'px'
terms = ['px']

refresh = False
pages = 2
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
#--------------------------------------------------------------------------------------------------------
database = current_path + '/../data/' + topic +'.db'

createDB(database, refresh)
processTerms(terms, pages, database)

opinion_leaders = getOpinionLeadersByCentrality(4, database)
print opinion_leaders

num = len(opinion_leaders)
print "there are "+ str(num) + " opinion leaders."

geocoding(database)

sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')
if __name__ == '__main__':
    pass
