#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 9:41
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : decorator02.py
# @Software: PyCharm

class logging(object):
    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func):  # 接受函数
        def wrapper(*args, **kwargs):
            print( "[{level}]: enter function {func}()".format(
                level=self.level,
                func=func.__name__))
            func(*args, **kwargs)
        return wrapper  # 返回函数


@logging(level='INFO')
def say(something):
    print("say {}!".format(something))
