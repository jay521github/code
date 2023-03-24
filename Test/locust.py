#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: locust.py
@Auth: Sun dong
@Date: 2022/7/13-17:08
@Desc: 
@Ver : 0.0.0
"""
# 该demo适用于：locust v2.1.0
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner

debug = False

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")

# 压测开始的时候执行
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("test is starting")

# 压测结束的时候执行
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("test is ending")

class HttpDemo(HttpUser):
    wait_time = between(0, 10)
    host = 'http://test.yourdns.com/api/query/12345'  # 示例地址是脱敏过的

    def on_start(self):
        # 每次任务开始的时候执行
        print("task start")

    def on_stop(self):
        # 每次任务执行完时执行
        print("task stop")

    '''例子'''

    @task
    def test(self):

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
        req = self.client.get(self.host, headers=header, verify=False)  # self.client调用get和post方法，和requests一样

        if req.status_code == 200: #这里的校验逻辑可以按需求写
            print("success")
        else:
            print("fails")

if __name__ == "__main__":
    # 调试模式，1s执行一次
    if debug:
        from locust.env import Environment
        my_env = Environment(user_classes=[HttpDemo])
        HttpDemo(my_env).run()
    else:
        import os
        #os.system("locust -f http_demo.py --host=http://lotcheck.woa.com")  # web console
        os.system("locust -f http_demo.py --host=http://test.yourdns.com HttpDemo --headless -u 1 -r 2 --run-time 10s")  # commandline启动