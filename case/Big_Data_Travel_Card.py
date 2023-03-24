#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: Big_Data_Travel_Card.py
@Auth: Sun dong
@Date: 2022/6/29-17:52
@Desc: 
@Ver : 0.0.0
"""
import json
import os
import random
from random import *
import time
import allure
import jsonpath
import pytest
from conf.yaml_driver import load_yaml
from params.allParams import *
from conf.read_ini import ReadIni

@allure.epic("大数据行程卡")
class Test_Travel_Card():
    formId = None
    scaleId = None
    questionId = None
    answerId = None
    @allure.story("01.查询用户是否有测试量表")
    @allure.severity('normal')
    def test_01(self, SMS_Token):
        '''
        1、填写手机号
        2、发送短信验证码
        3、填写验证码，登录获取token
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('查询用户是否显示测评量表')
        ak,token,log = SMS_Token
        with allure.step("验证码登录，首页显示测评量表"):
            url = DEV_URL + ReadIni('../conf/config.ini','ASSESSMENT_PATH','path')
            data={
                'token':token,
                'publicKey':publicKey
            }
            res = ak.get(url=url, params=data)
            Test_Travel_Card.formId = ak.json_path(res.text, 'formId')
            Test_Travel_Card.scaleId = ak.json_path(res.text, 'scaleId')[0]
            print(res.json())

    @allure.story("02.查询题目以及答案和已答题记录")
    @allure.severity('normal')
    def test_04(self, SMS_Token):
        ak, token, log = SMS_Token
        allure.dynamic.title('查询题目及做题记录')
        with allure.step("接口返回正确的返回值"):
            url = DEV_URL + ReadIni('../conf/config.ini', 'ANSWER_PATH', 'path')
            userdata = {
                'formId': Test_Travel_Card.formId,
                'token': token,
                'publicKey': publicKey,
                'scaleId': Test_Travel_Card.scaleId
            }
            res = ak.post(url=url, data=userdata)
        with allure.step('获取题目及答案'):
            print(res.json())
            Test_Travel_Card.questionId=jsonpath.jsonpath(res.json(),'$.data..evaluationQuestions.questionId')[1]
            # for i in questionIds:
            #     print("序号：%s   值：%s" % (questionIds.index(i) + 1, i))
            Test_Travel_Card.answerId=ak.json_path(res.text,'anweserId')[1]
            # for i in anweserId:
            #     print ("序号：%s   值：%s" % (anweserId.index(i) + 1, i))


    @allure.story("03.提交答案")
    @allure.severity('normal')
    def test_05(self, SMS_Token):
        ak, token, log = SMS_Token
        allure.dynamic.title('提交答案')
        with allure.step("提交答案"):
            url = DEV_URL + ReadIni('../conf/config.ini', 'SUBMIT_PATH', 'path')
            userdata = {
                'formId': Test_Travel_Card.formId,
                'token': token,
                'publicKey': publicKey,
                'scaleId': Test_Travel_Card.scaleId,
                'lastQuestion': 1,
                'params': json.dumps({"params": [
                    {"answerId": Test_Travel_Card.answerId, "questionId": Test_Travel_Card.questionId, "useTime": 1,
                     "answerType": 1}]})
            }
            res = ak.post(url=url, data=userdata)
            print(res.json())

    @allure.story("04.获取form个体报告")
    @allure.severity('normal')
    def test_06(self, SMS_Token):
        '''
        1、用户答题完毕
        2、查看生成的报告
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('用获取form个体报告')
        ak, token, log = SMS_Token
        with allure.step("作答完毕，查看报告"):
            url = DEV_URL + ReadIni('../conf/config.ini', 'REPORT_PATH', 'path')
            data = {
                'token': token,
                'publicKey': publicKey,
                'formId': Test_Travel_Card.formId
            }
            res = ak.get(url=url, params=data)
            print(res.json())
if __name__ == '__main__':
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    pytest.main(['-v', 'Big_Data_Travel_Card.py', '--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    os.system('allure serve ./result/{}'.format(time_str))
    # pytest.main(['-s','Big_Data_Travel_Card.py'])