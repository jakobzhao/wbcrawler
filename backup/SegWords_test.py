# -*- coding: utf-8 -*-
# !/usr/bin/python
'''
Created on Oct 26, 2012

@author:       Bo Zhao
@email:        Jakobzhao@gmail.com
@website:      http://yenching.org
@organization: The Ohio State University
'''

from src.pyictclas import PyICTCLAS, CodeType

a = PyICTCLAS()
#text = '如果你增加了一些成员变量, 全能补全还不能马上将新成员补全, 需要你重新生成一下tags文件, 但是你不用重启vim, 只是重新生成一下tags文件就行了, 这时全能补全已经可以自动补全了, 还真够"全能"吧'
text = '此外，民众中对薄熙来本人以及他在担任重庆市委书记期间所推行的民粹主义治理方式还存在一定的支持。薄熙来在担任重庆领导人期间提倡红色运动，并将大量政府支出投入到基础设施和其他社会性项目中。指责薄熙来在其整个从政生涯中犯有大量错误，似乎意味着中共决意要打击对他的这些支持。'
b = a.ictclas_paragraphProcess(text, CodeType.CODE_TYPE_UTF8, True)
a.ictclas_exit()
print b.value
print "finished"
