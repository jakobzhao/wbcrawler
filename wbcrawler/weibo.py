# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient, DESCENDING

from PIL import Image, ImageDraw

from utils import get_interval_as_human
from settings import TIMEOUT
from log import *


def get_response_as_human(browser, url, page_reload=True):
    url_raw = url
    response_data = ''
    waiting = get_interval_as_human()
    if page_reload:
        while True:
            try:
                browser.get(url_raw)
                time.sleep(waiting)
                response_data = browser.page_source
                if response_data != {}:
                    break
            except TimeoutException:
                url_raw = browser.current_url
                log(NOTICE, 'Web page refreshing')
    else:
        try:
            browser.get(url_raw)
            time.sleep(waiting)
        except TimeoutException:
            log(NOTICE, 'a timeout warning.')
    return response_data


def register(project, address, port):
    client = MongoClient(address, port)
    db = client[project]

    if db.accounts.find({"inused": False}).count() == 0:
        occupied_msg = "All the accounts are occupied, please try again later."
        log(FATALITY, occupied_msg)
        exit(-1)

    account_raw = db.accounts.find({"inused": False}).limit(1)[0]
    account = [account_raw['username'], account_raw['password'], account_raw['id']]

    db.accounts.update({'username': account_raw['username']}, {'$set': {"inused": True}})
    print 'ROBOT %d has registered.' % account_raw['id']

    return account


def unregister(project, address, port, account):
    # {'$set': {'inused': false}}
    client = MongoClient(address, port)
    db = client[project]
    db.accounts.update({'username': account[0]}, {'$set': {"inused": False}})
    log(NOTICE, 'ROBOT %d has successfully unregistered.' % account[2])
    return True


def create_database(project, address, port, fresh=False):
    client = MongoClient(address, port)
    db = client[project]
    posts = db.posts
    users = db.users

    if fresh:
        db.posts.delete_many({})
        db.users.delete_many({})

    posts.create_index([("mid", DESCENDING)], unique=True)
    users.create_index([("userid", DESCENDING)], unique=True)
    return db


def sina_login(account):
    username = account[0]
    password = account[1]
    id = account[2]
    username = 'vfbkkh154@126.com'
    password = 'nanjing1212'
    # chromedriver = CHROME_PATH
    # os.environ["webdr.chrome.driver"] = chromedriver
    # browser = webdriver.Chrome(chromedriver)

    browser = webdriver.Firefox()
    browser.set_window_size(960, 1060)
    browser.set_window_position(0, 0)
    browser.set_page_load_timeout(TIMEOUT)
    browser.set_script_timeout(TIMEOUT)

    # visit the sina login page
    login_url = "https://login.sina.com.cn/"
    browser.get(login_url)

    # input username
    # user = browser.find_element_by_id('username')
    user = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'username')))
    user.send_keys(username, Keys.ARROW_DOWN)

    # input the passowrd
    passwd = browser.find_element_by_id('password')
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # press click and then the vcode appears.
    browser.find_element_by_class_name('smb_btn').click()
    if browser.find_element_by_id('door').location != {'y': 0, 'x': 0}:
        vcode = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'door')))
        time.sleep(2)
        t = str(datetime.datetime.now(TZCHINA).time()).split(".")[0].replace(':', '-')
        filename = '../../data/%s-%s.png' % (username, t)
        browser.save_screenshot(filename)
        get_vpic(filename)

        # code = raw_input("v code:")

        while vcode:
            code = get_vcode_from_pushbullet(filename, "ROBOT %d" % id)
            if code:
                vcode.send_keys(code, Keys.ARROW_DOWN)
            browser.find_element_by_class_name('smb_btn').click()
            time.sleep(3)

            if browser.current_url == login_url:
                vcode.clear()
                code = ''
                print "Please try again."
                pb.push_note("Lord,", "Wrong input, please wait and have another try.")
                t = str(datetime.datetime.now(TZCHINA).time()).split(".")[0].replace(':', '-')
                filename = '../../data/%s-%s.png' % (username, t)
                browser.save_screenshot(filename)
                get_vpic(filename)
                # code = get_vcode_from_pushbullet(filename, "ROBOT %d" % id)
            else:
                break

    weibo_tab_xpath = '//*[@id="service_list"]/div[2]/ul/li[1]/a'

    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, weibo_tab_xpath)))
    weibo_tab = browser.find_element_by_xpath(weibo_tab_xpath)
    weibo_tab.send_keys(Keys.CONTROL + Keys.RETURN)

    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    print 'ROBOT %d has logged in.' % id
    # pb.push_note("Lord,", 'Robot %s is working!' % id)

    return browser


def get_vpic(filename):
    im = Image.open(filename)
    im_c = im.crop((740, 263, 840, 303))
    im_c.save(filename)
    return im_c


def get_vcode_from_pushbullet(filename, marker):
    img = Image.open(filename)
    img = img.resize((200, 80), resample=1)
    draw = ImageDraw.Draw(img)
    draw.text([3, 3], marker, fill=(60, 60, 60))
    img.save(filename)

    with open(filename, "rb") as vpic:
        file_data = pb.upload_file(vpic, file_name=filename)
    pb.push_file(**file_data)
    # os.remove(filename)
    latest = {}
    stop = False
    while True:
        code = ""
        time.sleep(15)
        pushes = pb.get_pushes()[1][0:30]
        for p in pushes:
            if 'body' in p.keys():
                if p['body'].split(" ")[0] == marker.split(" ")[1]:
                    code = p['body'].split(" ")[1]
                    stop = True
                    break
        if stop:
            break
            # verifying the vcode.
            # latest = pb.get_pushes()[1][0]
            # if latest['type'] == u"note":
            #     break
    # p = pb.get_pushes()
    # for i in p:
    #     ident=i.get("iden")
    #     try:
    #         pb.dismiss_push(ident)
    #         pb.delete_push(ident)
    #     except:
    #         pass
    return code
