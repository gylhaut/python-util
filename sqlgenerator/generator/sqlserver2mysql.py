# -*- coding: utf-8 -*-
# author: gylhaut time:2019/6/13#coding=utf-8
#import _mssql
import pymssql
import types
TableSpace='ABS.'
class SyncDataBase():
    def __init__(self):
        self.pgconn=psycopg2.connect("dbname=absob host=192.168.1.32 user=postgres password=12345")
        self.msconn=pymssql.connect(host="192.168.1.20",user="sa",password="sa",database="absOB090615")
    def commit(self):
        self.pgconn.commit()
    def close(self):
        self.pgconn.close()
        self.msconn.close()
    def rollback(self):
        self.pgconn.rollback()
    def exesyncdb(self):
        mscursor=self.msconn.cursor()
        sql=("SELECT COUNT(COLUMNNAME) AS CT,TABLENAME FROM "\
                 "(SELECT A.NAME AS COLUMNNAME,B.NAME AS TABLENAME FROM SYSCOLUMNS A RIGHT JOIN "\
                 " SYSOBJECTS B ON A.ID=B.ID WHERE B.TYPE='U' AND B.NAME NOT IN ('dtproperties','0626')) A "\
                 " GROUP BY TABLENAME ")
        #print sql
        mscursor.execute(sql)
        table=mscursor.fetchall()
        if(table is None or len(table)<=0):
            return
        else:
            for row in table:
                #print row[1]
                self.executeTable(row[1],row[0])
                print "%s is execute success"%row[1]
    def executeTable(self,tablename,count):
        #print tablename
        sql1="SELECT * FROM %s"%tablename
        mscursor=self.msconn.cursor()
        mscursor.execute(sql1)
        table=mscursor.fetchall()
        if(table is None or len(table)<=0):
            mscursor.close()
            return
        lst_result=self.initColumn(table)
        #print "column"
        mscursor.close()
        sql2=self.initPgSql(tablename,count)
        pgcursor=self.pgconn.cursor()
        pgcursor.executemany(sql2,lst_result)
        pgcursor.close()
    def initPgSql(self,tablename,count):
        columns=[]
        for i in range(count):
            columns.append("%s")
        strs=",".join(columns)
        sql="INSERT INTO %s%s VALUES(%s)"%(TableSpace,tablename,strs)
        return sql
    #-----------------------------
    #字段编码和相关格式初始化
    #-----------------------------
    def initColumn(self,table):
        if(table is None or len(table)<=0):
            return None
        lst_result=[]
        for row in table:
            i=0
            lines=[]
            for column in row:
                if(column is not None and types.StringType==type(column)):
      #lines.append(unicode(column))
                    try:
                        lines.append((column.decode('cp936')).encode('utf-8'))
                    except:
                        lines.append(column)
                else:
                    lines.append(column)
                i+=1
            lst_result.append(lines)
        return lst_result
    #-----------------------
    #测试数据表导入结果测试
    #----------------------
    def exeBulletin(self):
        mscursor=self.msconn.cursor()
        sql=("SELECT * FROM BBULLETIN")
        mscursor.execute(sql)
        table=mscursor.fetchall()
        if(table is None or len(table)<=0):
            mscursor.close()
            return
        lst_result=initColumn(table)
        mscursor.close()
        pgcursor=self.pgconn.cursor()
        ret=pgcursor.executemany("INSERT INTO "+TableSpace+"BBULLETIN VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",lst_result)
        pgcursor.close()
    def getAllTable(self):
        mscursor=self.msconn.cursor()
        sql=("SELECT NAME FROM sysobjects WHERE TYPE='U' AND NAME NOT IN ('dtproperties','0626')")
        mscursor.execute(sql)
        table=mscursor.fetchall()
        if(table is None or len(table)<=0):
            mscursor.close()
            return
        pgcursor=self.pgconn.cursor()
        for row in table:
            sqlext=self.createTable(row[0])
            print (sqlext)
            if(sqlext is not None):
                pgcursor.execute(sqlext)
        mscursor.close()
        pgcursor.close()
    #----------------------
    #根据SQL SERVER数据库基本结构创建PostgreSQL数据库表结构
    #----------------------
    def createTable(self,tablename):
        mscursor=self.msconn.cursor()
       # sql=("SELECT A.NAME AS COLUMNNAME,C.NAME,A.LENGTH,B.NAME AS TABLENAME "\
       #          " FROM SYSCOLUMNS A RIGHT JOIN  SYSOBJECTS B ON A.ID=B.ID "\
       #          " LEFT JOIN SYSTYPES C ON C.XTYPE=A.XTYPE "\
       #          " WHERE B.TYPE='U' AND B.NAME=%s AND B.NAME NOT IN ('dtproperties','BUPLOADCUSTOMER','RFREIGHT')")
        sql=("SELECT A.NAME AS COLUMNNAME,C.NAME,A.LENGTH,B.NAME AS TABLENAME,ISNULL(D.PKS,0) AS PKEY,E.CT "\
                 " FROM SYSCOLUMNS A RIGHT JOIN  SYSOBJECTS B ON A.ID=B.ID "\
                 " LEFT JOIN SYSTYPES C ON C.XTYPE=A.XTYPE LEFT JOIN "\
                 " (SELECT A.NAME,1 AS PKS FROM SYSCOLUMNS A "\
                 " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s)"\
                 " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID "\
                 " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') D "\
                 " ON A.NAME =D.NAME "\
                 " LEFT JOIN (SELECT COUNT(A.COLUMNNAME) AS CT,%s AS TABLENAME  FROM "\
                 " (SELECT A.NAME AS COLUMNNAME,D.NAME AS TABLENAME FROM SYSCOLUMNS A "\
                 " JOIN SYSINDEXKEYS B ON A.ID=B.ID AND A.COLID=B.COLID AND A.ID=OBJECT_ID(%s) "\
                 " JOIN SYSINDEXES C ON A.ID=C.ID AND B.INDID=C.INDID "\
                 " JOIN SYSOBJECTS D ON C.NAME=D.NAME AND D.XTYPE='PK') A GROUP BY A.TABLENAME) E "\
                 " ON B.NAME=E.TABLENAME "\
                 " WHERE B.TYPE='U'  AND B.NAME=%s AND B.NAME NOT IN ('dtproperties') ")
        mscursor.execute(sql,(tablename,tablename,tablename,tablename))
        table=mscursor.fetchall()
        if(table is None or len(table)<=0):
            mscursor.close()
            return
        csql="CREATE TABLE "+TableSpace+"%s ("%tablename
        lst=[]
        for row in table:
            if(row[1]=="int"):
                if(row[4]==1 and len(lst)<=0 and row[5]==1):
                    lst.append(row[0]+" serial PRIMARY KEY NOT NULL")
                elif(row[4]==1 and len(lst)>0 and row[5]==1):
                    lst.append(","+row[0]+" serial PRIMARY KEY NOT NULL")
                elif(row[4]==0 and len(lst)<=0 and row[5]!=0):
                    lst.append(row[0]+" INT DEFAULT 0")
                elif(len(lst)>0):
                    lst.append(","+row[0]+" INT DEFAULT 0")
                else:
                    lst.append(row[0]+" INT DEFAULT 0")
            if(row[1]=="varchar"):
                if(len(lst)<=0):
                    lst.append(row[0]+" varchar("+str(row[2])+")")
                else:
                    lst.append(","+row[0]+" varchar("+str(row[2])+")")
            if(row[1]=="text"):
                if(len(lst)<=0):
                    lst.append(row[0]+" text ")
                else:
                    lst.append(","+row[0]+" text ")
            if(row[1]=="datetime"):
                if(len(lst)<=0):
                    lst.append(row[0]+" timestamp without time zone NULL ")
                else:
                    lst.append(","+row[0]+" timestamp without time zone NULL ")
            if(row[1]=="numeric" or row[1]=="money" or row[1]=="float" or row[1]=="decimal"):
                if(len(lst)<=0):
                    lst.append(row[0]+" decimal(18,2) DEFAULT 0.00 ")
                else:
                    lst.append(","+row[0]+" decimal(18,2) DEFAULT 0.00 ")
            if(row[1]=="bit"):
                if(len(lst)<=0):
                    lst.append(row[0]+" boolean DEFAULT FALSE ")
                else:
                    lst.append(","+row[0]+" boolean DEFAULT FALSE ")
            if(row[1]=="tinyint"):
                if(len(lst)<=0):
                    lst.append(row[0]+" smallint DEFAULT 0 ")
                else:
                    lst.append(","+row[0]+" smallint DEFAULT 0 ")
            if(row[1]=="char"):
                if(len(lst)<=0):
                    lst.append(row[0]+" char("+str(row[2])+")")
                else:
                    lst.append(","+row[0]+" char("+str(row[2])+")")
        lst.append(");")
        mscursor.close()
        return csql+" ".join(lst)
if __name__=="__main__":
    sdb=SyncDataBase()
    try:
        #print sdb.initPgSql("aaa",10)
        #sdb.getAllTable()
        sdb.exesyncdb()
    except Exception,e:
        print e
        sdb.rollback()
    else:
        sdb.commit()
    sdb.close()
    print "ok........"