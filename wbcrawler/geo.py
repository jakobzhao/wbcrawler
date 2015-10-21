# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import urllib2
import json
import sys

from settings import BAIDU_AK
from log import *

reload(sys)
sys.setdefaultencoding('utf-8')


def geocode(loc):
    lat, lng = -1, -1
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' % (loc, BAIDU_AK)
    response = urllib2.urlopen(url.replace(' ', '%20'))
    try:
        loc_json = json.loads(response.read())
        lat = loc_json[u'result'][u'location'][u'lat']
        lng = loc_json[u'result'][u'location'][u'lng']
    except ValueError:
        log(ERROR, "No JSON object was decoded", 'geocode')
    except KeyError, e:
        log(ERROR, e.message, 'geocode')
    return [lat, lng]


# Estimate where a post was sent.
def estimate_location_by_path(user):
    est_latlng = [0, 0]
    path = user['path']
    latlng = user['latlng']
    if user['path'] != [] and user['path'] != [[0, 0, 0]]:

        if latlng != [0, 0] or latlng != [-1, -1]:
            path.append(latlng)
        avg_lat = 0
        avg_lng = 0
        for latlng in path:
            avg_lat += latlng[0]
            avg_lng += latlng[1]
        avg_lat = avg_lat / (1.0 * len(path))
        avg_lng = avg_lng / (1.0 * len(path))
        distances = []
        for latlng in path:
            distances.append(abs(latlng[0] - avg_lat) + abs(latlng[1] - avg_lng))
        est_latlng = path[distances.index(min(distances))][1:]
    elif user['path'] == [[0, 0, 0]]:
        est_latlng = latlng
    elif user['path'] == [] and latlng != [0, 0]:
        est_latlng = latlng[1:0]
    else:
        pass

    return est_latlng
