# !/usr/bin/python  
# -*- coding: utf-8 -*-
'''
Created on Oct 16, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

from utils import current_path, uploadToDropbox

uploadToDropbox(current_path + '/../data/pm2.5.db', 'pm2.5.db')
uploadToDropbox(current_path + '/../data/xilaibo.db', 'xilaibo.db')
#uploadToDropbox(current_path + '/../data/ningbo.db', 'ningbo.db')
#uploadToDropbox(current_path + '/../data/18ccp.db', '18ccp.db')
uploadToDropbox(current_path + '/../data/px.db', 'px.db')
