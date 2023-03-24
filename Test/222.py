#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: 222.py
@Auth: Sun dong
@Date: 2022/6/30-17:52
@Desc: 
@Ver : 0.0.0
"""
# import openpyxl
# excel=openpyxl.load_workbook('../data/login_test_account.xlsx')
# sheet=excel['学生名单']
# for i in sheet.values:
#     if type(i[0]) is int:
#         print(i[1])
# import configparser
# def readini(path,name,value):
#     conf=configparser.ConfigParser()
#     conf.read(path)
#     a=conf.get(name,value)
#     return a
#
# import yaml
# def readyaml(path):
#     file=open(path,'r',encoding='utf-8')
#     data=yaml.load(file,Loader=yaml.FullLoader)
#     return data
import random
import sys

from loguru import logger
# import os
# logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
# logger.debug('error')
logger.add("out.log", backtrace=True, diagnose=True) # Caution, may leak sensitive data in prod
# import notifiers
#
# params = {
#     "username": "374074353@qq.com",
#     "password": "jwshan024751",
#     "to": "472073421@qq.com"
# }
#
# # 初始化时发送一封邮件
# notifier = notifiers.get_notifier("qq")
# notifier.notify(message="The application is running!", **params)
# # 发生Error日志时，发邮件进行警报
# from notifiers.logging import NotificationHandler
#
# handler = NotificationHandler("qq", defaults=params)
# logger.add(handler, level="ERROR")
#
#
#
# def func(a, b):
#     return a / b
#
# def nested(c):
#     try:
#         func(5, c)
#     except ZeroDivisionError:
#         logger.exception("What?!")
#
# nested(0)
# list=[random.randrange(100) for _ in range(1000000)]
# # def aaa():
# #     un=[]
# #     for i in list:
# #         if i not in un:
# #             un.append(i)
# #     return un
# mylist=(x*x for x in range(5))
# for i in mylist:
#     print(i)
# a={'name':'小梦','age':'28','color':'白色',"性格":"温和"}
# for i in a.items():
#     print(i)
# a=lambda x,y:x*y
# # print(a(x=1,y=3))
# def sum(fuc):
#     mub=5
#     print('外')
#     def inner():
#         result=fuc()+mub
#         print('内')
#         return result
#     print('装饰器')
#     return inner
# @sum
# def aaa():
#     return 10
# print(aaa())
# a='123\000333'
# print(a)
str = 'LLOVETEST'
print(str.capitalize())
print(str.casefold())
print(str.lower())
print(str.upper())
print(str.swapcase())