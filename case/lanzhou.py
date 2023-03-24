#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
import allure
import os
import time

from conf.yaml_driver import load_yaml
from excel.excel_read import read_excel
from conf.read_ini import ReadIni
from params.allParams import *

@pytest.mark.parametrize('login',load_yaml('../data/mobile_account.yaml'))
@allure.title('登录6合测评前端')
def test_01(login,Login):
    '''
    1、打开链接
    2、登录账号，密码
    3、进入首页，点击量表，开始测评
    4、测评完毕，查看个人报告
    '''
    #获取用户的账号，密码信息
    user=read_excel()
    account=choice(user)
    wk,log=Login
    # log.info(f'本次参与测评的用户账号为：{account}')
    log.info('----------------------------------------本次自动化测试开始执行-------------------------------------------')
    url=ReadIni('../conf/config.ini','PORD_PC_SERVER','url')
    # log.info(f'本次打开的链接为：{url}')
    wk.open(url)
    #登录账号
    wk.input('xpath',UESRNAME,account)
    # wk.input('xpath',UESRNAME,login['username'])
    #登录密码
    wk.input('xpath',PASSWORD,'a123456')
    # log.info(f'本次参与测评的用户账号为：{login["username"]}')
    #勾选协议
    wk.click('xpath',CHECKBOX)
    #点击登录
    wk.click('xpath','//span[text()="登录"]')
    log.info('登录成功')
    wk.wait(2)
@allure.title('登录到首页')
def test_02(Login):
    wk,log=Login
    get_text=wk.get_text(NEW_PASSWORD)
    try:
        assert get_text == '设置新密码', log.error('没有获取到设置新密码的弹窗信息')
        if get_text=='设置新密码':
            #设置新密码
            with allure.step('1、点击X，关闭设置密码弹窗'):
                wk.click('xpath',X)
                wk.wait(1)
                log.info('已经关闭了设置新密码的弹窗')
                log.info('点击量表')
                wk.wait(1)
    except Exception as e:
        print(e)
@allure.title('点击我的测评开始答题')
def test_03(Login):
    wk, log = Login
    allure.dynamic.title('点击我的测评开始答题')
    wk.mouse_hold('//*[@id="app"]/div/div[1]/div/div/div[3]/div/span/span[2]')
    wk.wait(1)
    wk.click('xpath', '//*[text()="个人中心"]')
    wk.wait(1)
    wk.click('xpath', '//*[text()="我的测评"]')
    wk.wait(1)
    wk.click('xpath', '//*[text()="已测评"]')
    wk.wait(2)
    num=wk.get_text('//*[@id="pane-complete"]/div/div[2]/div/span[1]')
    if num =="共 0 条":
        wk.click('xpath', '//*[text()="待测评"]')
        wk.wait(2)
        wk.click('xpath','//*[text()=" 开始测试 "]')
        log.info('点击开始答题')
        wk.wait(2)
        wk.click('xpath', Start_the_topic)
        log.info('点击下一步')
        # wk.click('xpath', NEXT)
        wk.click('xpath', '//*[text()=" 下一步 "]')
        wk.wait(2)
        grade_title=wk.get_text('//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/div[1]/span')
        title='中小学生心理健康量表'
        if title in grade_title:
            #选择年级
            wk.click('xpath','//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/div[2]/form/div[1]/div/div/div/div/input')
            grades = [grade_four, grade_five, grade_six]
            grade=choice(grades)
            ck_l = wk.web_el_wait('xpath', grade)
            ck_l.click()
            # wk.click('xpath','//span[text()="三年级"]')
            #填写班级
            # wk.click('xpath','//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/div[2]/form/div[5]/div/div/div/input')
            wk.input('xpath','//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/div[2]/form/div[2]/div/div/div/input','8班')
           #选择性别
            wk.click('xpath',
                     '//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/div[2]/form/div[3]/div/div/div/div/input')
            sexs = [sex1, sex2]
            sex = choice(sexs)
            ck_l = wk.web_el_wait('xpath', sex)
            ck_l.click()
            wk.wait(1)
            log.info('点击开始测评按钮')
            # wk.click('xpath', Enter_the_assessment)
            wk.click('xpath','//*[@id="app"]/div/div[2]/div/div[1]/div/div/div/div/button')
            wk.wait(1)
            log.info('开始答题')
            wk.wait(3)
            with allure.step('1.系统获取到当前答题数/总答题数'):
                max_num = int(wk.get_text(status_num_total))
                min_num = int(wk.get_text(status_num_play))
            with allure.step('2.获取到答题的坐标系数，准备定位答案按钮'):
                answers = [Very_much, relatively_match, indeterminacy, Comparative_incompatibility,
                           Very_out_of_line]
            while min_num <= max_num:
                wk.wait(0.5)
                answer = choice(answers)
                ck_l = wk.web_el_wait('xpath', answer)
                ck_l.click()
                log.info(f'正在回答第:{min_num}题')
                min_num += 1
                # 答题完毕，点击提交
            wk.click('xpath', '//span[text()="提交"]')
            wk.wait(5)
            log.info('报告已生成，释放资源，关闭浏览器')
            wk.quit()
    else:
        log.info('该学员已完成测评，程序关闭')
        wk.quit()

@pytest.mark.skip
@allure.title('查看报告')
def test_04(Login):
    wk,log=Login
    log.info('**************正在浏览测评报告****************')
    report_text = wk.get_text(REPORT_TEXT)
    assert '报告' in report_text,log.error('报告未生成')
    n = 0
    while n <= 99:
        wk.wait(0.5)
        wk.down_scroll()
        n += 1
        log.info(f'浏览报告进度为：{n}%')
    wk.wait(1)

@pytest.mark.skip
@allure.title('我的测评')
def test_05(Login):
    wk,log=Login
    allure.dynamic.title('悬停点击')
    wk.mouse_hold('//*[@id="app"]/div/div[1]/div/div/div[3]/div/span/span[2]')
    wk.wait(1)
    wk.click('xpath', '//*[text()="个人中心"]')
    wk.wait(1)
    wk.click('xpath','//*[text()="我的测评"]')
    wk.wait(1)
    wk.click('xpath','//*[text()="已测评"]')
    wk.wait(2)
    with allure.step('查询已测评，检验报告是否生成成功'):
        expected_result = wk.get_text('//*[@id="pane-complete"]/div/div[1]/div/div[3]/div[2]/button')
        assert expected_result == "查看报告" or "测评完成", log.error(f"生成报告失败，没有找到{expected_result}的按钮")

if __name__ == '__main__':
    pytest.main(['-s','lanzhou.py','-v'])
    # time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # pytest.main(['-v', '6noble.py','--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    # os.system('allure serve ./result/{}'.format(time_str))
    # os.system('allure generate ./result/{}.format(time_str) --clean')
