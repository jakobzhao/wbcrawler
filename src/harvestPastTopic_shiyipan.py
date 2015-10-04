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
from utils import processTerm, getOpinionLeadersByCentrality, searchTermsFromUser,geocoding, sqlite2shp, createDB


topic = 'panshiyi'
terms = ['pm2.5', '空气质量', 'pm10', '空气污染']

refresh = False
current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
database = current_path + '/../data/' + topic +'.db'
#--------------------------------------------------------------------------------------------------------

createDB(database, refresh)
searchTermsFromUser(1182391231, terms, database, 31)

geocoding(database)
sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')

if __name__ == '__main__':
    pass
