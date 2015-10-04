# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Dec 18, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''
from pygeocoder import Geocoder
import time


s = '8600 N. High St Columbus, OH 43235'
coordinates = Geocoder.geocode(s)
time.sleep(1)
   
print str(coordinates)