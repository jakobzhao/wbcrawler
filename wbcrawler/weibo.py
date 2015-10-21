# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import time
import platform

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
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
            log(WARNING, 'timeout', 'get_response_as_human')
    return response_data


def sina_login(account):
    username = account[0]
    password = account[1]
    id = account[2]
    # chromedriver = CHROME_PATH
    # os.environ["webdr.chrome.driver"] = chromedriver
    # browser = webdriver.Chrome(chromedriver)
    if "Linux" in platform.platform():
        display = Display(visible=0, size=(1024, 768))
        display.start()
    browser = webdriver.Firefox()
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
                log(FATALITY, 'Wrong input, please wait and have another try.')
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

    log(NOTICE, 'ROBOT %d has logged in.' % id)

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
