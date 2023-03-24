# -*- coding: UTF-8 -*-
"""
@author:Sun Dong
@file:main_run.py
@time:2022/03/11
"""
import os

import pytest


def run():
    # 指定执行文件
    pytest.main(['-v','./case/6noble.py',
                 '--alluredir', './result','--clean-alluredir'])
    # os.system('allure generate ./result/ -o ./report_allure/ --clean')
    os.system('allure serve result')

if __name__ == '__main__':
    run()
