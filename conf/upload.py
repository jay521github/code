#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Name: upload.py
@Auth: Sun dong
@Date: 2022/7/26-15:59
@Desc: 
@Ver : 0.0.0
"""
import win32con
import win32gui


def UpLoad(path):
    dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, path)  # 往输入框输入绝对地址
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
