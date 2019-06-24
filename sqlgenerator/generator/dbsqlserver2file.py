#coding:utf-8
# author: gylhaut time:2019/6/13


# -*- coding:utf-8 -*-

import pymssql
import types
# 支持表前加前缀
TableSpace='project_'
#表名字
TableName ='reform_record'

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def initColumn(self, table):
        if (table is None or len(table) <= 0):
            return None
        lst_result = []
        for row in table:
            i = 0
            lines = []
            for column in row:
                print(column)
                return column
                # if type(bestSplit) == Types.ListType
                if (column is not None and isinstance(column,str)): # types.StringType == type(column)):
                    # lines.append(unicode(column))
                    try:
                        lines.append((column.decode('cp936')).encode('utf-8'))
                    except:
                        lines.append(column)
                else:
                    lines.append(column)
                i += 1
            lst_result.append(lines)
        return lst_result

    def exesyncdb(self):
        #mscursor = self.conn.cursor()
        mscursor = self.__GetConnect()
        sql = ("SELECT COUNT(COLUMNNAME) AS CT,TABLENAME FROM " \
               "(SELECT A.NAME AS COLUMNNAME,B.NAME AS TABLENAME FROM SYSCOLUMNS A RIGHT JOIN " \
               " SYSOBJECTS B ON A.ID=B.ID WHERE B.TYPE='U' AND B.NAME NOT IN ('dtproperties','0626')) A " \
               " GROUP BY TABLENAME ")
        # print sql
        mscursor.execute(sql)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            return
        else:
            for row in table:
                # print row[1]
                self.executeTable(row[1], row[0])
               # print("%s is execute success" % row[1])

    def getAllTable(self):
        mscursor = self.__GetConnect()
        sql = ("SELECT NAME FROM sysobjects WHERE TYPE='U' AND NAME NOT IN ('dtproperties','0626') AND NAME = '" + TableName+ "'")
       # sql = ("SELECT NAME FROM sysobjects WHERE TYPE='U' AND NAME NOT IN ('dtproperties','0626')")
        mscursor.execute(sql)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
       # pgcursor = self.pgconn.cursor()
        for row in table:
            sqlext = self.createTable(row[0])
            print(sqlext)
            sqlselect = self.selectTable(row[0])
            print(sqlselect)
        mscursor.close()
       # pgcursor.close()
        # ----------------------
        # 根据SQL SERVER数据库基本结构创建PostgreSQL数据库表结构
        # ----------------------

    def createTable(self, tablename):
        mscursor = self.__GetConnect()
        # sql=("SELECT A.NAME AS COLUMNNAME,C.NAME,A.LENGTH,B.NAME AS TABLENAME "\
        #          " FROM SYSCOLUMNS A RIGHT JOIN  SYSOBJECTS B ON A.ID=B.ID "\
        #          " LEFT JOIN SYSTYPES C ON C.XTYPE=A.XTYPE "\
        #          " WHERE B.TYPE='U' AND B.NAME=%s AND B.NAME NOT IN ('dtproperties','BUPLOADCUSTOMER','RFREIGHT')")
        sql = ("SELECT A.NAME AS COLUMNNAME,C.NAME,A.LENGTH,B.NAME AS TABLENAME,ISNULL(D.PKS,0) AS PKEY,E.CT,isnull(G.[value],'')" \
               " FROM SYSCOLUMNS A RIGHT JOIN  SYSOBJECTS B ON A.ID=B.ID " \
               " LEFT JOIN SYSTYPES C ON C.XTYPE=A.XTYPE LEFT JOIN " \
               " (SELECT A.NAME,1 AS PKS FROM SYSCOLUMNS A " \
               " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s)" \
               " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID " \
               " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') D " \
               " ON A.NAME =D.NAME " \
               " LEFT JOIN (SELECT COUNT(A.COLUMNNAME) AS CT,%s AS TABLENAME  FROM " \
               " (SELECT A.NAME AS COLUMNNAME,D.NAME AS TABLENAME FROM SYSCOLUMNS A " \
               " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s) " \
               " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID " \
               " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') A GROUP BY A.TABLENAME) E " \
               " ON B.NAME=E.TABLENAME " \
               " LEFT join sys.extended_properties G " \
               " on A.id=G.major_id and A.colid=G.minor_id " \
               " WHERE B.TYPE='U'  AND B.NAME=%s AND B.NAME NOT IN ('dtproperties') ")
        # sql =  r'''
        # SELECT
        #     -- 表名 = case when a.colorder=1 then d.name else '' end,
        #     -- 表说明 = case when a.colorder=1 then isnull(f.value,'') else '' end,
        #     字段序号 = a.colorder,
        #     字段名 = a.name,
        #     类型 = CASE WHEN b.name = 'varchar' OR b.name = 'nvarchar' THEN b.name+'('+CONVERT(VARCHAR(20),COLUMNPROPERTY(a.id,a.name,'PRECISION'))+')' ELSE b.name END,
        #     字段说明 = isnull(g.[value],''),
        #     主键 = case when exists(SELECT 1 FROM sysobjects where xtype='PK' and parent_obj=a.id and name in ( SELECT name FROM sysindexes WHERE indid in( SELECT indid FROM sysindexkeys WHERE id = a.id AND colid=a.colid))) then '√' else '' end,
        #     占用字节数 = a.length,
        #     长度 = COLUMNPROPERTY(a.id,a.name,'PRECISION'),
        #     小数位数 = isnull(COLUMNPROPERTY(a.id,a.name,'Scale'),0)
        #     FROM syscolumns a
        #     left join systypes b
        #     on a.xusertype=b.xusertype
        #     inner join sysobjects d
        #     on a.id=d.id and d.xtype='U' and d.name<>'dtproperties'
        #     left join syscomments e
        #     on a.cdefault=e.id
        #     left join sys.extended_properties g
        #     on a.id=G.major_id and a.colid=g.minor_id
        #     left join sys.extended_properties f
        #     on d.id=f.major_id and f.minor_id=0
        #     where d.name='Acceptance_List' --如果只查询指定表,加上此红色where条件，tablename是要查询的表名；去除红色where条件查询所有的表信息
        #     order by a.id,a.colorder'''
        mscursor.execute(sql, (tablename, tablename, tablename, tablename))
        #mscursor.execute(sql)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
        csql = "CREATE TABLE " + TableSpace + "%s ( \r\n" % tablename.lower()

        lst = []
        for row in table:
            if (row[1] == "int"):
                if (row[4] == 1 and len(lst) <= 0 and row[5] == 1):
                    lst.append(row[0] + " bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键'")
                elif (row[4] == 1 and len(lst) > 0 and row[5] == 1):
                    lst.append("," + row[0] + " bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键'")
                elif (row[4] == 0 and len(lst) <= 0 and row[5] != 0):

                    lst.append(row[0] + " INT NOT NULL DEFAULT 0 COMMENT '"+ row[6].replace("/r/n[0-9]"," ")+ "'")
                elif (len(lst) > 0):

                    lst.append("," + row[0] + " INT NOT NULL DEFAULT 0 COMMENT '"+ row[6].replace("/r/n[0-9]"," ")+ "'")
                else:

                    lst.append(row[0] + " INT NOT NULL DEFAULT 0 COMMENT '"+ row[6].replace("/r/n[0-9]"," ")+ "'")
            if(row[1] =="bigint"):
                lst.append(row[0] + " bigint(20) NOT NULL COMMENT '"+ row[6].replace("/r/n[0-9]"," ")+ "'")
            if (row[1] == "varchar"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " varchar(" + str(row[2]) + ")  NOT NULL DEFAULT '' COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
                else:
                    lst.append("," + row[0] + " varchar(" + str(row[2]) + ") NOT NULL DEFAULT '' COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
            if (row[1] == "text"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " text ")
                else:
                    lst.append("," + row[0] + " text ")
            if (row[1] == "datetime"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " datetime NOT NULL DEFAULT '1970-01-01' COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
                else:
                    lst.append("," + row[0] + " datetime NOT NULL DEFAULT '1970-01-01' COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
            if (row[1] == "numeric" or row[1] == "money" or row[1] == "float" or row[1] == "decimal"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " decimal(18,2) NOT NULL COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
                else:
                    lst.append("," + row[0] + " decimal(18,2) NOT NULL COMMENT '"+ row[6].replace("/r/n"," ")+ "'")
            if (row[1] == "bit"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " boolean DEFAULT FALSE ")
                else:
                    lst.append("," + row[0] + " boolean DEFAULT FALSE ")
            if (row[1] == "tinyint"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " smallint DEFAULT 0 ")
                else:
                    lst.append("," + row[0] + " smallint DEFAULT 0 ")
            if (row[1] == "char"):
                if (len(lst) <= 0):
                    lst.append(row[0] + " char(" + str(row[2]) + ")")
                else:
                    lst.append("," + row[0] + " char(" + str(row[2]) + ")")
        lst.append(");")
        mscursor.close()
        return csql + "\r\n ".join(lst)



    def executeTable(self, tablename, count):
        # print tablename
        sql1 = "SELECT * FROM %s" % tablename
        #mscursor = self.msconn.cursor()
        mscursor = self.__GetConnect()
        mscursor.execute(sql1)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
        lst_result = self.initColumn(table)
        print(lst_result)
        mscursor.close()

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def selectTable(self, tablename):
        mscursor = self.__GetConnect()
        sql = (
        "SELECT A.NAME AS COLUMNNAME,C.NAME,A.LENGTH,B.NAME AS TABLENAME,ISNULL(D.PKS,0) AS PKEY,E.CT,isnull(G.[value],'')" \
        " FROM SYSCOLUMNS A RIGHT JOIN  SYSOBJECTS B ON A.ID=B.ID " \
        " LEFT JOIN SYSTYPES C ON C.XTYPE=A.XTYPE LEFT JOIN " \
        " (SELECT A.NAME,1 AS PKS FROM SYSCOLUMNS A " \
        " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s)" \
        " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID " \
        " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') D " \
        " ON A.NAME =D.NAME " \
        " LEFT JOIN (SELECT COUNT(A.COLUMNNAME) AS CT,%s AS TABLENAME  FROM " \
        " (SELECT A.NAME AS COLUMNNAME,D.NAME AS TABLENAME FROM SYSCOLUMNS A " \
        " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s) " \
        " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID " \
        " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') A GROUP BY A.TABLENAME) E " \
        " ON B.NAME=E.TABLENAME " \
        " LEFT join sys.extended_properties G " \
        " on A.id=G.major_id and A.colid=G.minor_id " \
        " WHERE B.TYPE='U'  AND B.NAME=%s AND B.NAME NOT IN ('dtproperties') ")
        mscursor.execute(sql, (tablename, tablename, tablename, tablename))
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
        csql = "SELECT "
        lst = []
        for row in table:
            colName = row[0]
            douhao = ','
            if (row[1] == "int"):
                lst.append('ISNULL('+ colName + ',0) as ' + colName.lower() + douhao)
            if (row[1] == "bigint"):
                lst.append('ISNULL(' + colName + ',0) as ' + colName.lower() + douhao)
            if (row[1] == "varchar"):
                lst.append('ISNULL(' + colName + ',\'\') as ' + colName.lower() + douhao)
            if (row[1] == "text"):
                lst.append('ISNULL(' + colName + ','') as ' + colName.lower() + douhao)
            if (row[1] == "datetime"):
                lst.append('ISNULL(' + colName + ',\'1970-01-01\') as ' + colName.lower() + douhao)
            if (row[1] == "numeric" or row[1] == "money" or row[1] == "float" or row[1] == "decimal"):
                lst.append('ISNULL(' + colName + ',0) as ' + colName.lower() + douhao)
            if (row[1] == "bit"):
                lst.append('ISNULL(' + colName + ',0) as ' + colName.lower() + douhao)
            if (row[1] == "tinyint"):
                lst.append('ISNULL(' + colName + ',0) as ' + colName.lower() + douhao)
        lst.append("FROM " + tablename)
        lst.append("where 1 =2")
        mscursor.close()
        return csql + "\r\n ".join(lst)


    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    ms = MSSQL(host="192.168.1.210", user="sa", pwd="hr05709685", db="ProjectManage_New_V7_20150731_dev")
    # reslist = ms.ExecQuery("SELECT * from Acceptance_List")
    # for i in reslist:
    #     print(i)
    ms.getAllTable()


