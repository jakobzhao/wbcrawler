# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School


SETTINGS = {
    'project': 'insurance',
    'pis': ['jakobzhao@gmail.com', 'pku_fenglin@163.com'],
    'robot_table': 'accounts',
    'address': '192.168.1.10',
    'port': 27017,
    'robot_num': 15,
    'keywords': ['社保', '商业保险', '社会保险', '医疗保险', '医保', '医院%20报销'],
    'control_days': 370,
    'replies_control_days': 370,
    'min_fwd_times': 5,
    'remote': {'address': 'localhost', 'port': 27017, 'robot_table': 'accounts'}
}
