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
def to_pinyin(keyword):
    from pypinyin import lazy_pinyin
    py = lazy_pinyin(unicode(keyword))
    result = ''
    for i in py:
        result += i
    return result


def get_interval_as_human(low=18, high=22):
    return randint(low, high)


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


def get_name_from_content(content):
    names = []
    if u'@' not in content:
        return names

    parts = content.split(u"@")

    for part in parts[1:]:
        comma_index = -1
        if u':' in part or u'：' in part:
            if part.find(u':') == -1:
                comma_index = part.find(u'：')
            elif part.find(u'：') == -1:
                comma_index = part.find(u':')
            else:
                if part.find(u':') > part.find(u'：'):
                    comma_index = part.find(u'：')
                else:
                    comma_index = part.find(u':')

        space_index = part.find(u' ')
        if part == parts[-1] and space_index == -1:
            space_index = len(part)

        if comma_index == -1 and space_index == -1:
            name = u'@' + part
        elif comma_index == -1 and space_index != -1:
            name = u'@' + part[:space_index]
        elif comma_index != -1 and space_index == -1:
            name = u'@' + part[:comma_index]
        elif comma_index < space_index:
            name = u'@' + part[:comma_index]
        elif comma_index > space_index:
            name = u'@' + part[:space_index]
        else:
            name = u'@' + part
        names.append(name)

    return names
