#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 9:52
# @Author  : gylhaut
# @Site    : "http://www.cnblogs.com/gylhaut/"
# @File    : generate_table_struct.py
# @Software: PyCharm

import re


"""
建立相关表的字段
从源表创建指定的MySQL建表脚本

"""
with open('temp_table', encoding='UTF-8') as f:
    for line in f.readlines():
      print(line)
      if line=='\n':
          continue

      if re.match('.*(NOT.*NULL).*', line) is None:
          if re.match('.*(.*NULL.*).*',line) is not None:
            line = line.replace("NULL", " NOT NULL ")

      #print(line)
      # 获取注释

      list_comment = re.findall(r'\'(.*)\'',line)
      if list_comment.__len__() == 0:
        str_comment = '未知'
      else:
        str_comment = list_comment[0].strip()

      list_field=re.findall(r'(\[.*\])',line)
      str_filed = list_field[0].strip()
      #print(str_filed)
      new_field = re.findall(r'\[(.*)\]',str_filed)
      new_field = new_field[0].strip()
     # print(new_field + "  "+str_comment)
      #print(str_comment)
      #print(new_field+',')
      #print(new_field)
      new_column_name = ''
      if (len(new_field) > 2):
        new_column_name = new_field[0]
        for i in range(1, len(new_field) - 1):
          split_str0 = new_field[i - 1]
          split_str1 = new_field[i]
          split_str2 = new_field[i + 1]
          if ((split_str0 != '_') & split_str1.isupper() & split_str2.islower()):
            new_column_name = new_column_name + '_' + split_str1.lower()
          elif (split_str0.islower() & split_str1.isupper()):
            new_column_name = new_column_name + '_' + split_str1.lower()
          else:
            new_column_name = new_column_name + split_str1
        new_column_name = new_column_name + new_field[-1]
      else:
        new_column_name = new_field.lower()



    #  mew_string =re.sub(r'[A-Z]',lambda x:"_"+x.group(0),new_field)
    #  mew_string =mew_string.lower()
    #  mew_string = re.findall(r'([a-z]+.*)', mew_string)[0].strip()
      #剩余字符串
      end_field = re.sub(r'(\[.*\])','', line).strip()
      #print(new_column_name.lower())
      print(str_filed+ ' '+ new_column_name.lower() + " "+end_field)












