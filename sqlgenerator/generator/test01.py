#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 17:44
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : test01.py
# @Software: PyCharm


def debug(func):
    def wrapper(something):  # 指定一毛一样的参数
        print ( "[DEBUG]: enter {}()".format(func.__name__))
        return func(something)
    return wrapper  # 返回包装过函数

@debug
def say(something):
    print("hello {}!".format(something))

if __name__ == '__main__':
    say("world")