# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

import urllib2
import json

from settings import BAIDU_AK


def geocode(loc):
    lat, lng = 0, 0
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' % (loc, BAIDU_AK)
    response = urllib2.urlopen(url.replace(' ', '%20'))
    try:
        loc_json = json.loads(response.read())
        lat = loc_json[u'result'][u'location'][u'lat']
        lng = loc_json[u'result'][u'location'][u'lng']
    except ValueError, e:
        # print url
        print e.message + "No JSON object could be decoded"
    except KeyError, e:
        # print url
        print e.message
    return [lat, lng]


# estimate where the user would be while sending out the post
def estimate_location():
    pass
