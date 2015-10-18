# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2015
@author:       Bo Zhao
@email:        bo_zhao@hks.harvard.edu
@website:      http://yenching.org
@organization: Harvard Kennedy School
'''

import os

from selenium import webdriver

chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("http://stackoverflow.com")
driver.quit()
