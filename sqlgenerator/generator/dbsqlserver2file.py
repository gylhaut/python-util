# coding:utf-8
# author: gylhaut time:2019/6/13

import pymssql
import types

# 支持表前加前缀
TableSpace = 'pay_'
# 表名字
TableName = 'billingHeader'


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
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
                if (column is not None and isinstance(column, str)):  # types.StringType == type(column)):
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
        # mscursor = self.conn.cursor()
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
        sql = (
            "SELECT NAME FROM sysobjects WHERE TYPE='U' AND NAME NOT IN ('dtproperties','0626') AND NAME = '" + TableName + "'")
        mscursor.execute(sql)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
        for row in table:
            sqlext = self.createTable(row[0])
            print(sqlext)

            sqlselect = self.selectTable(row[0])
            print(sqlselect)
        mscursor.close()

    def createTable(self, tablename):
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
        csql = "CREATE TABLE " + TableSpace + "%s ( \r\n" % tablename.lower()

        lst = []
        for row in table:
            field = self.analyField(row[0])
            if (row[1] == "int"):
                if (row[4] == 1 and len(lst) <= 0 and row[5] == 1):
                    lst.append(field + " bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键'")
                elif (row[4] == 1 and len(lst) > 0 and row[5] == 1):
                    lst.append("," + field + " bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键'")
                elif (row[4] == 0 and len(lst) <= 0 and row[5] != 0):

                    lst.append(field + " INT NOT NULL DEFAULT 0 COMMENT '" + row[6].replace("/r/n[0-9]", " ") + "'")
                elif (len(lst) > 0):

                    lst.append(
                        "," + field + " INT NOT NULL DEFAULT 0 COMMENT '" + row[6].replace("/r/n[0-9]", " ") + "'")
                else:

                    lst.append(field + " INT NOT NULL DEFAULT 0 COMMENT '" + row[6].replace("/r/n[0-9]", " ") + "'")
            if (row[1] == "bigint"):
                lst.append(field + " bigint(20) NOT NULL COMMENT '" + row[6].replace("/r/n[0-9]", " ") + "'")
            if (row[1] == "varchar"):
                if (len(lst) <= 0):
                    lst.append(
                        field + " varchar(" + str(row[2]) + ")  NOT NULL DEFAULT '' COMMENT '" + row[6].replace("/r/n",
                                                                                                                " ") + "'")
                else:
                    lst.append(
                        "," + field + " varchar(" + str(row[2]) + ") NOT NULL DEFAULT '' COMMENT '" + row[6].replace(
                            "/r/n", " ") + "'")
            if (row[1] == "text"):
                if (len(lst) <= 0):
                    lst.append(field + " text ")
                else:
                    lst.append("," + field + " text ")
            if (row[1] == "datetime"):
                if (len(lst) <= 0):
                    lst.append(
                        field + " datetime NOT NULL DEFAULT '1970-01-01' COMMENT '" + row[6].replace("/r/n", " ") + "'")
                else:
                    lst.append(
                        "," + field + " datetime NOT NULL DEFAULT '1970-01-01' COMMENT '" + row[6].replace("/r/n",
                                                                                                           " ") + "'")
            if (row[1] == "numeric" or row[1] == "money" or row[1] == "float" or row[1] == "decimal"):
                if (len(lst) <= 0):
                    lst.append(field + " decimal(18,2) NOT NULL COMMENT '" + row[6].replace("/r/n", " ") + "'")
                else:
                    lst.append("," + field + " decimal(18,2) NOT NULL COMMENT '" + row[6].replace("/r/n", " ") + "'")
            if (row[1] == "bit"):
                if (len(lst) <= 0):
                    lst.append(field + " boolean DEFAULT FALSE ")
                else:
                    lst.append("," + field + " boolean DEFAULT FALSE ")
            if (row[1] == "tinyint"):
                if (len(lst) <= 0):
                    lst.append(field + " smallint DEFAULT 0 ")
                else:
                    lst.append("," + field + " smallint DEFAULT 0 ")
            if (row[1] == "char"):
                if (len(lst) <= 0):
                    lst.append(field + " char(" + str(row[2]) + ")")
                else:
                    lst.append("," + field + " char(" + str(row[2]) + ")")
        lst.append(");")
        mscursor.close()
        return csql + "\r\n ".join(lst)

    def analyField(self, fieldname):
        old_column_name = fieldname
        new_column_name = ''
        if (len(old_column_name) > 2):
            new_column_name = old_column_name[0]
            for i in range(1, len(old_column_name) - 1):
                split_str0 = old_column_name[i - 1]
                split_str1 = old_column_name[i]
                split_str2 = old_column_name[i + 1]
                if ((split_str0 != '_') & split_str1.isupper() & split_str2.islower()):
                    new_column_name = new_column_name + '_' + split_str1.lower()
                elif (split_str0.islower() & split_str1.isupper()):
                    new_column_name = new_column_name + '_' + split_str1.lower()
                else:
                    new_column_name = new_column_name + split_str1
            new_column_name = new_column_name + old_column_name[-1]
        else:
            new_column_name = old_column_name.lower()
        return new_column_name.lower()

    def executeTable(self, tablename, count):
        sql1 = "SELECT * FROM %s" % tablename
        mscursor = self.__GetConnect()
        mscursor.execute(sql1)
        table = mscursor.fetchall()
        if (table is None or len(table) <= 0):
            mscursor.close()
            return
        lst_result = self.initColumn(table)
        print(lst_result)
        mscursor.close()

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
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
                lst.append('ISNULL(' + colName + ',0) as ' + self.analyField(colName) + douhao)
            if (row[1] == "bigint"):
                lst.append('ISNULL(' + colName + ',0) as ' + self.analyField(colName) + douhao)
            if (row[1] == "varchar"):
                lst.append('ISNULL(' + colName + ',\'\') as ' + self.analyField(colName) + douhao)
            if (row[1] == "text"):
                lst.append('ISNULL(' + colName + ','') as ' + self.analyField(colName) + douhao)
            if (row[1] == "datetime"):
                lst.append('ISNULL(' + colName + ',\'1970-01-01\') as ' + self.analyField(colName) + douhao)
            if (row[1] == "numeric" or row[1] == "money" or row[1] == "float" or row[1] == "decimal"):
                lst.append('ISNULL(' + colName + ',0) as ' + self.analyField(colName) + douhao)
            if (row[1] == "bit"):
                lst.append('ISNULL(' + colName + ',0) as ' + self.analyField(colName) + douhao)
            if (row[1] == "tinyint"):
                lst.append('ISNULL(' + colName + ',0) as ' + self.analyField(colName) + douhao)
        lst.append("GETDATE() AS sync_time,")
        lst.append("GETDATE() AS modify_time,")
        lst.append("ISNULL(t.ts, 0) AS ts")
        lst.append("FROM " + tablename + " AS t WITH (NOLOCK)")
        lst.append("where t.ts >= ? ")
        mscursor.close()
        return csql + "\r\n ".join(lst)

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    ms = MSSQL(host="192.168.1.210", user="sa", pwd="hr05709685", db="payment_0611")
    ms.getAllTable()
