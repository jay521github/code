#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: oms.py
@Auth: Sun dong
@Date: 2022/7/5-18:49
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
@pytest.mark.parametrize('login',load_yaml('./data/account.yaml'))
@allure.epic('登录oms系统')
@allure.story('登录oms系统')
@allure.title('登录6合oms后台')
def test_01(login,Login):
    wk,log=Login
    log.info('----------------------------------------本次自动化测试开始执行-------------------------------------------')
    url = ReadIni('./conf/config.ini', 'DEV_OMS_SERVER', 'url')
    wk.open(url)
    allure.dynamic.title(login['title'])
    log.info(f'后台的网址为：{url}')
    #登录账号
    wk.input('id','normal-login_account',login['username'])
    #登录密码
    wk.input('id','normal-login_password',login['password'])
    #点击登录
    wk.click('xpath',login['button'])
    log.info('登录成功')
    wk.wait(2)
    text=wk.get_text(login['text'])
    assert text=='预警大屏',log.error('登录失败')
@pytest.mark.skip
#@pytest.mark.parametrize('content',load_yaml('./data/content.yaml'))
@allure.epic('内容管理')
@allure.severity('normal')
@allure.story('内容列表')
def test_02(Login,content):
    wk, log = Login
    allure.dynamic.title(content['title'])
    with allure.step(('1、点击内容管理菜单')):
        log.info('进入内容管理菜单')
        # wk.click('xpath',content['content_management'])
        wk.click('xpath','//span[text()="内容管理"]')
    with allure.step('2、点击内容列表'):
        wk.click('xpath',content['content_list'])
    wk.wait(1)
    with allure.step('3、点击新增内容'):
        wk.click('xpath',content['newly_content'])
    with allure.step('新增内容:1、选择页面'):
        wk.click('id','rangePage')
        wk.click('xpath','//div[text()="专题课程"]')
        wk.click('xpath','//div[text()="主题冥想"]')
        wk.click('xpath','//div[text()="缓解焦虑"]')
    with allure.step('新增内容:2、填写内容标题'):
        CT='测试标题TestNo.'+str(get_random(1,999))
        wk.input('id','title',CT)
    with allure.step('新增内容:3、选择内容类型'):
        wk.click('id','contentType')
        wk.click('xpath','//div[text()="音频"]')
    with allure.step('新增内容:4、上传音频文件'):
        wk.Mouse_Click('xpath','//span[text()="选择文件"]')
        mp3 = os.path.abspath('测试音频.mp3')
        # wk.wait(2)
        # UpLoad(mp3)
        # wk.wait(4)
    with allure.step('新增内容:5、上传主题配图'):
        png1 = os.path.abspath('微信截图_20220622155317.png')
        png2 = os.path.abspath('微信截图_20220622155606.png')
        wk.click('xpath','//div[text()="上传"]')
        # wk.wait(2)
        # UpLoad(png1)
        # wk.wait(1)
        # wk.click('xpath', '//div[text()="上传"]')
        # wk.wait(2)
        # UpLoad(png2)
        # wk.wait(3)
    with allure.step('新增内容：6、上架设置'):
        wk.click('xpath','//span[text()="立即上架"]')
        wk.wait(2)
    # with allure.step('新增内容：7、上传附件'):
    #     wk.click('xpath',content['attach_path'])
    #     wk.wait(2)
    #     attach=os.path.abspath('Traceback.pdf')
    #     UpLoad(attach)
    with allure.step('新增内容：8、点击提交按钮'):
        wk.click('xpath','//span[text()="提 交"]')
        wk.wait(2)
    with allure.step('校验添加内容是否成功'):
        wk.input('id','advanced_search_title',CT)
        wk.click('xpath', '//span[text()="查询"]')
        expected_result=wk.get_text(content['expected_result'])
        assert expected_result==CT,log.error(f'添加内容失败，没有找到内容标题为{CT}的新增内容')
