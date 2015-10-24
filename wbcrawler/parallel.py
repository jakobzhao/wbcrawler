# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock
import socket

from pymongo import MongoClient
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException

from wbcrawler.database import register, unregister
from wbcrawler.weibo import sina_login
from wbcrawler.parser import parse_repost, parse_path, parse_info
from wbcrawler.log import *
from wbcrawler.settings import *

start = datetime.datetime.now()
utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=FLOW_CONTROL_DAYS)
lock = Lock()


# calculate the sum of robots in each category
def create_robots(rr, pr, ir, project, address="localhost", port=27017):
    num_of_robots = rr + pr + ir
    robots = []
    for robot_id in range(0, num_of_robots):
        if robot_id < rr:  # repost
            robots.append({'id': robot_id, 'project': project, 'count': rr, 'type': 'repost', 'account': register('local', address, port), 'address': address, 'port': port})
        elif robot_id in range(robot_id, rr + pr):  # path
            robots.append({'id': robot_id, 'project': project, 'count': pr, 'type': 'path', 'account': register('local', address, port), 'address': address, 'port': port})
        elif robot_id >= rr + pr:  # indo
            robots.append({'id': robot_id, 'project': project, 'count': ir, 'type': 'info', 'account': register('local', address, port), 'address': address, 'port': port})
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
    address = rbt['address']
    port = rbt['port']
    project = rbt['project']
    rr = rbt['count']
    client = MongoClient(address, port)
    db = client[project]
    with lock:
        browser = sina_login(rbt['account'])
    try:
        round_start = datetime.datetime.now()
        count = db.posts.find({"timestamp": {"$gt": utc_now}, "fwd_count": {"$gt": MIN_FWD_COUNT}}).count()
        slc = count / rr
        posts = db.posts.find({"timestamp": {"$gt": utc_now}, "fwd_count": {"$gt": MIN_FWD_COUNT}}).skip(slc * rbt['id']).limit(slc)
        parse_repost(db, browser, posts)
        log(NOTICE, "Time per round: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
    except KeyboardInterrupt:
        log(ERROR, "prorgam is interrupted.", "repost_crawling")
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60))


def info_crawling(rbt):
    address = rbt['address']
    port = rbt['port']
    project = rbt['project']
    ir = rbt['count']
    client = MongoClient(address, port)
    db = client[project]
    browser = sina_login(rbt['account'])
    try:
        round_start = datetime.datetime.now()
        count = db.users.find({'latlng': [0, 0]}).count()
        slc = count / ir
        users = db.users.find({'latlng': [0, 0]}).skip(slc * rbt['id']).limit(slc)
        parse_info(db, browser, users)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
    except KeyboardInterrupt:
        log(ERROR, "Program is interrupted.", 'info_crawling')
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        log(NOTICE, "Time: %d min(s)." % int((datetime.datetime.now() - start).seconds / 60))


def path_crawling(rbt):
    address = rbt['address']
    port = rbt['port']
    project = rbt['project']
    pr = rbt['count']
    client = MongoClient(address, port)
    db = client[project]
    browser = sina_login(rbt['account'])
    try:
        round_start = datetime.datetime.now()
        count = db.users.find({'path': []}).count()
        slc = count / pr
        users = db.users.find({'path': []}).skip(slc * rbt['id']).limit(slc)
        parse_path(db, browser, users)
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60))
        #   i += 1
    except KeyboardInterrupt:
        log(ERROR, "Program is interrupted.", 'path_crawling')
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        log(NOTICE, "Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60))


def parallel_crawling(rr, pr, ir, project="local", address="localhost", port=27017):
    # Make the Pool of workers
    pool = ThreadPool(rr + pr + ir)
    robots = create_robots(rr, pr, ir, project, address, port)
    # Open the urls in their own threads
    # and return the results
    try:
        pool.map(crawling_job, robots)
    except NameError, e:
        log(FATALITY, 'NameError: ' + e.message, 'parallel_crawlling')
    except OSError, e:
        log(FATALITY, 'OSError: ' + e.message, 'parallel_crawlling')
    except TypeError, e:
        log(FATALITY, e.message, 'parallel_crawlling') # AttributeError: 'str' object has no attribute 'device_iden'
    except StaleElementReferenceException:
        log(FATALITY, "StateElementReferenceException: Too many robots", 'parallel_crawlling')
    except TimeoutException:
        log(FATALITY, "TimeoutException: Too many robots", 'parallel_crawlling')
    except socket.error:
        log(FATALITY, "SocketError: The browser is forced to close", 'parallel_crawlling')
    except WindowsError, e:
        # [Error 32] The process cannot access the file because it is being used by another process:
        # 'c:\\users\\bo\\appdata\\local\\temp\\tmphrg3yv.webdriver.xpi\\resource\\modules\\web-element-cache.js'
        print e.message, str(e)
        log(FATALITY, "WindowsError: The browser is forced to close", 'parallel_crawlling')
    except WebDriverException:
        log(FATALITY, "WebDriverError: The browser is forced to close.", 'parallel_crawlling')
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
