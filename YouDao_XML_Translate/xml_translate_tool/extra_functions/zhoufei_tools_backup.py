#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
# 周飞工具集合

import tkinter as tk
import os, sys
# from YouDao_XML_Translate.xml_translate_tool.extra_functions.browser_cef import cef_main  # cef浏览器
# from YouDao_XML_Translate.xml_translate_tool.extra_functions.browser_pyqt5 import browser_main,show_browser_tray  # pyqt5浏览器
import webbrowser  # webbrowser浏览器(由于内嵌浏览器遇到第二次启动会阻塞的问题，可能与代码设计架构有关，也可能与其他有影响)

open_browser_flag = False  # 是否打开浏览器标志位


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS, r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)  # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径

# def open_pyqt5_browser():
#     """打开pyqt5浏览器"""
#     global open_browser_flag
#     if not open_browser_flag:
#         open_browser_flag = True
#         browser_main()
#     else:
#         print('浏览器已打开')
#         show_browser_tray()