#@pytest.mark.skip
@pytest.mark.parametrize('organization',load_yaml('./data/organizational_management.yaml'))
@allure.epic('组织管理')
@allure.severity('normal')
@allure.story('机构管理')
def test_03(Login,organization):
    wk, log = Login
    allure.dynamic.title(organization['title'])
    '''
          1、输入机构名称
          2、点击新增机构
          3、输入机构名称
          4、点击新增用户
          5、选择北京|北京市|西城区|
          6、选择制造业
          7、选择教育行业
          8、输入联系人，手机号
          9、点击提交
          '''
    with allure.step('点击进入组织机构'):
        wk.click('xpath','//span[text()="组织管理"]')
    with allure.step('点击进入机构管理'):
        wk.click('xpath','//a[text()="机构管理"]')
    with allure.step('点击进入新增机构'):
        wk.click('xpath',organization['new_agency'])
    with allure.step('输入机构名称'):
        agency_title='测试机构No.'+str(get_random(1,999))
        wk.input('id','advanced_search_officeName',agency_title)
    with allure.step('点击新增用户'):
        wk.click('xpath',organization['add_user'])
    with allure.step('选择地区'):
        wk.click('xpath','//div[text()="北京"]')
        wk.click('xpath', '//div[text()="北京市"]')
        wk.click('xpath', '//div[text()="西城区"]')
    with allure.step('点击行业类型，选择行业'):
        wk.click('id','advanced_search_industryType')
        wk.click('xpath','//div[text()="制造业"]')
    with allure.step('点击客户类型，选择行业'):
        wk.click('id','advanced_search_officeType')
        wk.click('xpath','//div[text()="教育"]')
    with allure.step('输入联系人，手机号'):
        wk.input('id','advanced_search_leader',organization['Contact'])
        wk.input('id','advanced_search_phone',organization['phone'])
    with allure.step('点击提交'):
        wk.click('xpath',organization['submit'])
        wk.wait(3)
    with allure.step('查询新增的机构，检验新增是否成功'):
        wk.input('id','advanced_search_officeName',agency_title)
        wk.click('xpath','//span[text()="查询"]')
        expected_result=wk.get_text(organization['expected_result'])
        assert expected_result==agency_title,log.error(f"添加机构失败，没有找到机构标题为{agency_title}的机构信息")
#@pytest.mark.skip
@pytest.mark.parametrize('user',load_yaml('./data/user_management.yaml'))
@allure.epic('组织管理')
@allure.severity('normal')
@allure.story('用户管理')
def test_04(Login,user):
    wk, log = Login
    allure.dynamic.title(user['title'])
    with allure.step('点击进入组织机构'):
        wk.click('xpath','//span[text()="组织管理"]')
    with allure.step('点击进入用户管理'):
        wk.click('xpath','//a[text()="用户管理"]')
    with allure.step('点击进入新增用户'):
        wk.click('xpath',user['add_user'])
    with allure.step('点击组织机构'):
        wk.click('xpath',user['Organization'])
        wk.click('xpath','//span[text()="兰州教育局测试"]')
        wk.click('xpath','//*[@id="root"]/div/section/section/main/div/ul')
    with allure.step('选择账号类型'):
        wk.click('id','advanced_search_accountType')
        wk.click('xpath','//div[text()="学号"]')
        study_num=get_random(1,99999999)
        wk.input('id','advanced_search_account',study_num)
    with allure.step('选择性别'):
        wk.click('xpath',user['sex'])
    with allure.step('选择生日'):
        wk.click('id','advanced_search_birthStamp')
        wk.wait(2)
        wk.click('xpath',user['age'])
    with allure.step('保存数据'):
        wk.click('xpath','//span[text()="保存完善资料"]')
        wk.wait(2)
    with allure.step('查询新增的用户，检验新增是否成功'):
        wk.input('id','advanced_search_accountOrId',study_num)
        wk.click('xpath','//*[text()="查询"]')
        expected_result=wk.get_text(user['expected_result'])
        assert int(expected_result)==study_num,log.error(f"添加用户失败，没有找到用户为{study_num}的新增用户")
