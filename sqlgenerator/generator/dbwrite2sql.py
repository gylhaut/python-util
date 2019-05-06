#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 13:30
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : dbwrite2sql.py
# @Software: PyCharm



file_handle=open('1.cs',mode='w',encoding = 'utf-8')
# 2.1  write 写入
#\n 换行符
file_handle.write('hello word 你好 \n')
# 2.2  writelines()函数 会将列表中的字符串写入文件中，但不会自动换行，如果需要换行，手动添加换行符
#参数 必须是一个只存放字符串的列表
file_handle.writelines(['hello\n','world\n','你好\n','智游\n','郑州\n'])
##3、关闭文件
file_handle.close()