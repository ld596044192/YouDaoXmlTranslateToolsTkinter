#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 模块说明
import tkinter as tk
import os,sys


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


class ModuleIllustration(object):
    def root_form(self,module_button,module_button_disable):    # 模块说明窗口
        self.module_root = tk.Toplevel()
        self.module_root.title('模块说明（必看）')
        screenWidth = self.module_root.winfo_screenwidth()
        screenHeight = self.module_root.winfo_screenheight()
        w = 800
        h = 700
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.module_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.module_root.resizable(0, 0)
        self.module_root.iconbitmap(tools_ico)
        self.module_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.module_root.attributes("-topmost", True)  # 窗口置顶

        self.module_button = module_button
        self.module_button_disable = module_button_disable

        self.module_button.place_forget()
        self.module_button_disable.place(x=400, y=50)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context, 'module_button', self.module_button)
        setattr(Context, 'module_button_disable', self.module_button_disable)

        self.module_root.protocol('WM_DELETE_WINDOW', self.module_close_handle)  # 点击关闭按钮时执行的函数

        self.main_form()

    def module_close_handle(self):
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context, 'module_button').place(x=400, y=50)
        getattr(Context, 'module_button_disable').place_forget()
        self.module_root.destroy()

    def main_form(self):
        # 显示模块说明Text框
        self.module_text = tk.Text(self.module_root, width=80, height=30, font=('微软雅黑', 12))
        self.module_text.place(x=20, y=20)
        # 配置滚动条
        self.module_scroll = tk.Scrollbar(self.module_root)
        self.module_scroll.place(x=745, y=20, height=635)
        self.module_scroll.config(command=self.module_text.yview)
        self.module_text.config(yscrollcommand=self.module_scroll.set)
        # 读取模块说明文件
        with open(module_file_path, 'r', encoding='utf-8') as f:
            self.module_text.insert('end', f.read())
        # 禁止编辑
        self.module_text.config(state='disabled')