#@pytest.mark.skip
@pytest.mark.parametrize('evaluation',load_yaml('./data/Measurement_management.yaml'))
@allure.epic('测评管理')
@allure.severity('normal')
@allure.story('因子管理')
def test_05(Login,evaluation):
    wk, log = Login
    allure.dynamic.title(evaluation['title'])
    with allure.step('点击进入测评管理'):
        wk.click('xpath','//span[text()="测评管理"]')
    with allure.step('点击进入因子管理'):
        wk.click('xpath','//a[text()="因子管理"]')
    with allure.step('点击进入新增因子'):
        wk.click('xpath',evaluation['new_factor'])
    with allure.step('输入因子名称'):
        factor_name='测试因子No.'+str(get_random(1,999))
        wk.input('id','factor_search_name',factor_name)
    with allure.step('保存并下一步'):
        wk.scroll_foot()
        wk.click('xpath','//span[text()="保存并下一步"]')
    with allure.step('选择题目模块'):
        wk.click('xpath','//span[text()="选择题目"]')
        wk.wait(1)
        #checkbox,选择题目
        checkboxes = wk.locators('css selector', evaluation['check_box'])
        for checkbox in checkboxes:
            wk.wait(0.5)
            checkbox.click()
        #提交选择的题目
        wk.click('xpath','//span[text()="提 交"]')
        wk.wait(2)
        #等待页面加载完成，点击保存并下一步
        wk.click('xpath','//span[text()=" 保存并下一步"]')
    with allure.step('因子得分模块'):
        #点击因子得分
        wk.click('id','advanced_search_rulesId')
        #选择计分方式
        wk.click('xpath','//div[text()="求平均值"]')
        wk.click('xpath',evaluation['next'])
    with allure.step('结果解释模块'):
        #点击添加选项按钮
        wk.click('xpath','//span[text()="添加选项"]')
        wk.wait(2)
        #填入最小值
        wk.input('id','tableForm_0_minScore',1)
        #填入最大值
        wk.input('id', 'tableForm_0_maxScore', 10)
        #填写结果
        wk.input('id','tableForm_0_result','非常好')
        # #填写结果解释
        # wk.input('xpath',evaluation['result'],evaluation['txt'])
        #保存并提交
        wk.wait(4)
        loc=wk.web_el_wait('xpath','//span[text()="保存并提交"]')
        loc.click()
        # wk.click('xpath','//span[text()="保存并提交"]')
        wk.wait(3)
    with allure.step('查询新增的因子，检验新增是否成功'):
        wk.input('id', 'advanced_search_name', factor_name)
        wk.click('xpath', '//*[text()="查询"]')
        expected_result = wk.get_text(evaluation['expected_result'])
        assert expected_result == factor_name, log.error(f"添加因子失败，没有找到因子名称为{factor_name}的因子信息")
#@pytest.mark.skip
@pytest.mark.parametrize('dimensionality',load_yaml('./data/dimensionality_management.yaml'))
@allure.epic('测评管理')
@allure.severity('normal')
@allure.story('维度管理')
def test_06(Login,dimensionality):
    wk, log = Login
    allure.dynamic.title(dimensionality['title'])
    with allure.step('点击进入测评管理'):
        wk.click('xpath','//span[text()="测评管理"]')
    with allure.step('点击进入维度管理'):
        wk.click('xpath','//a[text()="维度管理"]')
    with allure.step('点击进入新增维度'):
        wk.click('xpath',dimensionality['new_dimensionality'])
    with allure.step('填写维度名称'):
        dimensionality_name='测试维度No.'+str(get_random(1,999))
        wk.input('id','dimensionNameForm_name',dimensionality_name)
    with allure.step('保存并下一步'):
        wk.scroll_foot()
        wk.click('xpath', '//span[text()="保存并下一步"]')
    with allure.step('添加因子'):
        wk.click('xpath','//span[text()="添加因子"]')
        wk.wait(1)
        #选择所有的checkbox并全部勾上
        checkboxes = wk.locators('css selector',dimensionality['check_box'])
        for checkbox in checkboxes:
                wk.wait(0.5)
                checkbox.click()
        # # 把页面上最后1个checkbox的勾给去掉
        # checkboxes.pop().click()
        #提交选择的题目
        wk.click('xpath','//p[text()="确定"]')
        wk.wait(3)
        #等待页面加载完成，点击保存并下一步
        wk.click('xpath',dimensionality['button'])
    with allure.step('维度得分模块'):
        #点击维度得分
        wk.click('id','fractionModeForm_rulesId')
        #选择计分方式
        wk.click('xpath','//div[text()="求平均值"]')
        wk.wait(1)
        wk.click('xpath',dimensionality['next'])
    with allure.step('结果解释模块'):
        #点击添加选项按钮
        wk.wait(1)
        wk.click('xpath','//span[text()="添加选项"]')
        wk.wait(2)
        #填入最小值
        wk.input('id','tableForm_0_minScore',1)
        #填入最大值
        wk.input('id', 'tableForm_0_maxScore', 10)
        #填写结果
        wk.input('id','tableForm_0_result','非常好')
        # #填写结果解释
        # wk.input('xpath',dimensionality['result'],dimensionality['txt'])
        #保存并提交
        wk.click('xpath','//span[text()="保存并提交"]')
        wk.wait(3)
    with allure.step('查询新增的维度，检验新增是否成功'):
        wk.input('id', 'advanced_search_name', dimensionality_name)
        wk.click('xpath', '//*[text()="查询"]')
        expected_result = wk.get_text(dimensionality['expected_result'])
        assert expected_result == dimensionality_name, log.error(f"添加维度失败，没有找到维度名称为{dimensionality_name}的维度信息")
