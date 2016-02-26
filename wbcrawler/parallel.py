# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import sys
from multiprocessing.dummy import Pool as ThreadPool
# from multiprocessing.dummy import Lock
import socket

from pymongo import MongoClient, DESCENDING, ASCENDING
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException

from wbcrawler.robot import register, unregister
from wbcrawler.parser import parse_repost, parse_path, parse_info
from wbcrawler.log import *
from wbcrawler.settings import UTC
from httplib import BadStatusLine
from urllib2 import URLError

reload(sys)
sys.setdefaultencoding('utf-8')
start = datetime.datetime.now()


# lock = Lock()


# calculate the sum of robots in each category
def create_robots(rr, pr, ir, settings):
    num_of_robots = rr + pr + ir
    robots = []

    for robot_id in range(0, num_of_robots):
        robot = {}

        for i in range(robot_id, num_of_robots):
            if robot == {}:
                # with lock:
                robot = register(settings)
            else:
                break

        if robot != {}:
            if robot_id < rr:  # repost
                robot['type'] = 'repost'
                robots.append(robot)
            elif robot_id in range(rr, rr + pr):  # path
                robot['type'] = 'path'
                robots.append(robot)
            elif robot_id >= rr + pr:  # info
                robot['type'] = 'info'
                robots.append(robot)

    nrr, npr, nir = 0, 0, 0

    for robot in robots:
        if robot['type'] == 'repost':
            robot['id'] = nrr
            nrr += 1
        elif robot['type'] == 'path':
            robot['id'] = npr
            npr += 1
        elif robot['type'] == 'info':
            robot['id'] = nir
            nir += 1

    for robot in robots:
        if robot['type'] == 'repost':
            robot['count'] = nrr
        elif robot['type'] == 'path':
            robot['count'] = npr
        elif robot['type'] == 'info':
            robot['count'] = nir

    return robots


def crawling_job(robot):
    if robot['type'] == 'repost':
        repost_crawling(robot)
    elif robot['type'] == 'path':
        path_crawling(robot)
    elif robot['type'] == 'info':
        info_crawling(robot)
    else:
        pass


def repost_crawling(rbt):
    utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=rbt['settings']['replies_control_days'])

    rr = rbt['count']
    client = MongoClient(rbt['settings']['address'], rbt['settings']['port'])
    db = client[rbt['settings']['project']]
    try:
        round_start = datetime.datetime.now()
        utc_end = datetime.datetime(2015, 10, 29, 0, 0, 0, 0, tzinfo=UTC)
        # search_json = {"timestamp": {"$gt": utc_now}, "timestamp": {"$lt": utc_end}, 'keyword': {'$ne': '五中全会'}, "fwd_count": {"$gt": rbt['settings']['min_fwd_times']}, "deleted": {"$eq": None}}
        # search_json = {"timestamp": {"$gt": utc_now}, {"$and": ["fwd_count": {"$gt": rbt['settings']['min_fwd_times']}, "fwd_count": {"$gt": 200000}]}, "deleted": {"$eq": None}}
        search_json = {"timestamp": {"$gt": utc_end}, '$and': [{"fwd_count": {"$gt": 99}}, {"fwd_count": {"$lt": 100000000}}], "replies": {"$eq": []}, "deleted": {"$eq": None}}
        # search_json = {"keyword": u'新型城镇化', "fwd_count": {"$gt": rbt['settings']['min_fwd_times']}}
        count = db.posts.find(search_json).count()
        slc = count / rr

        posts = db.posts.find(search_json).skip(slc * rbt['id']).limit(slc)  # .sort({'fwd_count': -1}). .sort([('mid', DESCENDING), ('fwd_count', ASCENDING)])
        parse_repost(posts, rbt, db)
        log(NOTICE, "Time per round: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
    except KeyboardInterrupt:
        log(ERROR, "prorgam is interrupted.", "repost_crawling")
    finally:
        unregister(rbt)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60))


def path_crawling(rbt):
    # utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=rbt['settings']['replies_control_days'])
    pr = rbt['count']
    client = MongoClient(rbt['settings']['address'], rbt['settings']['port'])
    db = client[rbt['settings']['project']]
    try:
        round_start = datetime.datetime.now()
        # search_json = {'latlng': [0, 0]}
        # search_json = {}
        search_json = {'path': []}
        count = db.users.find(search_json).count()
        slc = count / pr
        users = db.users.find(search_json).skip(slc * rbt['id']).limit(slc)
        parse_path(users, rbt, db)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
    except KeyboardInterrupt:
        log(ERROR, "Program is interrupted.", 'path_crawling')
    finally:
        unregister(rbt)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60))


def info_crawling(rbt):
    ir = rbt['count']
    client = MongoClient(rbt['settings']['address'], rbt['settings']['port'])
    db = client[rbt['settings']['project']]
    try:
        round_start = datetime.datetime.now()
        search_json = {'$or': [{'latlng': [0, 0]}, {'latlng': [-1, -1]}]}
        # search_json = {'latlng': [0, 0]}
        # search_json = {'msg': {'$exists': False}}
        count = db.users.find(search_json).count()
        slc = count / ir
        users = db.users.find(search_json).skip(slc * rbt['id']).limit(slc)
        parse_info(users, rbt, db)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
    except KeyboardInterrupt:
        log(ERROR, "Program is interrupted.", 'info_crawling')
    finally:
        unregister(rbt)
        log(NOTICE, "Time: %d min(s)." % int((datetime.datetime.now() - start).seconds / 60))


def parallel_crawling(rr, pr, ir, settings):
    # Make the Pool of workers
    pool = ThreadPool(rr + pr + ir)

    # Open the urls in their own threads
    # and return the results
    try:
        robots = create_robots(rr, pr, ir, settings)
        pool.map(crawling_job, robots)
    except NameError, e:
        log(FATALITY, 'NameError: ' + e.message, 'parallel_crawlling')
    except OSError, e:
        log(FATALITY, 'OSError: ' + e.message, 'parallel_crawlling')
    except TypeError, e:
        log(FATALITY, e.message, 'parallel_crawlling')  # AttributeError: 'str' object has no attribute 'device_iden'
    except StaleElementReferenceException:
        log(FATALITY, "StateElementReferenceException: Too many robots", 'parallel_crawlling')
    except TimeoutException:
        log(FATALITY, "TimeoutException: Too many robots", 'parallel_crawlling')
    except socket.error:
        log(FATALITY, "SocketError: The browser is forced to close", 'parallel_crawlling')
    except URLError, e:
        log(FATALITY, "urllib2.URLError", 'parallel_crawlling')
    except ValueError, e:
        log(FATALITY, "ValueError: could not convert string to float", 'parallel_crawlling')
    except IndexError, e:
        log(FATALITY, "IndexError: List index out of range", 'parallel_crawlling')
    # except WindowsError, e:
    #     # [Error 32] The process cannot access the file because it is being used by another process:
    #     # 'c:\\users\\bo\\appdata\\local\\temp\\tmphrg3yv.webdriver.xpi\\resource\\modules\\web-element-cache.js'
    #     print e.message, str(e)
    #     log(FATALITY, "WindowsError: The browser is forced to close", 'parallel_crawlling')
    except WebDriverException:
        log(FATALITY, "WebDriverError: The browser is forced to close.", 'parallel_crawlling')
    # close the pool and wait for the work to finish
    except BadStatusLine, e:
        log(FATALITY, "BadStatusline: The browser is forced to close." + e.message, 'parallel_crawlling')

    pool.close()
    pool.join()
    return
