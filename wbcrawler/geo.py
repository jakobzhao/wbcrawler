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
def estimate_location(user):
    db.
    path
    pass
