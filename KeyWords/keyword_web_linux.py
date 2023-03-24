#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: keyword_web_linux.py
@Auth: Sun dong
@Date: 2022/8/15-14:50
@Desc: 
@Ver : 0.0.0
"""
from time import sleep

from selenium import webdriver

# 生成一个浏览器（webdriver对象）:反射机制
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from KeyWords.chrome_options import ChromeOptions


# def browser(type_):
#     try:
#         driver = getattr(webdriver, type_)()
#     except Exception as e:
#         print(e)
#         driver = webdriver.Chrome(options=ChromeOptions().options())
#     return driver
def browser(type_):
    if type_ == 'Chrome':
        driver = webdriver.Chrome(options=ChromeOptions().options())
    else:
        try:
            driver = getattr(webdriver, type_)()
        except Exception as e:
            print("Exception Information:" + str(e))
            driver = webdriver.Chrome()
    return driver


# 定义工具类
class WebKeys:
    # 定义driver
    # driver = webdriver.Chrome()

    # 构造函数
    def __init__(self, type_):
        self.driver = browser(type_)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => false
                        })
                      """
        })


    # 访问URL
    def open(self, url):
        self.driver.get(url)

    # 退出
    def quit(self):
        self.driver.quit()

    # 元素定位
    def locator(self, name, value):
        return self.driver.find_element(name, value)
        # 多元素定位

    def locators(self, name, value):
        return self.driver.find_elements(name, value)

    # 显示定位的地方，确定定位问题
    def locator_station(self, element):
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid green;"  # 边框border:2px; red红色
        )

    # 输入
    def input(self, name, value, txt):
        self.locator(name, value).send_keys(txt)

    # 点击
    def click(self, name, value):
        self.locator(name, value).click()

    # 文本断言校验
    def assert_text(self, name, value, fact_text):
        assert self.locator(name, value).text == fact_text, '断言失败'

    # 强制等待
    def wait(self, time_):
        sleep(time_)
    # 显示等待
    def web_el_wait(self, name, value):
        return WebDriverWait(self.driver, 10, 0.5).until(
            lambda el: self.locator(name, value), message='元素查找失败')

    # 获取页面text，获取页面文本，使用xpath定位
    def get_text(self, path):
        return self.locator("xpath", path).text
    #弹窗
    def alert(self):
        return self.driver.switch_to.alert.accept()

    # 滚动条底部
    def scroll_foot(self):
        # js = "var q=document.documentElement.scrollTop=10000"
        js = "window.scrollTo(0,document.body.scrollHeight)"
        return self.driver.execute_script(js)

    # 滚动到顶部
    def scroll_top(self):
        js = "window.scrollTo(0,0)"
        return self.driver.execute_script(js)
    #滑动到指定元素位置
    def scrollbar(self,value):
        ele=self.locator('xpath',value)
        self.driver.execute_script("arguments[0].focus();",ele)
    # 滚动条往下滑动
    def down_scroll(self):
        # js = "var q=document.documentElement.scrollTop=10000"
        # js="window.scrollTo(0,1000)"
        js="window.scrollBy(0,300)"
        return self.driver.execute_script(js)
    def Time_Control(self):
        js = "$('input[id=advanced_search_birthStamp]').removeAttr('readonly')"
        return self.driver.execute_script(js)

    # 鼠标点击并悬停
    def mouse_hold(self,path):
        btn = self.locator("xpath", path)
        action = ActionChains(self.driver)
        action.click_and_hold(btn).perform()

    # 模拟鼠标点击
    def Mouse_Click(self, name, value):
        signin = self.locator(name, value)
        ActionChains(self.driver).click(signin).perform()

    # 句柄的切换：为了满足有些场景下不需要close，需要考虑逻辑的处理
    def switch_handle(self, status=1):
        handles = self.driver.window_handles
        if status == 1:
            self.driver.close()
        self.driver.switch_to.window(handles[1])

    # 断言预期结果是否包含在实际结果内
    def assert_almost_equal(self, name, value, expected):
        try:
            reality = self.locator(name, value).text
            assert expected in reality, '{0}不在{1}的范围内'.format(expected, reality)
            return True
        except:
            return False

    # # 文本断言
    # def assert_text(self, by, value, expected):
    #     try:
    #         reality = self.locator(by, value).text
    #         assert expected == reality, '{0}与{1}不相等'.format(expected, reality)
    #     except Exception as e:
    #         print('断言失败：{}'.format(e))

    # 切换Iframe
    def switch_frame(self, value, by=None):
        if by is None:
            self.driver.switch_to.frame(value)
        else:
            self.driver.switch_to.frame(self.locator(by, value))