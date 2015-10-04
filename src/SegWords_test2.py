# -*- coding: utf-8 -*-
# !/usr/bin/python
'''
Created on Nov 11, 2012

@author: bo
'''
from ctypes import cdll,create_string_buffer
ld=cdll.LoadLibrary('ICTCLAS/libICTCLAS50.so')
Init=getattr(ld,'_Z12ICTCLAS_InitPKc')
Init('ICTCLAS/')
ImportDict=getattr(ld,'_Z22ICTCLAS_ImportUserDictPKci9eCodeType')
Process=getattr(ld,'_Z24ICTCLAS_ParagraphProcessPKciPc9eCodeTypeb')
Exit=getattr(ld,'_Z12ICTCLAS_Exitv')

print 'before:'
szText = '如果你增加了一些成员变量, 全能补全还不能马上将新成员补全, 需要你重新生成一下tags文件, 但是你不用重启vim, 只是重新生成一下tags文件就行了, 这时全能补全已经可以自动补全了, 还真够"全能"吧'
cntText=len(szText)
buf=create_string_buffer(cntText*6)
rlen=Process(szText,cntText,buf,3,True)
print buf.value
usrDict='成员变量@@nr;新成员@@nr;补全@@nr;重启@@nr'
rlen=ImportDict(usrDict,len(usrDict),1)
print '%d imported.'%rlen

print 'after:'
rlen=Process(szText,cntText,buf,3,True)
print buf.value
Exit()