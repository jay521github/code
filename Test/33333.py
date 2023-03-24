#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: 33333.py
@Auth: Sun dong
@Date: 2023/2/2-16:13
@Desc: 
@Ver : 0.0.0
"""
from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
driver = webdriver.Chrome()
driver.get('https://www.qq.com/')
driver.maximize_window()
driver.find_element_by_partial_link_text('登录').click()
# 切换框架
# driver.switch_to.frame('ptlogin_iframe')

driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/p[1]/span').click()
driver.find_element_by_xpath('//span[text()="QQ登录"]').click()
sleep(1)
frame=driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/iframe')
driver.switch_to.frame(frame)
driver.switch_to.frame('ptlogin_iframe')
sleep(2)
driver.find_element_by_id('switcher_plogin').click()
sleep(1)
driver.find_element_by_id('u').send_keys('374074353@qq.com')
driver.find_element_by_id('p').send_keys('jwshan024751')
sleep(1)
driver.find_element_by_id('login_button').click()
sleep(3)
# 切换框架
driver.switch_to.frame('tcaptcha_iframe_dy')
# 定位滑块位置
locate = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[6]')
ActionChains(driver).click_and_hold(locate).perform()
sleep(2)
# 拖拽鼠标
for i in range(1,88):
    try:
        ActionChains(driver).move_by_offset(2,0).perform()
        print(i)
    except Exception as f:
        break
    ActionChains(driver).reset_actions()
    sleep(0.1)
# 释放鼠标
ActionChains(driver).release(locate).perform()
