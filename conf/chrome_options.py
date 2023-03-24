'''
    Chrome浏览器的配置项
'''

from selenium import webdriver


def options():
    # 创建chrome浏览器配置项
    options = webdriver.ChromeOptions()
    # 添加试验性质的配置项
    # options.add_experimental_option()
    # # 添加常规设定
    # options.add_argument()
    # 页面加载策略
    options.page_load_strategy = 'eager'
    # 浏览器最大化
    # options.add_argument('start-maximized')
    # 指定位置启动浏览器
    options.add_argument('window-position=2500,200')
    # 设置窗体的启动大小
    options.add_argument('window-size=1200,800')

    # 去掉浏览器提示自动化黄条:没什么用处，只是为了好看而已。(附加去掉控制台多余日志信息)
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    # 只支持与2.7版本的selenium，目前已经被弃用了。
    # options.add_experimental_option('disable-infobars')

    # 无头模式：不在桌面实现浏览器的运行，作为后台静默运行，虽然看不到，但是一切照旧。偶尔场景会有异常，但很少
    # options.add_argument('--headless')

    # 读取本地缓存的操作：webdriver启动的时候默认是不会加载本地缓存数据的。有时候想要绕过验证码或者登录流程，可以通过加载本地缓存来实现
    # 调用本地缓存一定要先关闭所有的浏览器，不然会报错。
    # options.add_argument(r'--user-data-dir=C:\Users\xuzhu\AppData\Local\Google\Chrome\User Data')

    # 去掉账号密码弹出框
    prefs = dict()
    prefs['credentials_enable_service'] = False
    prefs['profile.password_manager_enable'] = False
    # 缺少了一行代码，用于调用这个字典
    options.add_experimental_option('prefs', prefs)

    # 隐身模式下无法调用selenium中的switch_to.new_window()函数
    # options.add_argument('incognito')

    # 去掉控制台多余信息手段二，可以作为保险的存在。（当你发现还有多余信息的时候）
    options.add_argument('--log_level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    # 去掉控制台多余信息
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # return这一步很重要。因为需要有options对象进行返回才可以对webdriver生效
    return options
