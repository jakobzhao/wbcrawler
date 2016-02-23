# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


from random import randint
import time
from selenium.common.exceptions import TimeoutException
from log import *


# hanzi to pinyin
# def to_pinyin(keyword):
#     from pypinyin import lazy_pinyin
#     py = lazy_pinyin(unicode(keyword))
#     result = ''
#     for i in py:
#         result += i
#     return result


def get_interval_as_human(low=18, high=22):
    return randint(low, high)


def get_response_as_human(browser, url, page_reload=True, waiting=-1):
    url_raw = url
    response_data = ''
    if waiting == -1:
        waiting = get_interval_as_human()
    if page_reload:
        while True:
            try:
                time.sleep(waiting)
                browser.get(url_raw)
                response_data = browser.page_source
                if response_data != {}:
                    break
            except TimeoutException:
                url_raw = browser.current_url
                log(NOTICE, 'Web page refreshing')
    else:
        try:
            time.sleep(waiting)
            browser.get(url_raw)
            response_data = browser.page_source
        except TimeoutException:
            log(WARNING, 'timeout', 'get_response_as_human')
    return response_data


def get_response_to_end_as_human(browser, url, page_reload=True, waiting=-1):
    from selenium.webdriver.common.keys import Keys
    url_raw = url
    response_data = ''
    if waiting == -1:
        waiting = get_interval_as_human()
        waiting = 7
    if page_reload:
        while True:
            try:
                browser.get(url_raw)
                body = browser.find_element_by_tag_name('body')

                time.sleep(waiting)
                body.send_keys(Keys.END)
                time.sleep(waiting)
                body.send_keys(Keys.END)
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
            body = browser.find_element_by_tag_name('body')

            time.sleep(waiting)
            body.send_keys(Keys.END)
            time.sleep(waiting)
            body.send_keys(Keys.END)
            time.sleep(waiting)

            response_data = browser.page_source
        except TimeoutException:
            log(WARNING, 'timeout', 'get_response_as_human')
    return response_data
