#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import threading
import tkinter as tk
import tkinter.messagebox
import win32api
import win32con


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径
module_file_path = resource_path(os.path.join('version', 'module_illustrate_file.txt'))  # 模块说明文件路径


# 获取Windows文档路径
doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'  # 工具临时文件路径
youdao_id_key_path = trans_file + '\\youdao_id_key.log'  # 记录有道翻译ID和KEY


class Context:
    pass


class Setting(object):
    def root_form(self,setting_button,setting_button_disable):    # 设置窗口
        self.setting_root = tk.Toplevel()
        self.setting_root.title('设置')
        screenWidth = self.setting_root.winfo_screenwidth()
        screenHeight = self.setting_root.winfo_screenheight()
        w = 600
        h = 500
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.setting_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.setting_root.resizable(0, 0)
        self.setting_root.iconbitmap(tools_ico)
        self.setting_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.setting_root.attributes("-topmost", True)  # 窗口置顶

        self.setting_button = setting_button
        self.setting_button_disable = setting_button_disable

        self.setting_button.place_forget()
        self.setting_button_disable.place(x=400, y=290)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context, 'setting_button', self.setting_button)
        setattr(Context, 'setting_button_disable', self.setting_button_disable)

        self.setting_root.protocol('WM_DELETE_WINDOW', self.setting_close_handle)  # 点击关闭按钮时执行的函数

        self.main_form()

    def setting_close_handle(self):
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context, 'setting_button').place(x=400, y=290)
        getattr(Context, 'setting_button_disable').place_forget()
        self.setting_root.destroy()

    def main_form(self):
        # 更改有道翻译的ID和KEY提示Label
        self.youdao_id_key_label = tk.Label(self.setting_root, text='更改有道翻译ID和KEY：', font=('方正楷体', 10), fg='red')
        self.youdao_id_key_label.place(x=20, y=20)

        # 有道翻译ID
        self.youdao_id_label = tk.Label(self.setting_root, text='有道翻译ID：', font=('方正楷体', 10))
        self.youdao_id_label.place(x=20, y=50)
        self.youdao_id_entry = tk.Entry(self.setting_root, font=('方正楷体', 10), width=30)
        self.youdao_id_entry.place(x=120, y=50)

        # 有道翻译KEY
        self.youdao_key_label = tk.Label(self.setting_root, text='有道翻译KEY：', font=('方正楷体', 10))
        self.youdao_key_label.place(x=20, y=80)
        self.youdao_key_entry = tk.Entry(self.setting_root, font=('方正楷体', 10), width=30)
        self.youdao_key_entry.place(x=120, y=80)

        # 点击更改按钮
        self.change_button = tk.Button(self.setting_root, text='更改', font=('方正楷体', 12),width=10)
        self.change_button_disable = tk.Button(self.setting_root, text='更改', font=('方正楷体', 12),width=10)
        self.change_button_disable.config(state='disabled')
        self.change_button.place(x=20, y=110)
        self.change_button.bind('<Button-1>', lambda event: self.change_id_key())

    def change_id_key(self):
        def t_change_id_key():
            self.change_button.place_forget()
            self.change_button_disable.place(x=20, y=110)
            youdao_id = self.youdao_id_entry.get()
            youdao_key = self.youdao_key_entry.get()
            self.setting_root.attributes("-topmost", False)
            if youdao_id == '' or youdao_key == '':
                tk.messagebox.showinfo('提示', '有道翻译ID和KEY不能为空！')
            else:
                # 显示文件
                win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_NORMAL)
                # 写进文件
                with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
                    f.write(f'Your_Id={youdao_id}\nYour_Key={youdao_key}')
                # 再次隐藏文件
                win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_HIDDEN)
                tk.messagebox.showinfo('提示', '更改有道翻译ID和KEY成功！')
            self.setting_root.attributes("-topmost", True)

            # 清空输入框
            self.youdao_id_entry.delete(0, 'end')
            self.youdao_key_entry.delete(0, 'end')

            self.change_button.place(x=20, y=110)
            self.change_button_disable.place_forget()

        t_change_id_key = threading.Thread(target=t_change_id_key)
        t_change_id_key.setDaemon(True)
        t_change_id_key.start()
