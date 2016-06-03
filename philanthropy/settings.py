# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on May 16, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

SETTINGS = {
    'project': 'philanthropy',
    'pis': ['bo_zhao@hks.harvard.edu'],
    'robot_table': 'accounts',
    'address': '127.0.0.1',
    'port': 27017,
    'robot_num': 5,
    'keywords': [
        '捐赠 元',
        '捐赠 亿元～万元',
        '捐赠 元 小学～中学～大学～学校～学院～班',
        '捐赠 元 集团～有限公司～基金会～有限责任公司',
        '捐赠 元 省～市～政府',
        '捐赠 元 总经理～董事长'],
    'control_days': 60,
    'replies_control_days': 60,
    'min_fwd_times': 2
}
