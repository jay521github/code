#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: mysql.py
@Auth: Sun dong
@Date: 2022/6/30-16:48
@Desc: 
@Ver : 0.0.0
"""
import pymysql

db = pymysql.connect(host='mercury.6noble.net',
                     user='root',
                     port=3306,
                     password='root@6no',
                     database='db_ucenter',
                     charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SSELECT account FROM ucenter_user_base")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print(data)
print("数据库连接成功！")
# 关闭数据库连接
db.close()