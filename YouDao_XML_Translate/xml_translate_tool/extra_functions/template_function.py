#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 创建模板逻辑
import os,sys
from tkinter import messagebox
import tkinter as tk
import threading


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径


def create_template():
    # 获取Windows桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    # 创建模板文件夹
    template_path = os.path.join(desktop_path, 'xml_translate_template')
    if not os.path.exists(template_path):
        os.makedirs(template_path)
    # 创建values文件夹
    values_path = os.path.join(template_path, 'values')
    if not os.path.exists(values_path):
        os.makedirs(values_path)
    # 创建values-en文件夹
    values_en_path = os.path.join(template_path, 'values-en')
    if not os.path.exists(values_en_path):
        os.makedirs(values_en_path)
    # 创建values文件夹中的strings.xml文件
    values_string_path = os.path.join(values_path, 'strings.xml')
    if not os.path.exists(values_string_path):
        with open(values_string_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\r\n'
                    '<resources>\r'
                    '     <string name="app_name">这是一个xml模板</string>\r'
                    '     <string name="usage">请把需要翻译的中文xml文件替换成strings.xml</string>\r'
                    '     <string name="cover">这样覆盖此文件后成为翻译基准！！！</string>\r'
                    '     <string name="translateEn">values-en文件是翻译文件夹，如需添加直接复制该文件，只需要把后面的en换成其他翻译语言代码即可</string>\r'
                    '</resources>')
    # 创建values-en文件夹中的strings.xml文件
    values_en_string_path = os.path.join(values_en_path, 'strings.xml')
    if not os.path.exists(values_en_string_path):
        with open(values_en_string_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\r\n'
                    '<resources>\r\n'
                    '</resources>')


def template_prompt(template_button,template_button_disable):
    # 点击按钮二次确认提示
    content = """
    是否创建xml翻译模板？
    1.创建后的模板会显示在桌面上的xml_translate_template文件夹中
    2.把你需要翻译的中文xml文件替换成values文件夹中的strings.xml文件即可
    3.若想添加多个语言翻译，把values-en文件夹复制一份，把文件夹名字中的en换成其他语言代码即可，依次类推
    """
    if messagebox.askyesno('创建模板提示', content):
        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'Desktop', 'xml_translate_template')):
            create_template()
            msg = '模板创建成功！！！\n点击“打开文件夹”按钮即可自动打开模板位置；点击“关闭”则关闭该页面'
        else:
            msg = '模板文件夹已存在！！！\n点击“打开文件夹”按钮即可自动打开模板位置；点击“关闭”则关闭该页面'
        # 打开创建模板成功的窗口
        Template().root_form(template_button,template_button_disable,msg)


class Template(object):
    def root_form(self,template_button,template_button_disable,msg):
        template_button.place_forget()
        template_button_disable.place(x=400, y=90)

        # 创建模板成功的窗口
        self.template_root = tk.Toplevel()
        self.template_root.title('创建模板提示')
        screenWidth = self.template_root.winfo_screenwidth()
        screenHeight = self.template_root.winfo_screenheight()
        w = 500
        h = 200
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.template_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.template_root.resizable(0, 0)
        self.template_root.iconbitmap(tools_ico)
        self.template_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.template_root.attributes("-topmost", True)  # 窗口置顶

        self.template_button = template_button
        self.template_button_disable = template_button_disable

        self.template_root.protocol("WM_DELETE_WINDOW", self.close_handle)

        self.main_form(msg)

    def close_handle(self):
        self.template_root.destroy()
        self.template_button_disable.place_forget()
        self.template_button.place(x=400, y=90)

    def main_form(self,msg):
        # 提示模板创建成功
        tk.Label(self.template_root, text=msg, font=('微软雅黑',10),fg='red').place(x=20, y=50)
        # 打开文件夹按钮
        template_button = tk.Button(self.template_root, text='打开文件夹',width=10)
        template_button.place(x=100, y=100)
        template_button.bind('<Button-1>',lambda x: threading.Thread(target=self.open_file).start())

        # 关闭按钮
        template_button_close = tk.Button(self.template_root, text='关闭',width=10, command=self.close_handle)
        template_button_close.place(x=250, y=100)

    def open_file(self):
        try:
            # 打开模板文件夹
            os.startfile(os.path.join(os.path.expanduser("~"), 'Desktop', 'xml_translate_template'))
        except Exception:
            self.template_root.destroy()
            messagebox.showerror('打开文件夹失败', 'xml_translate_template文件夹不存在，请重新创建模板!!!')
            self.template_button_disable.place_forget()
            self.template_button.place(x=400, y=90)

