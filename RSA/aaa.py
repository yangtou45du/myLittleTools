#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import  os
def function(tagert):
    currentdir=os.getcwd()#获取当前目录
    if currentdir!=tagert and os.path.isdir(tagert):
        os.chdir(tagert)#g工作目录不在当前目前，切换到当前目录
    listdirs=os.listdir(os.getcwd())#获取该目录下所有的文件以及子文件
    for i in listdirs:
        print os.path.isdir(os.getcwd()+"\\"+i.decode("gbk").encode("utf-8"))
        print os.getcwd()+"\\"+i.decode("gbk").encode("utf-8")

        if os.path.isdir(os.getcwd()+"\\"+i.decode("gbk").encode("utf-8")):
            print 11
        #print i.decode("gbk").encode("utf-8")


ta="E:\lainxi"
function(ta)