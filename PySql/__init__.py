import config.config
import flask
import json
import time
from ast import Try
import pymysql
from flask import Flask, request, render_template

SqlCon = config.config.MYSQL_INFO  # MySql配置

# 链接数据库
DB = pymysql.connect(host=SqlCon['host'], port=SqlCon['port'], user=SqlCon['user'], password=SqlCon['pass'],
                     database=SqlCon['db'], charset=SqlCon['charset'])


# 添加操作
def add(sql):
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        curser = DB.cursor()
        curser.execute(sql)
        DB.commit()
        curser.close()
        return [200, '添加成功', None]
    except:
        DB.rollback()  # 发生错误，回滚
        return [400, '添加失败', None]


# 删除操作
def delete(sql):
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        curser = DB.cursor()
        curser.execute(sql)
        DB.commit()
        curser.close()
        return [200, '删除成功', None]
    except:
        DB.rollback()  # 发生错误，回滚
        return [400, '删除失败', None]


# 更新操作
def modify(sql):
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        curser = DB.cursor()
        curser.execute(sql)
        DB.commit()
        curser.close()
        return [200, '更新成功', None]
    except:
        DB.rollback()  # 发生错误，回滚
        return [400, '更新失败', None]


# 查看操作
def check(sql):
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        curser = DB.cursor()
        curser.execute(sql)
        ret = curser.fetchone()
        DB.commit()
        curser.close()
        return [200, '查看成功', ret]
    except:
        DB.rollback()  # 发生错误，回滚
        return [400, '查看失败', None]


# 判断id是否存在
def ids(sql):
    curser = DB.cursor()
    curser.execute(sql)
    ret = curser.fetchone()
    if ret is None:
        return False
    else:
        return True


# 列表操作
def list(sql):
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        curser = DB.cursor()
        curser.execute(sql)
        ret = curser.fetchall()
        DB.commit()
        curser.close()
        return [200, '列表初始化成功', ret]
    except:
        DB.rollback()  # 发生错误，回滚
        return [400, '列表初始化失败', None]
