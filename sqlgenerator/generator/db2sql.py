import re
# import mysql.connector
import pymysql
def lower_convert(str):
    new_str = ''
    for i in range(0, len(str)):
        if i == 0:
            new_str = str[i].upper()
        else:
            split_str0 = str[i - 1]
            split_str1 = str[i]
            if ((split_str0 == '_') & (split_str1 != '_') ):
                new_str = new_str + split_str1.upper()
            elif(split_str1 != '_'):
                new_str = new_str + split_str1
    return new_str


conn = mysql.connector.connect(host="192.168.1.213", user='root', password='qk365@test', database='information_schema')
#conn = mysql.connector.connect(host="127.0.0.1", user='root', password='zhoujisheng', database='information_schema',charset="utf8mb4")
cursor = conn.cursor()

table_schema = 'datacenter'
table_name = 'pp_ower_contract'

sql = "SELECT c.COLUMN_NAME,c.DATA_TYPE,c.COLUMN_COMMENT from information_schema.columns AS c WHERE table_name = '"+table_name+"' AND table_schema = '"+table_schema+"' ORDER BY ORDINAL_POSITION "
cursor.execute(sql)
values = cursor.fetchall()
print('-------------------------------Entity------------------------------------')
# print(values)
print('///<summary>')
print('/// The entity class for DB table '+table_name+'.')
print('///</summary>')
print('public class '+lower_convert(table_name)+'Entity')
print('{')
for col in values:
    print('    ///<summary>')
    #print('    ///'+str(col[2].decode()))  # charset=utf8mb4
    print('    ///'+str(col[2]))  # CHARSET=utf8
    print('    ///</summary>')
    print('    [Column("'+col[0]+'")]')

    cha = '    public '
    # cha_type = col[1].decode()
    cha_type = col[1]
    if(re.match('varchar', cha_type, flags=0) is not  None):
        cha = cha + 'string'
    elif(re.match('bigint', cha_type, flags=0) is not  None):
        cha = cha + 'long'
    elif(re.match('int', cha_type, flags=0) is not  None):
        cha = cha + 'int'
    elif(re.match('bit', cha_type, flags=0) is not  None):
        cha = cha + 'bool'
    elif(re.match('decimal', cha_type, flags=0) is not  None):
        cha = cha + 'decimal'
    elif(re.match('datetime', cha_type, flags=0) is not  None):
        cha = cha + 'DateTime'
    cha = cha + ' ' + lower_convert(col[0]) + ' { get; set; }'
    print(cha)
print('}')
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

# print(type(values))
# print(type(values[0]))
# print(values)
# print(values[0])
# print(values[0][0])

cursor.close()
conn.close()

