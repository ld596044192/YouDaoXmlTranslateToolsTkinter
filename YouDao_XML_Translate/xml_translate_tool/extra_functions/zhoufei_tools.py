#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
# 周飞工具集合

import tkinter as tk
import os,sys
# from YouDao_XML_Translate.xml_translate_tool.extra_functions.browser_cef import cef_main  # cef浏览器
# from YouDao_XML_Translate.xml_translate_tool.extra_functions.browser_pyqt5 import browser_main,show_browser_tray  # pyqt5浏览器
import webbrowser  # webbrowser浏览器(由于内嵌浏览器遇到第二次启动会阻塞的问题，可能与代码设计架构有关，也可能与其他有影响)


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径
module_file_path = resource_path(os.path.join('version', 'module_illustrate_file.txt'))  # 模块说明文件路径


class Context:
    pass


class ZFTools(object):
    def root_form(self,zhoufei_button,zhoufei_button_disable):    # 模块说明窗口
        self.zf_root = tk.Toplevel()
        self.zf_root.title('周飞工具集合')
        screenWidth = self.zf_root.winfo_screenwidth()
        screenHeight = self.zf_root.winfo_screenheight()
        w = 600
        h = 500
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.zf_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.zf_root.resizable(0, 0)
        self.zf_root.iconbitmap(tools_ico)
        self.zf_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        # self.zf_root.attributes("-topmost", True)  # 窗口置顶

        self.zhoufei_button = zhoufei_button
        self.zhoufei_button_disable = zhoufei_button_disable

        self.zhoufei_button.place_forget()
        self.zhoufei_button_disable.place(x=400, y=250)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context, 'zhoufei_button', self.zhoufei_button)
        setattr(Context, 'zhoufei_button_disable', self.zhoufei_button_disable)

        self.zf_root.protocol('WM_DELETE_WINDOW', self.module_close_handle)  # 点击关闭按钮时执行的函数

        self.main_form()

    def module_close_handle(self):
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context, 'zhoufei_button').place(x=400, y=250)
        getattr(Context, 'zhoufei_button_disable').place_forget()
        self.zf_root.destroy()

    def main_form(self):
        # 蒙恬扫描push测试
        self.mt_scan_push_button = tk.Button(self.zf_root, text='蒙恬扫描push测试',width=20)
        self.mt_scan_push_button_disable = tk.Button(self.zf_root, text='蒙恬扫描push测试',width=20)
        self.mt_scan_push_button.place(x=50, y=50)
        self.mt_scan_push_button_disable.config(state='disabled')
        self.mt_scan_push_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_push_test).start())

        # 合并多语言的多语言XML文件工具
        self.merge_xml_button = tk.Button(self.zf_root, text='合并多语言XML文件工具',width=20)
        self.merge_xml_button_disable = tk.Button(self.zf_root, text='合并多语言XML文件工具',width=20)
        self.merge_xml_button.place(x=50, y=100)
        self.merge_xml_button_disable.config(state='disabled')
        self.merge_xml_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_merge_xml).start())

        # XML文件转execl文件和execl文件转XML文件
        self.xml_excel_button = tk.Button(self.zf_root, text='XML文件转execl文件和execl文件转XML文件')
        self.xml_excel_button_disable = tk.Button(self.zf_root, text='XML文件转execl文件和execl文件转XML文件')
        self.xml_excel_button.place(x=50, y=150)
        self.xml_excel_button_disable.config(state='disabled')
        self.xml_excel_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_xml_excel).start())

        # XML文件翻译工具
        self.xml_translate_button = tk.Button(self.zf_root, text='XML文件翻译工具',width=20)
        self.xml_translate_button_disable = tk.Button(self.zf_root, text='XML文件翻译工具',width=20)
        self.xml_translate_button.place(x=50, y=200)
        self.xml_translate_button_disable.config(state='disabled')
        self.xml_translate_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_xml_translate).start())

    def click_open_button(self):
        self.mt_scan_push_button.place_forget()
        self.mt_scan_push_button_disable.place(x=50, y=50)
        self.merge_xml_button.place_forget()
        self.merge_xml_button_disable.place(x=50, y=100)
        self.xml_excel_button.place_forget()
        self.xml_excel_button_disable.place(x=50, y=150)
        self.xml_translate_button.place_forget()
        self.xml_translate_button_disable.place(x=50, y=200)

    def close_button_state(self):
        self.mt_scan_push_button_disable.place_forget()
        self.mt_scan_push_button.place(x=50, y=50)
        self.merge_xml_button_disable.place_forget()
        self.merge_xml_button.place(x=50, y=100)
        self.xml_excel_button_disable.place_forget()
        self.xml_excel_button.place(x=50, y=150)
        self.xml_translate_button_disable.place_forget()
        self.xml_translate_button.place(x=50, y=200)

    def open_push_test(self):
        # 打开蒙恬扫描push测试窗口
        self.click_open_button()

        url = 'https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/蒙恬扫描push测试.html'
        print('正在打开网页（浏览器）：', url)
        webbrowser.open(url)

        self.close_button_state()

    def open_merge_xml(self):
        # 打开合并多语言的多语言XML文件工具窗口
        self.click_open_button()

        url = 'https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/languageXMLmerge.html'
        print('正在打开网页（浏览器）：', url)
        webbrowser.open(url)

        self.close_button_state()

    def open_xml_excel(self):
        # 打开XML文件转execl文件和execl文件转XML文件窗口
        self.click_open_button()

        url = 'https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/XmlchangeExecl.html'
        print('正在打开网页（浏览器）：', url)
        webbrowser.open(url)

        self.close_button_state()

    def open_xml_translate(self):
        # 打开XML文件翻译工具窗口
        self.click_open_button()

        url = 'https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/XMLtranslateXML.html'
        print('正在打开网页（浏览器）：', url)
        webbrowser.open(url)

        self.close_button_state()

