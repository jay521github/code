#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: 6noble_ApiCase.py
@Auth: Sun dong
@Date: 2022/6/27-16:58
@Desc:
@Ver : 0.0.0
"""
import json
import os
import time
import allure
import jsonpath
import pytest
from conf.yaml_driver import load_yaml
from params.allParams import *
from conf.read_ini import ReadIni

@allure.epic("六合C端回归测试")
class Test_ApiCase():
    formId=None
    scaleId=None
    questionId=None
    answerId=None
    @allure.story("01.获取用户基本信息")
    @allure.severity('normal')
    def test_01(self, Api_Token):
        '''
        1、用户登录系统
        2、查询用户基本信息
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('用户登录获取基本信息')
        ak,token,log = Api_Token
        with allure.step("用户打开链接，登录平台"):
            url = PORD_URL + ReadIni('../conf/config.ini','LOGIN_PATH','path')
            data={
                'token':token,
                'publicKey':publicKey
            }
            res = ak.get(url=url, params=data)
            print(res.json())
            #获取响应中的结果，用于校验是否成功
            account=ak.json_path(res.text,'account')
            assert account=='zdhcd000',log.error('断言失败，没有获取到登录账号')

        return res
    # @pytest.mark.skip
    @allure.story("02.根据状态查询用户相关的测评量表")
    @allure.severity('normal')
    @pytest.mark.parametrize('scale', load_yaml(r'../data/test_scale.yaml'))
    def test_02(self,scale,Api_Token):
        ak,token,log = Api_Token
        allure.dynamic.title(scale['title'])
        with allure.step("根据状态查询用户的相关的测评量表"):
            url = PORD_URL + scale['path']
            data={
                'params':scale['data']['params'],
                'token':token,
                'publicKey':publicKey
            }
            res= ak.post(url=url, data=data)
            print(res.json())
            Test_ApiCase.formId=ak.json_path(res.text,'formId')
            Test_ApiCase.scaleId=ak.json_path(res.text,'scaleId')[0]
            # 获取响应中的结果，用于校验是否成功
            code=ak.json_path(res.text,'code')
            assert code==0,log.error('断言失败，接口没有成功返回数据')

    # @pytest.mark.skip
    @allure.story("03.查询用户量表信息")
    @allure.severity('normal')
    def test_03(self,Api_Token):
        ak,token,log = Api_Token
        allure.dynamic.title('查询用户的量表信息')
        with allure.step("查询用户量表信息"):
            url = PORD_URL + ReadIni('../conf/config.ini','QUERY_PATH','path')
            userdata = {
                'formId':Test_ApiCase.formId,
                'token': token,
                'publicKey':publicKey,
                'params':json.dumps({"params":[Test_ApiCase.scaleId]})
            }
            # #使用json.dumps转换, 转换回双引号
            # data = json.dumps(userdata)
            res = ak.post(url=url, data=userdata)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')

    # @pytest.mark.skip
    @allure.story("04.查询题目以及答案和已答题记录")
    @allure.severity('normal')
    def test_04(self, Api_Token):
        ak,token,log = Api_Token
        allure.dynamic.title('查询题目及做题记录')
        with allure.step("接口返回正确的返回值"):
            url = PORD_URL + ReadIni('../conf/config.ini','ANSWER_PATH','path')
            userdata = {
                'formId': Test_ApiCase.formId,
                'token': token,
                'publicKey': publicKey,
                'scaleId':Test_ApiCase.scaleId
            }
            res = ak.post(url=url, data=userdata)
            print(res.json())
        with allure.step('获取题目及答案'):
            Test_ApiCase.questionId=jsonpath.jsonpath(res.json(),'$.data.result..getEvluationQuestionAndAndwerVo[0].evaluationAnwsers[0].questionId')
            Test_ApiCase.answerId=jsonpath.jsonpath(res.json(),'$.data.result..getEvluationQuestionAndAndwerVo[0].evaluationAnwsers[0].anweserId')
            log.info(f'本次的问题为：{Test_ApiCase.questionId}')
            log.info(f'回答的答案为：{Test_ApiCase.answerId}')
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')

    @pytest.mark.skip
    @allure.story("05.提交答案")
    @allure.severity('normal')
    def test_05(self, Api_Token):
        ak,token,log = Api_Token
        allure.dynamic.title('提交答案')
        with allure.step("提交答案"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'SUBMIT_PATH', 'path')
            userdata = {
                'formId': Test_ApiCase.formId,
                'token': token,
                'publicKey': publicKey,
                'scaleId': Test_ApiCase.scaleId,
                'lastQuestion':1,
                 'params':json.dumps({"params":[{"answerId":Test_ApiCase.answerId,"questionId":Test_ApiCase.answerId,"useTime":1,"answerType":1}]})
            }
            res = ak.post(url=url, data=userdata)
            print(res.json())
            #获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')

    #@pytest.mark.skip
    @allure.story("06.获取form个体报告")
    @allure.severity('normal')
    def test_06(self, Api_Token):
        '''
        1、用户答题完毕
        2、查看生成的报告
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('用获取form个体报告')
        ak, token, log = Api_Token
        with allure.step("作答完毕，查看报告"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'REPORT_PATH', 'path')
            data = {
                'token': token,
                'publicKey': publicKey,
                'formId': 'FORM117403940732220620895022'
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')

    @allure.story("07.获取热门列表")
    @allure.severity('normal')
    def test_07(self, Api_Token):
        '''
        登录首页，查询热门列表
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('获取热门列表')
        ak, token, log = Api_Token
        with allure.step("首页，获取热门列表"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'HOT_LIST_PATH', 'path')
            data = {
                'token': token,
                'publicKey': publicKey
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')
        return res

    @allure.story("08.获取尊享位列表信息")
    @allure.severity('normal')
    def test_08(self, Api_Token):
        '''
        登录首页，查询热门列表
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('获取尊享位列表信息')
        ak, token, log = Api_Token
        with allure.step("首页，获取尊享位列表信息"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'GET_LIST', 'path')
            data = {
                'token': token,
                'publicKey': publicKey
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')
        return res

    @allure.story("09.查看栏目所有内容")
    @allure.severity('normal')
    def test_09(self, Api_Token):
        '''
        查看精选文章
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('查看精选文章')
        ak, token, log = Api_Token
        with allure.step("首页，查看精选文章"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'FIND_CONTENTS', 'path')
            data = {
                'token': token,
                'publicKey': publicKey,
                'rangePage':'topic_classes',
                'rangeColumn':113696311900058828828152,
                'isAdmin':0,
                'rangeColumnSecond': None
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')
        return res

    @allure.story("10.查看冥想音乐")
    @allure.severity('normal')
    def test_10(self, Api_Token):
        '''
        查看冥想音乐
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('查看冥想音乐')
        ak, token, log = Api_Token
        with allure.step("首页，查看冥想音乐"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'FIND_CONTENTS', 'path')
            data = {
                'token': token,
                'publicKey': publicKey,
                'rangePage': 'topic_classes',
                'rangeColumn': 113671913460885504006733,
                'isAdmin': 0,
                'rangeColumnSecond': None
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')
        return res

    @allure.story("11.查看推荐课程")
    @allure.severity('normal')
    def test_11(self, Api_Token):
        '''
        查看推荐课程
        '''
        # 动态获取参数生成标题
        allure.dynamic.title('查看推荐课程')
        ak, token, log = Api_Token
        with allure.step("首页，查看推荐课程"):
            url = PORD_URL + ReadIni('../conf/config.ini', 'FIND_CONTENTS', 'path')
            data = {
                'token': token,
                'publicKey': publicKey,
                'rangePage': 'topic_classes',
                'rangeColumn': '5f0a6538a9780b9f43d9fc223278e199',
                'isAdmin': 0,
                'rangeColumnSecond': None
            }
            res = ak.post(url=url, data=data)
            print(res.json())
            # 获取响应中的结果，用于校验是否成功
            code = ak.json_path(res.text, 'code')
            assert code == 0, log.error('断言失败，接口没有成功返回数据')
        return res
if __name__ == '__main__':
    pytest.main(['-s', 'Regression_Api.py', '-v'])
    # time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # pytest.main(['-v', 'Regression_Api.py', '--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    # os.system('allure serve ./result/{}'.format(time_str))