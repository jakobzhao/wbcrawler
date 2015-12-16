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
    'address': 'localhost',
    'port': 27017,
               'robot_num': 1,
    'keywords': ['中央政府', '地方政府', '省政府', '市政府', '县政府', '区政府', '乡政府', '镇政府', '街道办', '村委会', '居委会'],
               'control_days': 900,
    'replies_control_days': 20,
    'min_fwd_times': 20
           },

SETTINGS2 = {
    'project': 'gov',
    'pis': ['jakobzhao@gmail.com'],
    'robot_table': 'accounts',
    'address': 'localhost',
    'port': 27017,
    'robot_num': 1,
    'keywords': ['居委会', '村委会', '街道办', '镇政府', '乡政府'],
    'control_days': 900,
    'replies_control_days': 20,
    'min_fwd_times': 20
}
