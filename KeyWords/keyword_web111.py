
from time import sleep

from selenium import webdriver


# 定义工具类
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class WebKeys:

    def __init__(self, driver):

        self.driver = driver

    # 访问URL
    def open(self, url):
        self.driver.get(url)

    # 退出
    def quit(self):
        self.driver.quit()

    # 元素定位
    def locator(self, name,value):
        return self.driver.find_element(name, value)
    #多元素定位
    def locators(self,name,value):
        return self.driver.find_elements(name,value)

    # 元素定位，传参List
    def locator_list(self, list):
        el = self.driver.find_element(list[0], list[1])
        # 将定位的地方框出来
        self.locator_station(el)
        # return self.driver.find_element(list[0], list[1])
        return el

    # 组元素定位，传参List
    def locator_list_group(self, list):
        return self.driver.find_elements(list[0], list[1])

    # 输入
    def input(self, name,value,txt):
        el = self.locator(name,value)
        el.clear()
        el.send_keys(txt)

    # 强制等待
    def wait(self, time_):
        sleep(time_)

    # 获取title，获取网页标题栏
    def get_title(self):
        return self.driver.title

    # 获取页面text，获取页面文本，使用xpath定位
    def get_text(self, path):
        return self.locator("xpath",path).text

    # 显示定位的地方，确定定位问题
    def locator_station(self,element):
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid green;"  # 边框border:2px; red红色
        )

    # 窗口切换
    def change_window(self,n):
        # 获取句柄
        handles = self.driver.window_handles
        # 切换到原始页面,n = 0
        # 切换句柄到第二个页面,n = 1 ,以此类推
        self.driver.switch_to.window(handles[n])
        print(self.driver.title)

    # 关闭当前窗口
    def close_window(self):
        self.driver.close()

    # 鼠标点击并悬停
    def mouse_hold(self,url):
        btn = self.driver.find_elements_by_xpath(url)[0]
        action = ActionChains(self.driver)
        action.click_and_hold(btn).perform()

    # 切换frame
    def change_frame(self,a):
        self.driver.switch_to.frame(a)

    # 切换回主框架
    def change_defaultFrame(self):
        self.driver.switch_to.default_content()

    # 点击
    def click(self, name, value):
        self.locator(name, value).click()
    #显示等待
    def web_el_wait(self, name, value):
        return WebDriverWait(self.driver, 10, 0.5).until(
            lambda el: self.locator(name, value), message='元素查找失败')

    # 弹窗
    def alert(self):
        return self.driver.switch_to.alert.accept()

    # 滚动条底部
    def scroll_foot(self):
        # js = "var q=document.documentElement.scrollTop=10000"
        js = "window.scrollTo(0,document.body.scrollHeight)"
        return self.driver.execute_script(js)

    #滚动到顶部
    def scroll_top(self):
        js = "window.scrollTo(0,0)"
        return self.driver.execute_script(js)