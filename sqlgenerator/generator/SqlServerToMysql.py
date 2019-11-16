# coding:utf-8
# author: gylhaut time:2019/6/13

import pymssql
import types
def upper2lower(name):
    old_name = name;
    list =[]
    if(len(old_name) == 1):
        return old_name.lower()
    else:
        split_str0 = old_name[0].lower();
        list.append(split_str0)
        for i in range(1, len(old_name)):
            if(old_name[i].isupper() and old_name[i-1].islower()):
                list.append("_"+old_name[i].lower())
            elif(old_name[i].isupper() and old_name[i-1].isupper()):
                list.append(old_name[i].lower())
            else:
                list.append(old_name[i])
        return ''.join(list)

def regx2lower(name):
    str_name = re.sub("[A-Z]",
                      lambda x: "_" + x.group(0).lower() if not x.span() == (0, 1) else x.group(0).lower(),
                      name)
    return str_name

# 支持表前加前缀
TableSpace = 'test_'
# 原表名字
TableName = 'students'

p_type = {
    'bigint': 'bigint',
    'binary': 'binary',
    'bit': 'tinyint',
    'char': 'char',
    'date': 'date',
    'datetime': 'datetime',
    'datetime2': 'datetime',
    'datetimeoffset': 'datetime',
    'decimal': 'decimal',
    'float': 'float',
    'int': 'int',
    'money': 'float',
    'nchar': 'char',
    'ntext': 'text',
    'numeric': 'decimal',
    'nvarchar': 'varchar',
    'real': 'float',
    'smalldatetime': 'datetime',
    'smallint': 'smallint',
    'smallmoney': 'float',
    'text': 'text',
    'time': 'time',
    'timestamp': 'timestamp',
    'tinyint': 'tinyint',
    'uniqueidentifier': 'varchar(40)',
    'varbinary': 'varbinary',
    'varchar': 'varchar',
    'xml': 'text'
}
sql = '''SELECT
           字段序号 = a.colorder,
           字段名 = a.name,
           类型 = b.name,
         字段说明 = isnull(g.[value], ''),
         占用字节数 = a.length,
         小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
         主键 = CASE WHEN EXISTS ( SELECT 1
           FROM  sysobjects
           WHERE xtype = 'PK' AND parent_obj = a.id
           AND name IN (
               SELECT name FROM sysindexes
               WHERE indid IN ( SELECT indid
                       FROM sysindexkeys
                       WHERE id = a.id AND colid = a.colid)
           )
        ) THEN 1 ELSE 0 END,
         长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
         表名 = d.NAME 
       FROM
           syscolumns a
       INNER JOIN sysobjects d ON a.id = d.id
       AND d.xtype = 'U'
       AND d.name <> 'dtproperties'
       LEFT JOIN systypes b ON a.xusertype = b.xusertype
       LEFT JOIN syscomments e ON a.cdefault = e.id
       LEFT JOIN sys.extended_properties g ON a.id = G.major_id
       AND a.colid = g.minor_id
       LEFT JOIN sys.extended_properties f ON d.id = f.major_id
       AND f.minor_id = 0
       WHERE d.name = %s
       ORDER BY
           a.colorder
       '''
# ms = MSSQL(host="192.168.1.4", user="aotest", pwd="vPl2r7lNBrErAUtihoGs", db="new_HouseRent_aotest")
conn = pymssql.connect(host="127.0.0.1", user="sa", password="123456", database="test", charset="utf8")
cur = conn.cursor()
cur.execute(sql,TableName)
values = cur.fetchall()
lst = []
lst.append(" DROP TABLE IF EXISTS {0}{1};".format(TableSpace,TableName.lower()))
lst.append("CREATE TABLE {0}{1}(".format(TableSpace,TableName.lower()))
for col in values:
    type= p_type[col[2]]
    field = upper2lower(col[1])
    if(col[6] ==1):
       lst.append('  {0} {1} NOT NULL AUTO_INCREMENT COMMENT "{2}",'.format(field, type,col[3]))
       primarykey = field
    elif(type =="varchar"  or type== "char"):
        lst.append('  {0} {1}({2}) NOT NULL DEFAULT \'\' COMMENT "{3}",'.format(field, type,col[4],col[3]))
    else:
        lst.append('  {0} {1} NULL COMMENT "{2}",'.format(field, type, col[3]))
lst.append("  PRIMARY KEY ({0})".format(primarykey))
lst.append(") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='';")

print("\r\n ".join(lst))

print("---------------------------------select-----------------------------------")

lst = []
lst.append("select ")
for col in values:
    colName = col[1]
    type = p_type[col[2]]
    field = upper2lower(col[1])
    douhao = ','
    if (type== "int" or type== "bigint" or type == "tinyint"):
        lst.append('ISNULL(' + colName + ',0) as ' + field + douhao)
    elif(type=="varchar" or type =="char" or type == "text"):
        lst.append('ISNULL(' + colName + ',\'\') as ' + field + douhao)
    elif(type =="datetime"):
        lst.append('ISNULL(' + colName + ',\'1970-01-01\') as ' + field + douhao)
    elif(type=="float" or type=="decimal"):
        lst.append('ISNULL(' + colName + ',0) as ' + field + douhao)
    else:
        lst.append('ISNULL(' + colName + ',\'\') as ' + field + douhao)
lst.append("0 as is_delete,")
lst.append("GETDATE() AS sync_time,")
lst.append("GETDATE() AS modify_time,")
lst.append("ISNULL(t.ts, 0) AS ts")
lst.append("FROM " + TableName + " AS t WITH (NOLOCK)")
lst.append("where t.ts >= ? ")
cur.close()
print("\r\n ".join(lst))








