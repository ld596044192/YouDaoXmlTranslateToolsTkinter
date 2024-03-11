#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import threading
import time
# 单个xml文件翻译
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk, tkinter.messagebox
import os,sys
from xml.etree import ElementTree as ET
from YouDao_XML_Translate.xml_translate_tool.youdao_demo import YouDao
from YouDao_XML_Translate.xml_translate_tool.my_thread import MyThread


single_translate_file_path = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\single_translate_da'  # 翻译文件夹路径
if not os.path.exists(single_translate_file_path):
    os.makedirs(single_translate_file_path)
doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'  # 工具临时文件路径
trans_log_path = trans_file + 'trans_log'  # 翻译工具日志存储
single_file_path = trans_log_path + '\\single_file_path.log'  # 单个xml文件翻译的文件路径


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径
single_language_txt = resource_path(os.path.join('extra_functions','single_language_youdao.txt')) # 单个xml文件翻译语言列表


class Context:
    pass


class SingleXmlTranslate(object):
    def root_form(self,single_xml_button,single_xml_button_disable):
        # 窗口
        self.single_xml_root = tk.Toplevel()
        self.single_xml_root.title('单个xml文件翻译')
        screenWidth = self.single_xml_root.winfo_screenwidth()
        screenHeight = self.single_xml_root.winfo_screenheight()
        w = 500
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.single_xml_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.single_xml_root.resizable(0, 0)
        self.single_xml_root.iconbitmap(tools_ico)
        self.single_xml_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.single_xml_root.attributes("-topmost", True)  # 窗口置顶

        self.single_xml_button = single_xml_button
        self.single_xml_button_disable = single_xml_button_disable

        self.single_xml_button.place_forget()
        self.single_xml_button_disable.place(x=400, y=130)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context, 'single_xml_button', self.single_xml_button)
        setattr(Context, 'single_xml_button_disable', self.single_xml_button_disable)

        self.main_form()
        self.single_xml_root.protocol('WM_DELETE_WINDOW', self.single_close_handle)  # 点击关闭按钮时执行的函数

    def single_close_handle(self):
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context, 'single_xml_button').place(x=400, y=130)
        getattr(Context, 'single_xml_button_disable').place_forget()
        self.single_xml_root.destroy()

    def main_form(self):
        # xml文件路径提示
        self.xml_path_label = tk.Label(self.single_xml_root, text='单个xml文件路径：')
        self.xml_path_label.place(x=10, y=20)

        # xml文件路径输入框
        self.xml_path = tk.StringVar()
        self.xml_path_entry = tk.Entry(self.single_xml_root, textvariable=self.xml_path, width=45)
        self.xml_path_entry.place(x=20, y=50)
        # 保存输入框的路径
        if not os.path.exists(single_file_path):
            with open(single_file_path, 'w', encoding='utf-8') as f:
                f.write('')
        with open(single_file_path, 'r', encoding='utf-8') as f:
            self.xml_path_entry.insert(tk.END, f.read())

        # 浏览xml文件按钮
        self.xml_path_button = tk.Button(self.single_xml_root, text='选择xml文件')
        self.xml_path_button_disable = tk.Button(self.single_xml_root, text='选择xml文件')
        self.xml_path_button_disable.config(state='disabled')
        self.xml_path_button.place(x=350, y=45)
        self.xml_path_button.config(command=self.xml_path_button_click)

        # 翻译语言选择下拉框
        self.translate_language = tk.StringVar()
        self.translate_language.set('中文 zh-CHS')
        self.translate_language_label = tk.Label(self.single_xml_root, text='翻译语言：')
        self.translate_language_label.place(x=10, y=80)
        self.translate_language_combobox = tk.ttk.Combobox(self.single_xml_root, textvariable=self.translate_language, width=25, state='readonly')
        # 读取翻译语言列表
        with open(single_language_txt, 'r', encoding='utf-8') as f:
            # 先读取然后把中间的空格只保存一个
            self.translate_language_combobox['value'] = [' '.join(i.split()) for i in f.readlines()]
        self.translate_language_combobox.place(x=100, y=80)

        # 翻译按钮
        self.translate_button = tk.Button(self.single_xml_root, text='点击翻译')
        self.translate_button_disable = tk.Button(self.single_xml_root, text='点击翻译')
        self.translate_button_disable.config(state='disabled')
        self.translate_button.place(x=30, y=120)
        self.translate_button.bind('<Button-1>',lambda x:self.start_trans_bind())

        # 停止翻译按钮
        self.stop_translate_button = tk.Button(self.single_xml_root, text='停止翻译')
        self.stop_translate_button_disable = tk.Button(self.single_xml_root, text='停止翻译')
        self.stop_translate_button_disable.place(x=150, y=120)
        self.stop_translate_button_disable.config(state='disabled')
        self.stop_translate_button.bind('<Button-1>',lambda x:self.stop_trans_bind())

        # 暂停恢复翻译按钮
        self.pause_translate_button = tk.Button(self.single_xml_root, text='暂停翻译')
        self.pause_translate_button_disable = tk.Button(self.single_xml_root, text='暂停翻译')
        self.pause_translate_button_disable.config(state='disabled')
        self.resume_translate_button = tk.Button(self.single_xml_root, text='恢复翻译')
        self.pause_translate_button_disable.place(x=270, y=120)
        self.pause_translate_button.bind('<Button-1>',lambda x:self.stop_resume_bind())
        self.resume_translate_button.bind('<Button-1>',lambda x:self.resume_bind())

        # 打开翻译后的文件夹按钮
        self.open_xml_button = tk.Button(self.single_xml_root, text='打开翻译文件夹')
        self.open_xml_button_disable = tk.Button(self.single_xml_root, text='打开翻译文件夹')
        self.open_xml_button_disable.config(state='disabled')
        self.open_xml_button.place(x=370, y=120)
        # 打开翻译后的文件夹
        self.open_xml_button.bind('<Button-1>', lambda x: os.startfile(single_translate_file_path))

        # 显示翻译内容listbox并配置滚动条
        self.translate_content_listbox = tk.Listbox(self.single_xml_root, width=60, height=10)
        self.translate_content_listbox.place(x=20, y=160)
        self.translate_content_listbox_scrollbar_y = tk.Scrollbar(self.single_xml_root)
        self.translate_content_listbox_scrollbar_y.place(x=445, y=160, height=185)
        self.translate_content_listbox.config(yscrollcommand=self.translate_content_listbox_scrollbar_y.set)
        self.translate_content_listbox_scrollbar_y.config(command=self.translate_content_listbox.yview)
        # 横向滚动条
        self.translate_content_listbox_scrollbar_x = tk.Scrollbar(self.single_xml_root, orient='horizontal')
        self.translate_content_listbox_scrollbar_x.place(x=20, y=345, width=423)
        self.translate_content_listbox.config(xscrollcommand=self.translate_content_listbox_scrollbar_x.set)
        self.translate_content_listbox_scrollbar_x.config(command=self.translate_content_listbox.xview)

    def xml_path_button_click(self):
        # 浏览并选择xml文件
        self.xml_path_button.place_forget()
        self.xml_path_button_disable.place(x=350, y=45)
        self.single_xml_root.attributes("-topmost", False)
        self.xml_path.set(tk.filedialog.askopenfilename(title='选择xml文件', filetypes=[('xml文件', '*.xml')]))
        # 保存输入框的路径
        if not os.path.exists(single_file_path):
            with open(single_file_path, 'w', encoding='utf-8') as f:
                f.write('')
        with open(single_file_path, 'w', encoding='utf-8') as f:
            f.write(self.xml_path.get())
        try:
            self.single_xml_root.attributes("-topmost", True)
        except Exception:
            pass
        self.xml_path_button_disable.place_forget()
        self.xml_path_button.place(x=350, y=45)

    def single_translate(self,stop_event):
        global stop_event_flag
        stop_event_flag = False

        # 单个xml文件翻译
        self.translate_button.place_forget()
        self.translate_button_disable.place(x=30, y=120)
        self.stop_translate_button_disable.place_forget()
        self.stop_translate_button.place(x=150, y=120)
        self.pause_translate_button_disable.place_forget()
        self.pause_translate_button.place(x=270, y=120)

        if self.xml_path.get() == '':
            tk.messagebox.showerror('错误', '文件夹路径不能为空')
        else:
            # 获取翻译语言
            self.translate_language_value = self.translate_language.get().split()[-1]

            # 保存输入框的路径
            if not os.path.exists(single_file_path):
                with open(single_file_path, 'w', encoding='utf-8') as f:
                    f.write('')
            with open(single_file_path, 'w', encoding='utf-8') as f:
                f.write(self.xml_path.get())

            # 根据当前时间创建文件夹
            # 获取当前时间
            now_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            # 创建文件夹
            new_translate_path = os.path.join(single_translate_file_path, now_time)
            os.mkdir(new_translate_path)

            self.single_lock = threading.Lock()  # 翻译锁
            setattr(Context, 'stop_event_flag', stop_event_flag)  # 设置停止翻译标志位 - 反射机制

            # 读取xml文件
            # tree = ET.parse(self.xml_path.get())
            # root = tree.getroot()
            # # 获取所有的string标签
            # string_list = root.findall('string')
            # # 获取所有name值
            # string_name_list = [i.attrib['name'] for i in string_list]
            # # 获取里面所有翻译内容
            # string_content_list = [i.text for i in string_list]

            with open(self.xml_path.get(),'r',encoding='utf-8') as f:
                xml_line = f.read()
                string_name_list = re.findall(r'<string name="(.*?)">.*?</string>',xml_line,re.S)
                string_content_list = re.findall(r'<string name=".*?">(.*?)</string>',xml_line,re.S)

            # 最后过滤掉不需要翻译的name值，比如含有translatable="false的name值
            # 首先先找出translatable="false的name值，然后根据这些name值找出对应的索引，然后删除这些索引的name值和翻译内容
            translatable_false_name_list = [i for i in string_name_list if 'translatable="false' in i]
            for translatable_false_name in translatable_false_name_list:
                index = string_name_list.index(translatable_false_name)
                del string_name_list[index]
                del string_content_list[index]

            print('最终得到的翻译内容：',string_name_list,string_content_list,sep='\n')

            # 翻译内容
            for string_name,string_content in zip(string_name_list, string_content_list):
                if stop_event.is_set():  # 停止接下来的所有翻译
                    self.translate_content_listbox.insert(tk.END, '翻译已停止')
                    print("Stopping all thread...")
                    return

                youdao = YouDao(string_content, self.translate_language_value, string_name, self.xml_path.get(),
                                            self.translate_content_listbox,'single',single_new_path=new_translate_path)  # single代表单个xml文件翻译
                youdao.connect()
                time.sleep(1)

                if stop_event_flag:
                    self.single_lock.acquire()  # 获取锁

            if stop_event.is_set():
                self.translate_content_listbox.insert(tk.END, '翻译已停止')
            else:
                self.translate_content_listbox.insert(tk.END, '翻译完成')
            self.translate_content_listbox.insert(tk.END, '翻译文件保存在：' + new_translate_path)
            self.translate_content_listbox.see(tk.END)

        self.translate_button_disable.place_forget()
        self.translate_button.place(x=30, y=120)
        self.stop_translate_button.place_forget()
        self.stop_translate_button_disable.place(x=150, y=120)
        self.pause_translate_button.place_forget()
        self.pause_translate_button_disable.place(x=270, y=120)
        self.resume_translate_button.place_forget()

    def start_trans_bind(self):
        # 启动翻译按钮线程
        single_thread = MyThread(self.single_translate)  # 创建线程
        self.single_thread = single_thread
        self.single_thread.start()  # 启动线程

    def stop_trans_bind(self):
        def t_stop_trans():
            # 停止翻译按钮绑定事件
            self.single_xml_root.attributes("-topmost", False)
            if tk.messagebox.askyesno('停止提示', '正在翻译中，是否需要停止翻译？'):
                self.single_thread.stop()

                try:
                    self.single_lock.release()
                except Exception:
                    pass

                # 恢复按钮状态
                self.translate_button_disable.place_forget()
                self.translate_button.place(x=30, y=120)
                self.stop_translate_button.place_forget()
                self.stop_translate_button_disable.place(x=150, y=120)
                self.pause_translate_button.place_forget()
                self.pause_translate_button_disable.place(x=270, y=120)
                self.resume_translate_button.place_forget()

            self.single_xml_root.attributes("-topmost", True)

        t_stop_trans = threading.Thread(target=t_stop_trans)
        t_stop_trans.setDaemon(True)
        t_stop_trans.start()

    def stop_resume_bind(self):
        def t_stop_resume():
            # 暂停翻译
            self.single_xml_root.attributes("-topmost", False)
            if tk.messagebox.askyesno('暂停提示', '正在翻译中，是否需要暂停翻译？'):
                global stop_event_flag
                stop_event_flag = True
                setattr(Context, 'stop_event_flag', stop_event_flag)
                self.pause_translate_button.place_forget()
                self.resume_translate_button.place(x=270, y=120)
                self.translate_content_listbox.insert(tk.END, '已暂停翻译...')
            self.single_xml_root.attributes("-topmost", True)

        t_stop_resume = threading.Thread(target=t_stop_resume)
        t_stop_resume.setDaemon(True)
        t_stop_resume.start()

    def resume_bind(self):
        def t_resume():
            # 恢复翻译
            global stop_event_flag
            stop_event_flag = False
            setattr(Context, 'stop_event_flag', stop_event_flag)
            self.single_lock.release()  # 释放锁
            self.resume_translate_button.place_forget()
            self.pause_translate_button.place(x=270, y=120)
            self.translate_content_listbox.insert(tk.END, '已恢复翻译...')

        t_resume = threading.Thread(target=t_resume)
        t_resume.setDaemon(True)
        t_resume.start()

