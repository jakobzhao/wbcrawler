# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import platform
from pymongo import MongoClient, DESCENDING
from utils import get_response_as_human
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from settings import TIMEOUT
from log import *


def register(settings):
    TIMEOUT = 20
    if 'remote' not in settings.keys():
        client = MongoClient(settings['address'], settings['port'])
        robot_table = settings['robot_table']
    else:
        client = MongoClient(settings['remote']['address'], settings['remote']['port'])
        robot_table = settings['remote']['robot_table']

    # get a Robot from the database
    if client.local[robot_table].find({"inused": False}).count() == 0:
        occupied_msg = "All Robots are occupied, please try again later."
        log(FATALITY, occupied_msg)
        exit(-1)

    account_raw = client.local[robot_table].find({"inused": False, 'id': {'$ne': 999}}).limit(1)[0]
    log(NOTICE, 'ROBOT %d is registering...' % account_raw['id'])

    # sign in the robot
    account = [account_raw['username'], account_raw['password'], account_raw['id']]
    username = account[0]
    password = account[1]
    id = account[2]

    if "Linux" in platform.platform():
        display = Display(visible=0, size=(1024, 768))
        display.start()

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    browser = webdriver.Firefox(firefox_profile=firefox_profile)

    # browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    browser.set_window_size(960, 1050)
    browser.set_window_position(0, 0)

    browser.set_page_load_timeout(TIMEOUT)
    browser.set_script_timeout(TIMEOUT)
    # visit the sina login page
    login_url = "https://login.sina.com.cn/"
    browser.get(login_url)

    # input username
    # user = browser.find_element_by_id('username')
    user = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'username')))
    user.clear()
    user.send_keys(username, Keys.ARROW_DOWN)

    # input the passowrd
    passwd = browser.find_element_by_id('password')
    passwd.clear()
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # press click and then the vcode appears.
    browser.find_element_by_class_name('smb_btn').click()
    time.sleep(10)
    # run = True
    # # a = browser.find_element_by_partial_link_text('完善资料').text
    # while run:
    #     time.sleep(5)
    #     try:
    #         a = browser.find_element_by_partial_link_text('完善资料').text
    #         if a == '完善资料':
    #             run = False
    #     except:
    #         log(NOTICE, "trying ...")

    # if a == '完善资料'
    # else:
    #     time.sleep(5)
    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '完善资料')))

    # weibo_tab_xpath = '//*[@id="service_list"]/div[2]/ul/li[1]/a'
    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, weibo_tab_xpath)))

    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, weibo_tab_xpath)))
    # # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    # weibo_tab = browser.find_element_by_xpath(weibo_tab_xpath)
    # weibo_tab.send_keys(Keys.CONTROL + Keys.RETURN)
    #
    # WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    #
    # browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    # browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    # Examing the validity of the account
    test_urls = ['http://s.weibo.com/weibo/love', 'http://weibo.com/1642592432/D0EwmhebV?type=repost']
    passed = False

    rd = get_response_as_human(browser, test_urls[0], page_reload=True, waiting=3)
    soup = BeautifulSoup(rd, 'html5lib')

    if soup.find('div', {'node-type': 'feed_list_page_morelist'}) is None:
        log(NOTICE, 'ROBOT %d has not logged in.' % id)
        browser.close()
        # db.accounts.update({'username': username}, {'$set': {"inused": False}})
        return {}
    else:
        log(NOTICE, "ROBOT %d successfully passes Test One..." % id)
        passed = True

    # get_response_as_human(browser, test_urls[1])
    # if "weibo.com/login.php" in browser.current_url:
    #     passed = False
    #     log(NOTICE, 'ROBOT %d has not logged in.' % id)
    #     browser.close()
    #     db.accounts.update({'username': username}, {'$set': {"inused": None}})
    #     return {}
    # else:
    #     log(NOTICE, "ROBOT %d successfully passes Test Two..." % id)
    #     passed = True

    if passed:
        log(NOTICE, 'ROBOT %d has logged in.' % id)
        client.local[robot_table].update({'username': username}, {'$set': {"inused": True}})
        return {'browser': browser, 'account': account, 'settings': settings}


def unregister(robot):
    # {'$set': {'inused': false}}
    browser = robot['browser']
    try:
        robot['browser'].close()
    except:
        browser.close()
    settings = robot['settings']
    account = robot['account']

    if 'remote' not in settings.keys():
        client = MongoClient(settings['address'], settings['port'])
        robot_table = settings['robot_table']
    else:
        client = MongoClient(settings['remote']['address'], settings['remote']['port'])
        robot_table = settings['remote']['robot_table']

    client.local[robot_table].update({'username': account[0]}, {'$set': {"inused": False}})
    log(NOTICE, 'ROBOT %d has successfully unregistered.' % account[2])

    robot.clear()
    del robot
    return True


def create_database(settings, fresh=False):
    client = MongoClient(settings['address'], settings['port'])
    # client.the_database.authenticate()
    # client.the_database.authenticate('bo', 'f', source="C:\MongoDB\data")
    # client = MongoClient('mongodb://bo:f@localhost:27017')
    # db.add_user('bo','f')
    # from the address level, I have to define the url by myself. seems we cannot reply on pyton
    # from the database level, what we can do? And how to do that?
    db = client[settings['project']]
    posts = db.posts
    users = db.users

    if fresh:
        db.posts.delete_many({})
        db.users.delete_many({})

    try:
        posts.create_index([("mid", DESCENDING)], unique=True, sparse=True)
        users.create_index([("userid", DESCENDING)], unique=True)
        posts.delete_many({"mid": None})
    except:
        pass
    return db


def unlock_robots(settings):
    if 'remote' not in settings.keys():
        client = MongoClient(settings['address'], settings['port'])
        robot_table = settings['robot_table']
    else:
        client = MongoClient(settings['remote']['address'], settings['remote']['port'])
        robot_table = settings['remote']['robot_table']

    client.local[robot_table].update_many({'inused': True}, {'$set': {'inused': False}})
    client[settings['project']].posts.delete_many({"mid": None})
    log(NOTICE, "All the robots have been unlocked.")