@pytest.mark.skip
# @pytest.mark.flaky(reruns=1, reruns_delay=3)
@pytest.mark.parametrize('scale',load_yaml('./data/scale_management.yaml'))
@allure.epic('测评管理')
@allure.severity('normal')
@allure.story('量表管理')
def test_07(Login,scale):
    wk, log = Login
    allure.dynamic.title(scale['title'])
    with allure.step('点击进入测评管理'):
        wk.click('xpath','//span[text()="测评管理"]')
    with allure.step('点击进入量表管理'):
        wk.click('xpath','//a[text()="量表管理"]')
    with allure.step('点击进入新增量表'):
        wk.click('xpath',scale['new_scale'])
    with allure.step('选择量表分类'):
        wk.click('id','advanced_search_typeId')
        wk.click('xpath','//span[text()="教育行业"]')
    with allure.step('填写量表名称'):
        scale_name = '测试量表No.' + str(get_random(1, 999))
        wk.input('id', 'advanced_search_name', scale_name)
    with allure.step('选择量表类型'):
        wk.click('id', 'advanced_search_type')
        wk.click('xpath', '//div[text()="专业性量表"]')
    with allure.step('上传主题配图'):
        png1 = os.path.abspath('微信截图_20220622155317.png')
        png2 = os.path.abspath('微信截图_20220622155606.png')
        wk.click('xpath',scale['upload1'])
        wk.wait(2)
        # UpLoad(png1)
        # # wk.wait(1)
        # # wk.click('xpath', scale['upload2'])
        # wk.wait(2)
        # # UpLoad(png2)
    with allure.step('填写市场价'):
        wk.input('id','advanced_search_marketPrice',randint(1,999))
    with allure.step('选择量表状态'):
        wk.click('xpath','//span[text()="开启"]')
    with allure.step('保存量表基本信息'):
        wk.click('xpath', '//span[text()="保存并下一步"]')
    with allure.step('添加维度'):
        wk.click('xpath','//span[text()="添加维度"]')
        wk.wait(2)
        #选择所有的checkbox并全部勾上
        checkboxes = wk.locators('css selector',scale['check_box'])
        for checkbox in checkboxes:
                wk.wait(0.5)
                checkbox.click()
        # # 把页面上最后1个checkbox的勾给去掉
        # checkboxes.pop().click()
        #提交选择的题目
        wk.click('xpath','//p[text()="确定"]')
        wk.wait(2)
        # 等待页面加载完成，点击保存并下一步
        wk.click('xpath',scale['button'])
    with allure.step('量表计分模块'):
        #点击量表得分
        wk.click('xpath',scale['scale_scoring'])
        #选择计分方式
        wk.click('xpath','//div[text()="求平均值"]')
        wk.wait(1)
        wk.click('xpath',scale['next'])
    with allure.step('结果解释模块'):
        #点击添加选项按钮
        wk.click('xpath','//span[text()="添加选项"]')
        wk.wait(2)
        #填入最小值
        wk.input('id','tableForm_0_minScore',1)
        #填入最大值
        wk.input('id', 'tableForm_0_maxScore', 10)
        #填写结果
        wk.input('id','tableForm_0_result','非常好')
        # #填写结果解释
        # wk.input('xpath',scale['result'],scale['txt'])
        #保存并提交
        wk.click('xpath','//span[text()="保存并提交"]')
        wk.wait(3)
    with allure.step('查询新增的维度，检验新增是否成功'):
        wk.input('id', 'advanced_search_scaleNameOrId', scale_name)
        wk.click('xpath', '//span[text()="查询"]')
        expected_result = wk.get_text(scale['expected_result'])
        assert expected_result == scale_name, log.error(f"添加量表失败，没有找到量表名称为{scale_name}的量表信息")
#@pytest.mark.skip
@pytest.mark.parametrize('role',load_yaml('./data/role_management.yaml'))
@allure.epic('权限管理')
@allure.severity('normal')
@allure.story('角色管理')
def test_08(Login,role):
    wk, log = Login
    allure.dynamic.title(role['title'])
    with allure.step('点击进入权限管理'):
        wk.click('xpath','//span[text()="权限管理"]')
    with allure.step('点击进入角色管理'):
        wk.click('xpath','//a[text()="角色管理"]')
    with allure.step('点击进入新增角色'):
        wk.click('xpath',role['add_role'])
    with allure.step('输入角色名称'):
        role_name='测试角色No'+str(get_random(1,999))
        wk.input('id','advanced_search_roleName',role_name)
    with allure.step('输入角色编码'):
        role_coding=get_random(1,9999)
        wk.input('id','advanced_search_roleCode',role_coding)
    with allure.step('选择角色状态'):
        wk.click('id','advanced_search_status')
        wk.click('xpath','//div[text()="正常"]')
    with allure.step('选择数据范围'):
        wk.click('xpath','//span[text()="机构数据"]')
    with allure.step('保存角色信息'):
        wk.click('xpath', '//span[text()="保 存"]')
        wk.wait(2)
    with allure.step('查询新增的角色，检验新增是否成功'):
        wk.input('id', 'advanced_search_roleName', role_name)
        wk.click('xpath', '//*[text()="查询"]')
        wk.wait(3)
        expected_result = wk.get_text(role['expected_result'])
        print(expected_result)
        assert expected_result == role_name, log.error(f"添加角色失败，没有找到角色名称为{role_name}的角色信息")


