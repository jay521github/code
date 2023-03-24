# -*- coding: UTF-8 -*-
"""
@author:Sun Dong
@file:conftest.py
@time:2022/03/11
"""
import os
import allure
import pytest
from KeyWords.Api_Keys import api_keys
from KeyWords.keyword_web import WebKeys
import random
from conf.read_ini import ReadIni
from conf.yaml_driver import load_yaml
from conf.log import Logger
import jsonpath

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport():
    #获取测试用例执行结果，yield返回result对象
    out = yield
    report = out.get_result()
    #仅仅获取用例call阶段的执行结果，不包含setup和teardown
    if report.when == 'call':
        #获取用例call执行结果为失败的情况
        xfail = hasattr(report,'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            #添加allure报告截图
            with allure.step('添加失败截图:'):
                allure.attach(wk.driver.get_screenshot_as_png(),'失败截图',
                              allure.attachment_type.PNG)
#项目级fix，整个项目只初始化一次
@pytest.fixture(scope='session')
# @pytest.mark.parametrize('login',load_yaml('../data/account.yaml'))
@allure.title('初始化工具类')
def Login():
    # 初始化工具类
    global wk,log
    wk=WebKeys('Chrome')
    log=Logger.get_logger(Logger)
    return wk,log


@pytest.fixture(scope='session')
@allure.title('获取用户token')
def Api_Token():
    ak=api_keys()
    log = Logger.get_logger(Logger)
    url = 'https://hapi.6noblexc.com/api/6nobleapi/ucenter/login'
    data={
        'account':'zdhcd000',
        'password':'e10adc3949ba59abbe56e057f20f883e',
        'publicKey':'pvj9bTwwaY4YdPiwRBH5RE25o9ZM8BHG'
    }
    with allure.step("发送登录接口请求，并生成用户的token，整个项目仅生成一次"):
        res=ak.post(url=url,data=data)
        token=ak.json_path(res.text,'token')
        return ak,token,log

@pytest.fixture(scope='session')
@allure.title('登录oms获取token')
def OMS_Token():
    ak=api_keys()
    log = Logger.get_logger(Logger)
    url = 'https://omsapi.6noblexc.com/api/6nobleadmin/ucenterPC/userManage/loginPC'
    data={
        'account':17611593986,
        'password':'e10adc3949ba59abbe56e057f20f883e'
    }
    with allure.step("登录oms后台，登录成功，生成用户的token，整个项目仅生成一次"):
        res=ak.post(url=url,data=data)
        token=jsonpath.jsonpath(res.json(),'$.data.result.token')
        return ak,token,log
