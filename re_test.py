# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
import re

pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.subn(pattern, r'\2 \1', s)


def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()


print re.subn(pattern, func, s)

### output ###
# ('say i, world hello!', 2)
# ('I Say, Hello World!', 2)
