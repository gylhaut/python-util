#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name is db2sql2file.py

import re
import os
import pymysql

def lower_convert(str_name):
    str_new = ''
    str_split = str_name.split('_')
    str_split = [''.join([split[0].upper(),split[1:]]) for split in str_split if split]
    str_new = ''.join(str_split)
    return str_new

conn = pymysql.connect(host="192.168.1.213", user='root', password='qk365@test', database='information_schema')
cursor = conn.cursor()

table_schema = 'datacenter'
table_name = 'project_unqualified_reason'

sql = "SELECT c.COLUMN_NAME,c.DATA_TYPE,c.COLUMN_COMMENT FROM information_schema.columns AS c " \
      "WHERE table_name='{0}' AND table_schema='{1}' ORDER BY ORDINAL_POSITION"\
      .format(table_name,table_schema)

cursor.execute(sql)
values = cursor.fetchall()

# 1 创建文件
file_handle = open(lower_convert(table_name) + 'Entity.cs', mode='w', encoding='utf-8')

# 2  write 写入
using_args = [
    'using System;',
    'using System.ComponentModel.DataAnnotations;',
    'using System.ComponentModel.DataAnnotations.Schema;',
    'using QK365.Component.Data;',
    'namespace QK365.Core.DB.EntityModel',
    '{'
]
using_args.append('    ///<summary>')
using_args.append('    /// The entity class for DB table {0} .'.format(table_name))
using_args.append('    ///</summary>')
using_args.append('    [Table("{0}")]'.format(table_name))
using_args.append('    public class {0}Entity'.format(lower_convert(table_name)))
using_args.append('    {')

p_use = [
    'public',
    'private',
    '{ get; set; }'
]
p_type={
    'varchar':'System.String',
    'int':'System.Int32',
    'tinyint':'System.Int32',
    'bigint':'System.Int64',
    'bit':'System.Boolean',
    'decimal':'System.Decimal',
    'datetime':'System.DateTime',
}

for col in values:
    using_args.append('        ///<summary>')
    using_args.append('        /// {0}'.format(str(col[2])))
    using_args.append('        ///</summary>')
    using_args.append('        [Column("{0}")]'.format(col[0]))
    type = col[1]
    cha = lower_convert(col[0])
    using_args.append('        {0} {1} {2} {3}'.format(p_use[0], p_type[type], cha, p_use[2]))
    using_args.append('        ')

using_args.append('    }')
using_args.append('}')

using_args = [''.join([arg,'\n']) for arg in using_args if arg]
file_handle.writelines(using_args)
file_handle.close()

print('-------------------------------SELECT------------------------------------')
print('SELECT')
for col in values:
    colName = col[0]
    douhao = ','
    if (col == values[len(values)-1]):
        douhao = ''
    print('\t', colName, 'as', lower_convert(colName), douhao)
print('FROM', table_name)
print('WHERE 1=2')

print('-------------------------------INSERT------------------------------------')
print('INSERT INTO', table_name)
print('(')
new_colname = ''
for col in values:
    colName = col[0]
    douhao = ','
    huanhang = '\n'
    if(col==values[0]):
        huanhang = ''
    if (col == values[len(values)-1]):
        douhao = ''
    print('\t', colName, douhao)
    new_colname = new_colname + huanhang + '\t@' + lower_convert(colName) + douhao
print(')')
print('VALUES')
print('(')
print(new_colname)
print(')')

print('-------------------------------UPDATE------------------------------------')
print('UPDATE', table_name)
print('SET')
for col in values:
    colName = col[0]
    douhao = ','
    if (col == values[len(values)-1]):
        douhao = ''
    print('\t', colName, '=', '@'+lower_convert(colName), douhao)
print('WHERE 1=2')


cursor.close()
conn.close()

