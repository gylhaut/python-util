
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 9:46
# @Author  : maomao
# @File    : sql_create_table.py

import re



"""
建立相关表的字段
从源表创建指定的MySQL建表脚本

"""
# 目标表名称 lzb_decoration_houseinfo
table_name = 'lzb_decoration_procedure_template'
# 原表名称
original_table_name="DecorationProcedureTemplate"

print("DROP TABLE IF EXISTS {0};".format(table_name))
print("CREATE TABLE {0} (".format(table_name))
print("id bigint(20) unsigned NOT NULL AUTO_INCREMENT")

with open('sql_server_table_source', encoding='UTF-8') as f:
    for line in f.readlines():
      #print(line)
      if line=='\n':
          continue

      if re.match('.*(NOT.*NULL).*', line) is None:
          if re.match('.*(.*NULL.*).*',line) is not None:
            line = line.replace("NULL", " NOT NULL ")

      #print(line)
      # 获取注释
      str_comment='未知'
      list_comment=re.findall(r".*,(.*)",line)
      if len(list_comment)==1:
          str_comment=list_comment[0].strip()
      # 获取注释后的字符
      temp_line_list=re.findall(r"(.*),.*",line)
      if temp_line_list is None or temp_line_list=="" or len(temp_line_list)==0:
          continue

      temp_line=temp_line_list[0]
      #  unrenow_reason varchar(512)
      prefix_line=re.sub(r'(\[.*\])','',temp_line).strip()
      #print(prefix_line)
      #str_comment=re.sub("(\,)","",str_comment)
      #if re.match(r'.*ts.*', prefix_line, flags=0) is not None:

      if re.match(r'ts.*bigint.*NOT.*NULL.*', prefix_line, flags=0) is not None:
          continue
      if re.match(r'.*int.*', prefix_line, flags=0) is not None:
          if re.match(r'(.*int.*NOT.*NULL).*',prefix_line, flags=0) is not None:
              if re.match(r'(id int NOT NULL).*',prefix_line, flags=0) is not None:
                  prefix_line = re.findall(r"(id int NOT NULL).*", prefix_line)
                  print("," +"origin_" +prefix_line[0] + " " + " DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
              else:
                prefix_line = re.findall(r"(.*int.*NOT.*NULL).*", prefix_line)
                #print(prefix_line[0])
                print("," + prefix_line[0] + " " + " DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
          else:
              print(","+prefix_line+" "+"NOT NULL  DEFAULT 0 "+"COMMENT '"+str_comment.strip()+"'")
          continue
      if re.match(r'.*decimal.*', prefix_line, flags=0) is not None:
          #print(prefix_line)
          if re.match(r'(.*decimal\(18,2\).*NOT.*NULL).*', prefix_line, flags=0) is not None:
              prefix_line = re.findall(r"(.*decimal\(18,2\).*NOT.*NULL).*", prefix_line)
              print( "," + prefix_line[0] +" " + " DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
          else:
              print(
                  "," + prefix_line + "(18,2)" + " " + "NOT NULL DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
          continue

      if re.match(r'.*datetime.*', prefix_line, flags=0) is not None:
          #print(prefix_line)
          if re.match(r'(.*datetime.* NOT NULL).*', prefix_line, flags=0) is not None:
              prefix_line = re.findall(r"(.*datetime.* NOT NULL).*", prefix_line)
              print(
                  "," + prefix_line[0] + " " + " DEFAULT '1970-01-01' " + "COMMENT '" + str_comment.strip() + "'")
          else:
            print("," + prefix_line + " " + "NOT NULL DEFAULT '1970-01-01' " + "COMMENT '" + str_comment.strip() + "'")
          continue

      if re.match(r'.*varchar.*', prefix_line, flags=0) is not None:
          if re.match(r'(.*varchar.* NOT NULL).*', prefix_line, flags=0) is not None:
              prefix_line = re.findall(r"(.*varchar.* NOT NULL).*", prefix_line)
              #print(prefix_line[0])
              strinfo = re.compile('nvarchar')
              b = strinfo.sub('varchar', prefix_line[0])
              print("," + b + " " + " DEFAULT '' " + "COMMENT '" + str_comment.strip() + "'")
          else:
              strinfo = re.compile('nvarchar')
              b = strinfo.sub('varchar', prefix_line)
              print("," + b + " " + "NOT NULL DEFAULT ''" + "COMMENT '" + str_comment.strip() + "'")
          continue
      if re.match(r'.*bit.*', prefix_line, flags=0) is not None:
          if re.match(r'(.*bit.*NOT.*NULL).*', prefix_line, flags=0) is not None:
              prefix_line = re.findall(r"(.*bit.*NOT.*NULL).*", prefix_line)
              print("," + prefix_line[0] + " " + " DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
          else:
            print("," + prefix_line + " " + "NOT NULL DEFAULT 0 " + "COMMENT '" + str_comment.strip() + "'")
          continue
      if re.match(r'.*uniqueidentifier.*',prefix_line,flags=0) is not None:
          prefix_line = re.findall(r"(.*)uniqueidentifier.*", prefix_line)
          print("," + prefix_line[0] + "varchar(64) NOT NULL DEFAULT '' " + "COMMENT '" + str_comment.strip() + "'")
          continue

print(",source_db int(11) NOT NULL DEFAULT 0 COMMENT '1:LZB,2:LZB_V3,3:project1.0,4:project2.0'")
print(",ts bigint NOT NULL DEFAULT 0 COMMENT '源表时间戳' ")
print(",sync_time  datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '从原表同步到报表的时间'")
print(",modify_time  datetime NOT NULL COMMENT '最后更新时间'")
print(",PRIMARY KEY (id)")
print(') ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT  CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')

print("\n\n\n\n")

print("同步kettle脚本")


print("select ")
with open('sql_server_table_source', encoding='UTF-8') as f:
    for line in f.readlines():
      if line=='\n':
          continue

      str_original_field = ""
      field_original_reg=re.findall(".*\[(.*)\].*",line)
      if field_original_reg is not None:
          str_original_field=field_original_reg[0]

      result_field_nvarchar=re.findall('.*\](.*)\s*nvarchar.*',line)

      is_nvarchar_field=False
      is_bigint_field=False

      str_target_field=""
      if result_field_nvarchar is not None and len(result_field_nvarchar)>0:
          str_target_field=result_field_nvarchar[0]
          is_nvarchar_field=True
      else:
          result = re.findall('.*\](.*)(int|varchar|uniqueidentifier|datetime|bigint|decimal|nvarchar|bit).*', line)
          if result is not None and len(result)!=0 and len(result[0])!=0:
              str_target_field=result[0][0].strip()

      if re.match('.*(bigint).*', line) is not None:
          result_field_bigint = re.findall('.*\](.*)\s*bigint.*', line)
          str_target_field=result_field_bigint[0].strip()
      if str_target_field == "id":
          str_target_field ="origin_" +str_target_field

      if is_nvarchar_field or re.match(r".*(varchar|uniqueidentifier).*", line) is not None:
          print("ISNULL(t.{0},'') AS {1},".format(str_original_field.strip(),str_target_field))
      elif is_bigint_field:
          print("ISNULL(t.{0},0) AS {1},".format(str_original_field.strip(), str_target_field))
      elif re.match('.*(bigint).*',line) is not None or re.match(r".*(int|bigint|decimal).*",line) is not None:
          if re.match(r'.*ts bigint.*', line, flags=0) is not None:
              continue
          else:
            print("ISNULL(t.{0},0) AS {1},".format(str_original_field.strip(), str_target_field))
      elif re.match(r".*(datetime|date).*",line) is not None:
          print("ISNULL(t.{0},'1970-01-01') AS {1},".format(str_original_field.strip(), str_target_field))
      elif re.match(r".*(bit).*",line) is not None:
          print("ISNULL(t.{0},0) AS {1},".format(str_original_field.strip(), str_target_field))
      else :
          print("error")
print('2 AS source_db,')
print("GETDATE() as sync_time,")
print("GETDATE() as modify_time, ")
print("ISNULL(t.ts,0) AS ts ")
print(" from {0} as t with(nolock) where t.ts> ? ".format(original_table_name))












