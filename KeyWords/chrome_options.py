'''
    Chrome浏览器的配置:
        通过webdriver启动的浏览器默认是零缓存（不读取本地缓存数据）的浏览器。相当于隐身浏览器，包括各类设置都是已经有的。
        options没有任何技术含量，所有的内容都是已经写死的内容
        一般就是一次编写，以后固定使用。
'''
from time import sleep

from selenium import webdriver


class ChromeOptions:
    def options(self):
        # chrome浏览器的配置项，可以通过修改默认参数，改变默认启动的浏览器的形态
        options = webdriver.ChromeOptions()
        # 无头模式：虽然看不到，但是一切照旧，在一些特定场景下会失败
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        return options

