# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: The Ohio State University
'''

from multiprocessing.dummy import Pool as ThreadPool

from src.utils import *
from settings import *

num_of_robots = 8
robots = []
r_sum, i_sum, p_sum = 0, 0, 0
project = 'five'
start = datetime.datetime.now()
utc_now = datetime.datetime.utcnow() - datetime.timedelta(days=FLOW_CONTROL_DAYS)

db = create_database(project, address, port, fresh)

# calculate the sum of robots in each category
for robot_id in range(0, num_of_robots):
    # repost
    if robot_id % num_of_robots in range(0, 2):

        robots.append({'id': r_sum + 1, 'type': 'repost', 'account': register('local', address, port)})
        r_sum += 1
    # info
    elif robot_id % num_of_robots in range(3, 6):
        robots.append({'id': i_sum + 1, 'type': 'info', 'account': register('local', address, port)})
        i_sum += 1
    # path
    else:
        robots.append({'id': p_sum + 1, 'type': 'path', 'account': register('local', address, port)})
        p_sum += 1


def crawling_job(robot):
    time.sleep(robot['id'] * 15)
    if robot['type'] == 'repost':
        repost_crawling(robot)
    elif robot['type'] == 'info':
        info_crawling(robot)
    else:
        path_crawling(robot)


def repost_crawling(rbt):
    browser = sina_login(rbt['account'])
    try:
        round_start = datetime.datetime.now()
        count = db.posts.find({"timestamp": {"$gt": utc_now}, "fwd_count": {"$gt": 0}}).count()
        slc = count / r_sum
        posts = db.posts.find({"timestamp": {"$gt": utc_now}, "fwd_count": {"$gt": 0}}).skip(slc * (rbt['id'] - 1)).limit(slc)
        parse_repost(db, browser, posts)
        print "Time per round: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60)
    except:
        print "prorgam is interrupted."
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        print "Cost Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60)


def info_crawling(rbt):
    browser = sina_login(rbt['account'])
    try:
        round_start = datetime.datetime.now()
        count = db.users.find({'$or': [{'latlng': [0, 0]}, {'path': [0, 0, 0]}]}).count()
        slc = count / i_sum
        users = db.users.find({'$or': [{'latlng': [0, 0]}, {'path': [0, 0, 0]}]}).skip(slc * (rbt['id'] - 1)).limit(slc)
        parse_info(db, browser, users)
        print "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60)
    except:
        print "Program is interrupted."
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        print "Time: %d min(s)." % int((datetime.datetime.now() - start).seconds / 60)


def path_crawling(rbt):
    browser = sina_login(rbt['account'])
    try:
        # i = 0
        # while True:
        round_start = datetime.datetime.now()
        count = db.users.find({'$and': [{'latlng': [0, 0]}, {'path': []}]}).count()
        slc = count / p_sum
        users = db.users.find({'$and': [{'latlng': [0, 0]}, {'path': []}]}).skip(slc * (rbt['id'] - 1)).limit(slc)
        parse_path(db, browser, users)
        print "Time: %d mins." % int((datetime.datetime.now() - round_start).seconds / 60)
        #   i += 1
    except:
        print "Program is interrupted."
    finally:
        browser.close()
        unregister('local', address, port, rbt['account'])
        print "Cost Time: %d mins." % int((datetime.datetime.now() - start).seconds / 60)


def main():
    # Make the Pool of workers
    pool = ThreadPool(num_of_robots)
    # Open the urls in their own threads
    # and return the results
    pool.map(crawling_job, robots)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