#@pytest.mark.skip
@pytest.mark.parametrize('role_admin',load_yaml('./data/role_admin.yaml'))
@allure.epic('权限管理')
@allure.severity('normal')
@allure.story('机构管理员')
def test_09(Login,role_admin):
    wk, log = Login
    allure.dynamic.title(role_admin['title'])
    with allure.step('点击进入权限管理'):
        wk.click('xpath','//span[text()="权限管理"]')
    with allure.step('点击进入机构管理员'):
        wk.click('xpath','//a[text()="机构管理员"]')
    with allure.step('点击进入新增管理员'):
        wk.click('xpath',role_admin['add_role'])
    with allure.step('点击组织机构'):
        wk.click('xpath', role_admin['Organization'])
        wk.click('xpath', '//span[text()="兰州教育局测试"]')
        wk.click('xpath', '//*[@id="root"]/div/section/section/main/div/ul')
    with allure.step('选择账号类型'):
        wk.click('id','advanced_search_accountType')
        wk.click('xpath','//div[text()="工号"]')
    with allure.step('输入登录账号'):
        role_account='cs'+str(get_random(1,9999))
        wk.input('id','advanced_search_account',role_account)
    with allure.step('输入姓名'):
        role_name = '测试机构管理员No' + str(get_random(1, 999))
        wk.input('id', 'advanced_search_userManageName', role_name)
    with allure.step('选择性别'):
        wk.click('xpath',role_admin['sex'])
    with allure.step('选择生日'):
        wk.click('id', 'advanced_search_birth')
        wk.wait(2)
        wk.click('xpath', role_admin['age'])
        wk.wait(3)
    with allure.step('保存角色信息'):
        wk.click('xpath', '//span[text()="保 存"]')
        wk.wait(2)
    with allure.step('查询新增的角色，检验新增是否成功'):
        wk.input('id', 'advanced_search_accountOrId', role_account)
        wk.click('xpath', '//*[text()="查询"]')
        wk.wait(3)
        expected_result = wk.get_text(role_admin['expected_result'])
        print(expected_result)
        assert expected_result == role_account, log.error(f"添加角色失败，没有找到账号为{role_account}的机构管理员")
@pytest.mark.skip
@pytest.mark.parametrize('classify',load_yaml('./data/classify_mangement.yaml'))
@allure.epic('分类管理')
@allure.severity('normal')
@allure.story('分类列表')
def test_10(Login,classify):
    wk, log = Login
    allure.dynamic.title(classify['title'])
    with allure.step('点击进入分类管理'):
        wk.click('xpath','//span[text()="分类管理"]')
    with allure.step('点击进入分类列表'):
        wk.click('xpath','//a[text()="分类列表"]')
    with allure.step('点击进入新增分类'):
        wk.click('xpath',classify['new_classify'])
    with allure.step('填写分类名称'):
        classify_name='测试分类No'+str(get_random(1,999))
        wk.input('id','advanced_search_dictName',classify_name)
    with allure.step('选择上级分类'):
        wk.click('id','advanced_search_parentCode')
        wk.click('xpath','//span[text()="我的"]')
    # with allure.step('上传分类图标'):
    #     png1 = os.path.abspath('微信截图_20220622155317.png')
    #     wk.click('xpath', classify['upload1'])
    #     wk.wait(2)
    #     UpLoad(png1)
    with allure.step('保存完善资料'):
        wk.click('xpath','//span[text()="保存完善资料"]')

if __name__ == '__main__':
    # pytest.main(['-s','oms.py','-v'])
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    pytest.main(['-v','--reruns','1','--reruns-delay','2','oms.py', '--alluredir', './result/{}'.format(time_str), '--clean-alluredir'])
    os.system('allure serve ./result/{}'.format(time_str))
