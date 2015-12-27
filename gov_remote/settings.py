# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

SETTINGS = {
    'project': 'gov',
    'pis': ['jakobzhao@gmail.com'],
    'robot_table': 'accounts',
    'address': '192.168.1.11',
    'port': 27017,
    'robot_num': 1,
    'keywords': ['镇政府', '街道办', '村委会', '居委会'],
    'control_days': 10,
    'replies_control_days': 10,
    'min_fwd_times': 20,
    'remote': {'address': 'localhost', 'port': 27017, 'robot_table': 'accounts'}
}

#     'remote': {'address': 'localhost', 'port': 27017, 'robot_table': 'accounts'}
#   'keywords': ['中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会'],
