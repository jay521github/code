#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: screenshot.py
@Auth: Sun dong
@Date: 2022/11/21-16:11
@Desc: 
@Ver : 0.0.0
"""
import pytest
import allure
import os
import time
from conf.read_ini import ReadIni
from selenium.webdriver.support.select import Select
from conf.yaml_driver import load_yaml
from params.allParams import *
from conf.random_data import get_random
#from conf.upload import UpLoad
@pytest.mark.parametrize('login',load_yaml('../data/account.yaml'))
@allure.epic('登录oms系统')
@allure.story('登录oms系统')
@allure.title('登录6合oms后台')
def test_01(login,Login):
    wk,log=Login
    log.info('----------------------------------------本次自动化测试开始执行-------------------------------------------')
    url = ReadIni('../conf/config.ini', 'PORD_OMS_SERVER', 'url')
    wk.open(url)
    allure.dynamic.title(login['title'])
    log.info(f'后台的网址为：{url}')
    #登录账号
    wk.input('id','normal-login_account',login['username'])
    #登录密码
    wk.input('id','normal-login_password','Jsbyyds9527')
    #点击登录
    wk.click('xpath',login['button'])
    log.info('登录成功')
    wk.wait(3)
@allure.epic('测评管理')
@allure.severity('normal')
@allure.story('量表管理')
def test_02(Login):
    wk, log = Login
    allure.dynamic.title('获取量表列表截图')
    with allure.step('点击进入测评管理'):
        wk.wait(3)
        wk.click('xpath','//span[text()="测评管理"]')
    with allure.step('点击进入量表管理'):
        wk.wait(1)
        wk.click('xpath','//a[text()="量表管理"]')
    with allure.step('查询维度'):
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        path='../'+time_str+'.PNG'
        wk.wait(2)
        wk.click('xpath', '//span[text()="查询"]')
        wk.screenshot(path)
        allure.attach.file(source=path,name='量表截图',attachment_type=allure.attachment_type.PNG)

        # text=wk.get_text('//*[@id="root"]/div/section/section/header/div/div[1]/p[2]')
        # assert text=='量表管理'
if __name__ == '__main__':
    # pytest.main(['-s','oms.py','-v'])
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    pytest.main(['-v','--reruns','1','--reruns-delay','2','screenshot.py', '--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    os.system('allure serve ./result/{}'.format(time_str))