# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

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
    if loc == u'其他' or loc == u'美国' or loc == u'英国':
        pass
    else:
        try:
            response = urllib2.urlopen(url.replace(' ', '%20'))
        except urllib2.HTTPError, e:
            log(WARNING, e, 'geocode')
        try:
            loc_json = json.loads(response.read())
            lat = loc_json[u'result'][u'location'][u'lat']
            lng = loc_json[u'result'][u'location'][u'lng']
        except ValueError:
            log(ERROR, "No JSON object was decoded", 'geocode')
        except KeyError, e:
            log(ERROR, e.message, 'geocode')
    return [lat, lng]


# Estimate where a post was sent out based on the semantics of the user's name,
# verified inforamtion, and/or other contextual information.
def geocode_by_semantics(project, address, port):
    from pymongo import MongoClient
    client = MongoClient(address, port)
    db = client[project]
    users = db.users.find({'$or': [{'latlng': [0, 0]}, {'latlng': [-1, -1]}], 'verified': True})
    count = db.users.find({'$or': [{'latlng': [0, 0]}, {'latlng': [-1, -1]}], 'verified': True}).count()
    print count
    i = 0
    for user in users:
        i += 1
        verified_info = user['verified_info']
        username = user['username']

        verified_info = verified_info.replace(u'主持人', '').replace(u'职员', '').replace(u'院长', '').replace(u'经理', '')
        verified_info = verified_info.split(u' ')[0]
        if verified_info == u'前' or u'www' in verified_info or u'律师' in verified_info or u'学者' in verified_info or u'作家' in verified_info or u'媒体人' in verified_info or u'诗人' in verified_info:
            verified_info = ''
        locational_info = verified_info
        if locational_info == '':
            locational_info = username
        if verified_info != '':
            latlng = geocode(verified_info)
        else:
            continue

        log(NOTICE, '#%d geocode the user by its semantic info %s. %d posts remain. latlng: %s ' % (i, verified_info.encode('gbk', 'ignore'), count - i, str(latlng)))

        if latlng[0] != -1:
            db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})

    log(NOTICE, "mission compeletes.")


def geocode_locational_info(project, address, port):
    from pymongo import MongoClient
    client = MongoClient(address, port)
    db = client[project]
    search_json = {'$or': [{'latlng': [0, 0]}, {'latlng': [-1, -1]}], 'location': {'$ne': ''}}
    users = db.users.find(search_json)
    count = users.count()
    print count
    i = 0
    for user in users:
        i += 1
        latlng = geocode(user['location'])

        log(NOTICE, '#%d geocode the user by its locational info %s. %d posts remain. latlng: %s ' % (i, user['location'].encode('gbk', 'ignore'), count - i, str(latlng)))

        if latlng[0] != -1:
            db.users.update({'userid': user['userid']}, {'$set': {'latlng': latlng}})

    log(NOTICE, "mission compeletes.")


# Estimate where a post was sent out based the path of its author.
def estimate_location_by_path(user):
    est_latlng = [0, 0]
    path = user['path']
    latlng = user['latlng']
    if user['path'] != [] and user['path'][0][0] != 0:

        if latlng != [0, 0] or latlng != [-1, -1]:
            path.append(latlng)
        avg_lat = 0
        avg_lng = 0
        for latlng in path:
            avg_lat += latlng[0]
            avg_lng += latlng[1]

        avg_lat /= float(len(path))
        avg_lng /= float(len(path))
        distances = []
        for latlng in path:
            distances.append(abs(latlng[0] - avg_lat) + abs(latlng[1] - avg_lng))
        est_latlng = path[distances.index(min(distances))][0:2]
    elif user['path'] == [] and latlng != [0, 0]:
        est_latlng = latlng
    else:
        pass

    return est_latlng


# Estimate where a post was sent out by the locational information of its author.
def georeference(project, address, port):
    from pymongo import MongoClient
    client = MongoClient(address, port)
    db = client[project]
    posts = db.posts.find()
    count = db.posts.find().count()
    i = 0
    for post in posts:
        userid = post['user']['userid']
        user = db.users.find_one({'userid': userid})
        i += 1
        if abs(user['latlng'][0] - 0) < 0.001 or abs(user['latlng'][0] + 1) < 0.001:
            pass
        else:
            try:
                db.posts.update({'mid': post['mid']}, {'$set': {
                    'latlng': user['latlng']
                }
                })
                log(NOTICE, 'georeferencing #%d, %d posts remain. latlng: %s ' % (i, count - i, str(user['latlng'])))
            except:
                log(NOTICE, 'the user latlng does not exit')

    log(NOTICE, "mission compeletes.")
