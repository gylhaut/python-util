#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 17:49
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : test02.py
# @Software: PyCharm

def debug(func):
    def wrapper(*args,**kwargs): #指定宇宙无敌参数
        print("[DEBUG]: enter {}()".format(func.__name__))
        print("Prepare and say...")
        return func(*args,**kwargs)
    return wrapper #返回
@debug
def say(something):
    print("hello {}!".format(something))




if __name__ == '__main__':
    say("你好")