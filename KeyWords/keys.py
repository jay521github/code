
import time

# import SafeDriver.drivers
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
# 构造浏览器对象，基于type_参数，构造对应的浏览器对象。
from conf import chrome_options


def open_browser(type_):

    try:
        if type_ == 'Chrome':
            driver = webdriver.Chrome()
        else:
            driver = getattr(webdriver, type_)()
    except:
        driver = webdriver.Chrome()
    return driver



class Keys:
    # 临时driver对象
    # driver = webdriver.Chrome()

    # 构造函数
    def __init__(self, type_):
        self.driver = open_browser(type_)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => false
                })
              """
        })

    # url的访问
    def open(self, url):
        self.driver.get(url)

    # 元素定位:一定要考虑各种不同的元素定位方法。
    def locate(self, by, value):
        return self.driver.find_element(by, value)

    # 显示定位的地方，确定定位问题
    def locator_station(self, element):
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid green;"  # 边框border:2px; red红色
        )

    # 输入
    def input(self, by, value, txt):
        self.locate(by, value).send_keys(txt)

    # 点击
    def click(self, by, value):
        self.locate(by, value).click()

    # 浏览器关闭
    def quit(self):
        self.driver.quit()

    # 显式等待
    def driver_wait(self, by, value):
        return WebDriverWait(self.driver, 10, 0.5).until(lambda el: self.locate(by, value), message='元素获取失败')

    # 强制等待
    def sleep(self, time_):
        time.sleep(int(time_))

    # 句柄的切换：为了满足有些场景下不需要close，需要考虑逻辑的处理
    def switch_handle(self, status=1):
        handles = self.driver.window_handles
        if status == 1:
            self.driver.close()
        self.driver.switch_to.window(handles[1])

    # 断言预期结果是否包含在实际结果内
    def assert_almost_equal(self, by, value, expected):
        try:
            reality = self.locate(by, value).text
            assert expected in reality, '{0}不在{1}的范围内'.format(expected, reality)
            return True
        except:
            return False

    # 文本断言
    def assert_text(self, by, value, expected):
        try:
            reality = self.locate(by, value).text
            assert expected == reality, '{0}与{1}不相等'.format(expected, reality)
        except Exception as e:
            print('断言失败：{}'.format(e))

    # 切换Iframe
    def switch_frame(self, value, by=None):
        if by is None:
            self.driver.switch_to.frame(value)
        else:
            self.driver.switch_to.frame(self.locate(by, value))
    #模拟鼠标点击
    def Mouse_Click(self,by,value):
        signin = self.locate(by, value)  # 用css定位到before的父亲节点处
        ActionChains(self.driver).click(signin).perform()

    # 模拟鼠标点击
    def move_to(self,by,value):
        btn = self.locate(by,value)
        action = ActionChains(self.driver)
        action.move_to_element(btn).perform()
    #移除时间空间的只读模式
    def Time_Control(self):
        js ="document.getElementById('advanced_search_birthStamp').removeAttribute('autocomplete')"
        return self.driver.execute_script(js)

    # 滚动到顶部
    def scroll_top(self):
        js = "window.scrollTo(0,0)"
        return self.driver.execute_script(js)
    # 滚动条底部
    def scroll_foot(self):
        # js = "var q=document.documentElement.scrollTop=10000"
        js = "window.scrollTo(0,document.body.scrollHeight)"
        return self.driver.execute_script(js)

