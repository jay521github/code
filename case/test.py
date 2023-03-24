#coding=utf-8
import pytest
import allure
import os
import time
from conf.yaml_driver import load_yaml
from params.allParams import *


@pytest.mark.parametrize('login',load_yaml('../data/account.yaml'))
@allure.title('登录6合测评前端')
def test_01(login,Login):
    '''
    1、打开链接
    2、登录账号，密码
    3、进入首页，点击量表，开始测评
    4、测评完毕，查看个人报告
    '''
    wk,log=Login
    wk.open(login['url'])
    wk.input('xpath',UESRNAME,login['username'])
    wk.input('xpath',PASSWORD,login['password'])
    wk.click('xpath',CHECKBOX)
    wk.click('xpath','//span[text()="登录"]')
    log.info('登录成功')
    wk.wait(3)
@allure.title('登录到首页')
def test_02(Login):
    wk,log=Login
    get_text=wk.get_text(NEW_PASSWORD)
    try:
        if get_text=='设置新密码':
            #设置新密码
            wk.click('xpath',X)
            wk.wait(3)
            log.info('已经关闭了设置新密码的弹窗')
    except Exception as e:
        print(e)
@allure.title('开始答题')
@pytest.mark.skip(reason="no env,can't test")
def test_03(Login):
    wk,log=Login
    log.info('开始答题')
    wk.wait(2)
    max_num = int(wk.get_text(status_num_total))
    min_num = int(wk.get_text(status_num_play))
    ck_l=wk.web_el_wait('xpath', Totally_Agree)
    print(min_num,max_num)
    while min_num<=max_num:
        wk.wait(1)
        ck_l = wk.web_el_wait('xpath', Totally_Agree)
        ck_l.click()
        log.info(f'正在回答第:{min_num}题')
        min_num+=1
    #答题完毕，点击提交
    wk.click('xpath','//span[text()="提交"]')
    wk.wait(5)
@pytest.mark.skip(reason="no env,can't test")
@allure.title('查看报告')
def test_04(Login):
    wk,log=Login
    allure.dynamic.title('滑动到底部')
    wk.scroll_foot()
    wk.wait(1)
    allure.dynamic.title('滑动到顶部')
    wk.scroll_top()
    wk.wait(1)
    allure.dynamic.title('悬停点击')
    wk.mouse_hold('	https://pc.6noblexc.com/img/photo_woman.ed916e5f.png')
@allure.title('个人中心')
def test_05(Login):
    wk,log=Login
    wk.wait(1)
    allure.dynamic.title('悬停点击')
    wk.mouse_hold('//*[@id="app"]/div/div[1]/div/div/div[3]/div/span')
    wk.wait(1)
    wk.click('xpath','//*[text()="个人中心"]')
    wk.wait(1)
@allure.title('我的测评')
def test_06(Login):
    wk,log=Login
    wk.click('xpath','//*[text()="我的测评"]')
    wk.wait(1)
    wk.click('xpath','//*[text()="已测评"]')
    wk.wait(4)
if __name__ == '__main__':
    # pytest.main(['-s','6noble.py','-v'])
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    pytest.main(['-s', '-v', 'test.py','--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    os.system('allure serve ./result/{}'.format(time_str))
    # os.system('allure generate ./result/{}.format(time_str) --clean')