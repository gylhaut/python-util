#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 17:56
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : decorator01.py
# @Software: PyCharm

# 带参数的装饰器的实现

def logging(level):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            print("[{level}]: enter function {func}()".format(
                level=level,
                func=func.__name__))
            return func(*args,**kwargs)
        return inner_wrapper
    return wrapper
@logging(level='INFO')
def say(something):
    print("say {}!".format(something))

@logging(level='DEBUG')
def do(something):
    print("do {}...".format(something))


if __name__ == '__main__':
    say('hello')
    do("my work")

