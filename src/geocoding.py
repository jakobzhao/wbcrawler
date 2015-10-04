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
from utils import geocoding, sqlite2shp


topic = 'shiyipan'

current_path = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
database = current_path + '/../data/' + topic +'.db'
#--------------------------------------------------------------------------------------------------------
geocoding(database)
sqlite2shp(database, current_path + '/../data/shapefiles/' + topic + '.shp')
if __name__ == '__main__':
    pass