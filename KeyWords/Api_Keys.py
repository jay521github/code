# -*- coding: UTF-8 -*-
import json
import jsonpath
import requests
import allure
from conf.logger import logger
class api_keys():
    @allure.step("发送get请求")
    def get(self,url,params=None,**kwargs):
        logger.info(f'发送请求的地址为：{url},发送的数据为：{params}')
        return requests.get(url=url,params=params,**kwargs)


    @allure.step("发送post请求")
    def post(self,url,data=None,**kwargs):
        logger.info(f'发送请求的地址为：{url},发送的数据为：{data}')
        return requests.post(url=url,data=data,**kwargs)

    @allure.step("获取返回结果字典值")
    def json_path(self,txt,key):
        try:
            txt=json.loads(txt)
            value = jsonpath.jsonpath(txt, '$..{0}'.format(key))
            if value:
                if len(value) ==1:
                    logger.info(f'成功提取的数据为：{value[0]}')
                    return value[0]
                return value

        except Exception as e:
            logger.error(f'没有提取到数据，报错信息：{e}')
            return e
        return value