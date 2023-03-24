#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: read.py
@Auth: Sun dong
@Date: 2022/7/4-15:47
@Desc: 
@Ver : 0.0.0
"""
import pathlib
import openpyxl

from KeyWords.keys import Keys
from excel import excel_conf



# 解析测试用例中测试参数单元格的内容，并转换为字典的形态返回
def arguments(value):
    data = dict()
    # 如果value有值，进行切分
    if value:
        str_temp = value.split(';')
        for temp in str_temp:
            t = temp.split('=', 1)
            data[t[0]] = t[1]
    # 如果value没有值，就不做任何操作。
    else:
        pass
    return data

# 获取指定的测试用例文件，进行自动化执行
def read(file, log):
    excel = openpyxl.load_workbook(file)
    # 获取所有的sheet页，来执行里面的测试内容
    for name in excel.sheetnames:
        sheet = excel[name]
        log.info('**********正在执行{}Sheet页*********'.format(name))
        for values in sheet.values:
            # 获取测试用例的正文内容
            if type(values[0]) is int:
                # 用例描述可以用于日志的输出
                log.info('*****************正在执行：{}*****************'.format(values[3]))
                data = arguments(values[2])
                # 实例化操作
                if values[1] == 'open_browser':
                    key = Keys(**data)
                    Key=None
                # 断言行为:基于断言的返回结果来判定测试的成功失败，并进行写入操作
                elif 'assert' in values[1]:
                    status = getattr(key, values[1])(expected=values[4], **data)
                    # 基于status判定写入的测试结果
                    if status:
                        excel_conf.pass_(sheet.cell, row=values[0] + 2, column=6)
                    else:
                        excel_conf.failed(sheet.cell, row=values[0] + 2, column=6)
                    # 保存Excel
                    excel.save(file)
                # 常规操作行为
                else:
                    getattr(key, values[1])(**data)
    excel.close()
    log.info('********执行完毕*********')