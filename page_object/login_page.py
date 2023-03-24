#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: login_page.py
@Auth: Sun dong
@Date: 2022/7/1-13:51
@Desc: 
@Ver : 0.0.0
"""
import pytest
import allure
import os
import time
from conf.yaml_driver import load_yaml
from params.allParams import *
from excel.excel_read import read_excel
class LoginPage():
    @pytest.mark.parametrize('login',load_yaml('../data/account.yaml'))
    @allure.title('登录6合测评前端')
    def Login_page(login,Login):
        '''
        1、打开链接
        2、登录账号，密码
        3、进入首页，点击量表，开始测评
        4、测评完毕，查看个人报告
        '''
        user=read_excel()
        account=choice(user)
        wk,log=Login
        log.info(f'本次参与测评的用户账号为：{account}')
        log.info('----------------------------------------本次自动化测试开始执行-------------------------------------------')
        wk.open(login['url'])
        log.info(f'打开本次测评链接地址为：{login["url"]}')
        wk.input('xpath',UESRNAME,account)
        wk.input('xpath',PASSWORD,login['password'])
        wk.click('xpath',CHECKBOX)
        wk.click('xpath','//span[text()="登录"]')
        log.info('登录成功')
        wk.wait(3)
    @allure.title('登录到首页')
    def Home_page(Login):
        wk,log=Login
        get_text=wk.get_text(NEW_PASSWORD)
        try:
            if get_text=='设置新密码':
                #设置新密码
                with allure.step('1、点击X，关闭设置密码弹窗'):
                    wk.click('xpath',X)
                    wk.wait(1)
                    log.info('已经关闭了设置新密码的弹窗')
                    log.info('点击量表')
                    wk.wait(1)
                with allure.step('2、在首页点击测评量表'):
                    wk.click('xpath',SCALE)
                    wk.wait(1)
                with allure.step('3、点击开始答题按钮'):
                    log.info('点击开始答题')
                    wk.click('xpath', Start_the_topic)
                with allure.step('4、点击下一步按钮'):
                    log.info('点击下一步')
                    wk.click('xpath', NEXT)
                with allure.step('5、点击开始测评按钮，准备作答'):
                    log.info('点击开始测评按钮')
                    wk.click('xpath', Enter_the_assessment)
        except Exception as e:
            print(e)