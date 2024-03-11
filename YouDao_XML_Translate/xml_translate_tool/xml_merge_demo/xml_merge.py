#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,re
import threading
from xml.etree import ElementTree as ElementTree
from xml.etree.ElementTree import Element
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox

doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'  # 工具临时文件路径
trans_log_path = trans_file + 'trans_log'  # 翻译工具日志存储
xml_file_path = trans_log_path + '\\xml_file_path.log'  # 记录多国语言xml文件路径
project_file_path = trans_log_path + '\\project_file_path.log'  # 记录项目路径
error_xml_path = trans_log_path + '\\merge_error.xml'
# error_xml_flag = False  # 是否有错误的xml文件
xml_show_tips_flag = False  # 只显示xml文件的提示信息一次


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径


def indent(elem, level=0):
    # 用于格式化xml文件  但是此时的xml文件和我们平时常见的格式不太一样，如何转变成标准的格式呢？ 思路就是在每个节点之后添加"\n\t"
    i = "\n" + level*"\t"  # 换行符+缩进符
    if len(elem):  # 如果elem有子元素
        if not elem.text or not elem.text.strip():  # 如果elem.text为空或者elem.text只包含空格
            elem.text = i + "\t"  # 将elem.text设置为换行符+缩进符+缩进符
        if not elem.tail or not elem.tail.strip():  # 如果elem.tail为空或者elem.tail只包含空格
            elem.tail = i  # 将elem.tail设置为换行符+缩进符
        for elem in elem:  # 遍历elem的子元素
            indent(elem, level+1)  # 递归调用indent函数
        if not elem.tail or not elem.tail.strip():  # 如果elem.tail为空或者elem.tail只包含空格
            elem.tail = i  # 将elem.tail设置为换行符+缩进符
    else:  # 如果elem没有子元素
        if level and (not elem.tail or not elem.tail.strip()):  # 如果elem.tail为空或者elem.tail只包含空格
            elem.tail = i  # 将elem.tail设置为换行符+缩进符


def insert_colored_text(text_box,text, fg_color='', bg_color=''):
    # 插入带颜色的文本，其中fg_color是字体颜色，bg_color是字体的背景颜色，text_box是文本框组件，text是要插入的文本
    text_box.tag_configure(fg_color, foreground=fg_color)
    text_box.tag_configure(bg_color, background=bg_color)
    text_box.insert("insert", text, (fg_color, bg_color))


def get_strings_xml_list(project_file_path):
    """
    获取项目中特定路径的所有strings.xml文件路径
    :param project_file_path:  项目路径
    :return:  返回所有strings.xml文件路径的列表
    :return: values_dir_list   返回所有带values-命名的文件夹路径
    """
    # 获取项目中特定路径的所有strings.xml文件路径
    strings_xml_list = []
    values_dir_list = []  # 获取所有带values命名的文件夹路径
    for root, dirs, files in os.walk(project_file_path):
        # 首先遍历文件夹，依次找到src、main、res、values文件夹，最后拼接成strings.xml文件路径
        if 'src' in dirs:
            src_path = os.path.join(root, 'src')
            for root, dirs, files in os.walk(src_path):
                if 'main' in dirs:
                    main_path = os.path.join(root, 'main')
                    for root, dirs, files in os.walk(main_path):
                        if 'res' in dirs:
                            res_path = os.path.join(root, 'res')
                            for root, dirs, files in os.walk(res_path):
                                # 获取所有带values命名的文件夹路径
                                for dir in dirs:
                                    if 'values-' in dir:
                                        values_dir_list.append(os.path.join(root, dir))
                                if 'values' in dirs:
                                    values_path = os.path.join(root, 'values')
                                    # 把 / 替换成 \ 以便于后面的拼接
                                    values_path = values_path.replace('/', '\\')
                                    strings_xml_path = values_path + '\\strings.xml'
                                    strings_xml_list.append(strings_xml_path)

    return {'strings_xml_list':strings_xml_list,'values_dir_list':values_dir_list}


def read_merge_xml(xml_file,text_box):
    global xml_show_tips_flag
    # global error_xml_flag
    # 读取多国语言xml文件

    # 首先创建一个空的xml文件
    # if not os.path.exists(error_xml_path):
    #     with open(error_xml_path, 'w', encoding='utf-8') as f:
    #         f.write('')
    #
    # if not error_xml_flag:  # 只执行一次寻找错误内容的逻辑
    #     # 找出错误格式无法读取的内容并写入error.xml文件
    #     error_list = []
    #     i = 1   # 记录错误格式的行数
    #     while True:  # 用while循环，如果该行中包含错误格式的内容，则删除该行，重新读取文件直到没有错误格式的内容
    #         with open(xml_file, 'r', encoding='utf-8') as f:
    #             lines = f.readlines()
    #             for line in lines:
    #                 if '&nbsp;' in line or '<br>' in line:
    #                     print('发现解析失败的内容：', line)
    #                     error_list.append(line)
    #                     # 把错误格式的内容显示在界面上
    #                     text_box.config(state='normal')
    #                     insert_colored_text(text_box, f'发现解析失败的内容：{line}\n', 'red', 'yellow')
    #                     text_box.config(state='disabled')
    #                     # 把错误格式的内容写入error.xml文件
    #                     with open(error_xml_path, 'a+', encoding='utf-8') as f:
    #                         # 然后每次有新内容写入时，在后面追加时间等信息
    #                         f.write('\n发现解析失败的内容：' + line)
    #                         f.write('发现时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
    #                     # 删除该行
    #                     lines.remove(line)
    #                     new_lines = ''.join(lines)
    #                     # 重新写入文件
    #                     with open(xml_file, 'w', encoding='utf-8') as f:
    #                         f.write(new_lines)
    #                     i += 1
    #
    #         # 再次读取文件，如果没有错误格式的内容，则跳出循环
    #         with open(xml_file, 'r', encoding='utf-8') as f:
    #             lines = f.readlines()
    #             for line in lines:
    #                 if '&nbsp;' in line or '<br>' in line:
    #                     print('再次发现解析失败的内容：', line)
    #                     error_list.append(line)
    #                     # 把错误格式的内容显示在界面上
    #                     text_box.config(state='normal')
    #                     insert_colored_text(text_box, f'再次发现解析失败的内容：{line}\n', 'red', 'yellow')
    #                     text_box.config(state='disabled')
    #                     with open(error_xml_path, 'a+', encoding='utf-8') as f:
    #                         # 然后每次有新内容写入时，在后面追加时间等信息
    #                         f.write('\n发现解析失败的内容：' + line)
    #                         f.write('发现时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
    #                     # 删除该行
    #                     lines.remove(line)
    #                     new_lines = ''.join(lines)
    #                     # 重新写入文件
    #                     with open(xml_file, 'w', encoding='utf-8') as f:
    #                         f.write(new_lines)
    #                     i += 1
    #                     continue
    #
    #         # 如果没有错误格式的内容（即小于循环行数），则跳出循环
    #         if len(error_list) < i:
    #             text_box.config(state='normal')
    #             insert_colored_text(text_box, f'错误内容已整理在：{error_xml_path}\n', 'blue', '')
    #             text_box.config(state='disabled')
    #             error_xml_flag = True
    #             break
    #
    # # 读取xml文件
    # tree = ElementTree.parse(xml_file)
    # # 获取根节点
    # root = tree.getroot()
    # # 获取所有的string标签
    # string_tags = root.findall('string')
    # # 获取所有的name值
    # name_list = []
    # for string_tag in string_tags:
    #     name_list.append(string_tag.get('name'))

    # 优化后的代码，兼容所有不合法的xml格式
    name_list = []
    text_list = []
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_data = f.read()
        # 获取所有的name值
        name = re.findall('<string name="(.*?)">.*?</string>', xml_data, re.S)
        name_list.extend(name)
        # print(name_list)
        # 获取所有的string值
        string_text = re.findall('<string name=".*?">(.*?)</string>', xml_data, re.S)
        text_list.extend(string_text)
        # print(text_list)
    if not xml_show_tips_flag:
        text_box.config(state='normal')
        insert_colored_text(text_box, f'{xml_file}共有{len(name_list)}个name值\n', 'blue', '')
        insert_colored_text(text_box, f'{xml_file}共有{len(text_list)}个文本内容\n', 'red', '')
        text_box.config(state='disabled')
        xml_show_tips_flag = True

    return {'name_list': name_list,'text_list':text_list}


def string_merge(name_list,text_list,strings_xml_file_path,merge_folder_name):
    # # 读取strings.xml文件
    # strings_tree = ElementTree.parse(strings_xml_file_path)
    # strings_root = strings_tree.getroot()
    # # 获取所有name值
    # strings_name_list = []
    # for string_tag in strings_root.findall('string'):
    #     strings_name_list.append(string_tag.get('name'))
    #
    # # 找出多国语言xml文件中的name值在strings.xml文件中相同的name值
    # same_name_list = []
    # for name in name_list:
    #     if name in strings_name_list:
    #         same_name_list.append(name)
    # print('same_name_list',same_name_list)
    #
    # # 然后把相同的name值从多国语言xml文件中找出对应的文本内容
    # string_text_list = []
    # for name in same_name_list:
    #     for string_tag in string_tags:
    #         if string_tag.get('name') == name:
    #             string_text_list.append(string_tag.text)
    # print('string_text_list',string_text_list)

    # 读取目标xml文件
    string_name_list = []
    string_text_list = []
    with open(strings_xml_file_path, 'r', encoding='utf-8') as f:
        strings_xml_data = f.read()
        # 获取所有的name值
        strings_name = re.findall('<string name="(.*?)">.*?</string>', strings_xml_data, re.S)
        string_name_list.extend(strings_name)
        # print(string_name_list)
        # 获取所有的string值
        strings_string_text = re.findall('<string name=".*?">(.*?)</string>', strings_xml_data, re.S)
        string_text_list.extend(strings_string_text)
        # print(string_text_list)

    # 找出多国语言xml文件中的name值在strings.xml文件中相同的name值
    same_name_list = []
    for i in name_list:
        if i in string_name_list:
            same_name_list.append(i)
    # print(same_name_list)

    # 然后把相同的name值从多国语言xml文件中找出对应的文本内容
    same_text_list = []
    for i in same_name_list:
        index = name_list.index(i)  # 获取相同name值在多国语言xml文件中的索引
        same_text_list.append(text_list[index])
    # print(same_text_list)

    # 返回上一级新建values-new文件夹并写入其中的strings.xml文件中
    values_new_file = os.path.join(os.path.dirname(strings_xml_file_path.split('values')[0]), merge_folder_name)
    if not os.path.exists(values_new_file):
        os.makedirs(values_new_file)

    # 创建新的strings.xml文件到values-new文件夹中
    new_strings_xml_file = os.path.join(values_new_file, 'strings.xml')
    print(new_strings_xml_file)

    with open(new_strings_xml_file, 'w', encoding='utf-8') as f:
        f.write('<resources>\n')

    with open(new_strings_xml_file, 'a', encoding='utf-8') as f:
        for name, text in zip(same_name_list, same_text_list):
            f.write(f'    <string name="{name}">{text}</string>\n')

    # 最后添加</resources>标签
    with open(new_strings_xml_file, 'a', encoding='utf-8') as f:
        f.write('</resources>')


class Context:
    pass  # 创建一个空类,用于存储全局变量


# 创建多国语言xml合并功能窗口
class MergeXml(object):
    def root_form(self,merge_xml_button,merge_xml_button_disable):
        self.merge_xml_root = tk.Toplevel()
        self.merge_xml_root.title('多国语言xml合并')
        screenWidth = self.merge_xml_root.winfo_screenwidth()
        screenHeight = self.merge_xml_root.winfo_screenheight()
        w = 500
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.merge_xml_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.merge_xml_root.resizable(0, 0)
        self.merge_xml_root.iconbitmap(tools_ico)
        self.merge_xml_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.merge_xml_root.attributes("-topmost", True)  # 窗口置顶

        self.merge_xml_button = merge_xml_button
        self.merge_xml_button_disable = merge_xml_button_disable

        self.merge_xml_button.place_forget()
        self.merge_xml_button_disable.place(x=400, y=170)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context,'merge_xml_button',self.merge_xml_button)
        setattr(Context,'merge_xml_button_disable',self.merge_xml_button_disable)

        self.merge_xml_root.protocol('WM_DELETE_WINDOW', self.merge_close_handle)  # 点击关闭按钮时执行的函数
        self.main_form()

    def merge_close_handle(self):
        print('关闭窗口')
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context,'merge_xml_button').place(x=400, y=170)
        getattr(Context,'merge_xml_button_disable').place_forget()
        self.merge_xml_root.destroy()

    def main_form(self):
        # 多国语言xml文件路径提示
        self.merge_xml_label = tk.Label(self.merge_xml_root, text='多国语言xml文件路径：')
        self.merge_xml_label.place(x=10, y=10)

        # 多国语言xml文件路径输入框
        self.merge_xml_entry = tk.Entry(self.merge_xml_root,width=45)
        self.merge_xml_entry.place(x=30, y=40)
        # 打开记录的多国语言xml文件路径
        if not os.path.exists(xml_file_path):
            with open(xml_file_path,'w',encoding='utf-8') as f:
                f.truncate()
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            self.merge_xml_entry.insert(0, f.read())

        # 多国语言xml文件路径选择按钮
        self.merge_xml_button = tk.Button(self.merge_xml_root, text='浏览多国xml路径')
        self.merge_xml_button_disable = tk.Button(self.merge_xml_root, text='浏览多国xml路径')
        self.merge_xml_button_disable.config(state='disabled')
        self.merge_xml_button.place(x=360, y=35)
        self.merge_xml_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_merge_xml_path).start())

        # 项目路径提示
        self.project_path_label = tk.Label(self.merge_xml_root, text='项目路径：')
        self.project_path_label.place(x=10, y=80)

        # 项目路径输入框
        self.project_path_entry = tk.Entry(self.merge_xml_root,width=45)
        self.project_path_entry.place(x=30, y=110)
        # 打开记录的项目路径
        if not os.path.exists(project_file_path):
            with open(project_file_path,'w',encoding='utf-8') as f:
                f.truncate()
        with open(project_file_path, 'r', encoding='utf-8') as f:
            self.project_path_entry.insert(0, f.read())

        # 项目路径选择按钮
        self.project_path_button = tk.Button(self.merge_xml_root, text='浏览项目路径')
        self.project_path_button_disable = tk.Button(self.merge_xml_root, text='浏览项目路径')
        self.project_path_button_disable.config(state='disabled')
        self.project_path_button.place(x=360, y=105)
        self.project_path_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_project_path).start())

        # 创建合并后的文件夹名称输入框
        self.merge_folder_name_label = tk.Label(self.merge_xml_root, text='合并后的文件夹名称：')
        self.merge_folder_name_label.place(x=10, y=140)
        self.merge_folder_name_entry = tk.Entry(self.merge_xml_root,width=20)
        self.merge_folder_name_entry.place(x=30, y=160)
        self.merge_folder_name_entry.insert(0, 'values-')

        # 创建点击合并按钮
        self.merge_button = tk.Button(self.merge_xml_root, text='合并',width=10)
        self.merge_button_disable = tk.Button(self.merge_xml_root, text='合并',width=10)
        self.merge_button_disable.config(state='disabled')
        self.merge_button.place(x=200, y=150)
        self.merge_button.bind('<Button-1>', lambda x:threading.Thread(target=self.merge_xml).start())

        # 显示合并日志信息框
        self.merge_log_text = tk.Text(self.merge_xml_root, width=60, height=13)
        self.merge_log_text.place(x=20, y=200)
        # 设置只读
        self.merge_log_text.config(state='disabled')

        # 创建滚动条
        self.merge_log_scroll = tk.Scrollbar(self.merge_xml_root)
        self.merge_log_scroll.place(x=445, y=195, height=180)
        # 绑定滚动条
        self.merge_log_scroll.config(command=self.merge_log_text.yview)
        self.merge_log_text.config(yscrollcommand=self.merge_log_scroll.set)
        # 创建横向滚动条
        self.merge_log_scroll_x = tk.Scrollbar(self.merge_xml_root, orient=tk.HORIZONTAL)
        self.merge_log_scroll_x.place(x=20, y=370, width=425)
        # 绑定横向滚动条
        self.merge_log_scroll_x.config(command=self.merge_log_text.xview)
        self.merge_log_text.config(xscrollcommand=self.merge_log_scroll_x.set)

    def open_merge_xml_path(self):
        # 打开多国语言xml文件路径，过滤出xml文件
        self.merge_xml_button.place_forget()
        self.merge_xml_button_disable.place(x=360, y=35)
        self.merge_xml_root.attributes("-topmost", False)
        self.merge_xml_path = filedialog.askopenfilename(title='选择多国语言xml文件', filetypes=[('xml文件', '*.xml')])
        # 先清空输入框
        self.merge_xml_entry.delete(0, tk.END)
        self.merge_xml_entry.insert(0, self.merge_xml_path)

        # 保存多国语言xml文件路径
        with open(xml_file_path, 'w', encoding='utf-8') as f:
            f.write(self.merge_xml_path)
        self.merge_xml_root.attributes("-topmost", True)
        self.merge_xml_button_disable.place_forget()
        self.merge_xml_button.place(x=360, y=35)

    def open_project_path(self):
        # 打开项目路径
        self.project_path_button.place_forget()
        self.project_path_button_disable.place(x=360, y=105)
        self.merge_xml_root.attributes("-topmost", False)
        self.project_path = filedialog.askdirectory(title='选择项目路径')
        # 先清空输入框
        self.project_path_entry.delete(0, tk.END)
        self.project_path_entry.insert(0, self.project_path)

        # 保存项目路径
        with open(project_file_path, 'w', encoding='utf-8') as f:
            f.write(self.project_path)
        self.merge_xml_root.attributes("-topmost", True)
        self.project_path_button_disable.place_forget()
        self.project_path_button.place(x=360, y=105)

    def merge_xml(self):
        global xml_show_tips_flag
        # 合并xml主逻辑
        self.merge_button.place_forget()
        self.merge_button_disable.place(x=200, y=150)

        if not os.path.exists(self.merge_xml_entry.get()) or not os.path.exists(self.project_path_entry.get()):
            self.merge_log_text.config(state='normal')
            self.merge_log_text.insert(tk.END, '请检查多国语言xml文件路径或项目路径是否正确！\n')
            self.merge_log_text.config(state='disabled')
            self.merge_log_text.see(tk.END)
        else:
            # 日志信息清空
            self.merge_log_text.config(state='normal')
            self.merge_log_text.delete(1.0, tk.END)

            # 获取合并后文件夹名称的名称
            merge_folder_name = self.merge_folder_name_entry.get()
            if merge_folder_name.strip() == 'values-':
                self.merge_xml_root.attributes("-topmost", False)
                messagebox.showerror('合并失败', '需要填写完整合并后的文件夹名称，例如“values-en”')
                self.merge_log_text.insert(tk.END, '需要填写完整合并后的文件夹名称，例如“values-en”！\n')
                self.merge_log_text.config(state='disabled')
                self.merge_xml_root.attributes("-topmost", True)
            else:
                # 继续写入日志
                self.merge_log_text.insert(tk.END, '###########################\n')
                self.merge_log_text.insert(tk.END, '开始合并xml文件中...\n')
                self.merge_log_text.insert(tk.END, '开始寻找项目中符合条件的strings.xml文件...\n')
                self.merge_log_text.config(state='disabled')

                # 首先获取项目路径符合条件的strings.xml文件路径
                strings_xml_dict = get_strings_xml_list(self.project_path_entry.get())
                self.merge_log_text.config(state='normal')
                self.merge_log_text.insert(tk.END, '寻找到符合条件的strings.xml文件如下：\n')
                self.merge_log_text.config(state='disabled')

                # 遍历strings.xml文件路径，然后合并
                for strings_xml in strings_xml_dict['strings_xml_list']:
                    # 读取多国语言xml文件
                    merge_xml_dict = read_merge_xml(self.merge_xml_entry.get(),self.merge_log_text)

                    # 拼接合并后的文件夹路径，去掉values，从res开始
                    merge_folder_path = strings_xml.replace('values', merge_folder_name)
                    print(merge_folder_path)
                    # 判断合并后的文件夹是否存在，不存在则合并，存在则跳过
                    if os.path.exists(merge_folder_path):
                        self.merge_log_text.config(state='normal')
                        self.merge_log_text.insert(tk.END, f'发现{merge_folder_name}文件夹重复，已跳过文件：' + merge_folder_path + '\n')
                        self.merge_log_text.config(state='disabled')
                        self.merge_log_text.see(tk.END)
                    else:
                        # 合并文件
                        self.merge_log_text.config(state='normal')
                        self.merge_log_text.insert(tk.END, '开始合并文件：' + merge_folder_path + '\n')
                        self.merge_log_text.config(state='normal')
                        self.merge_log_text.see(tk.END)  # 滚动条自动滚动到最后
                        string_merge(merge_xml_dict['name_list'],merge_xml_dict['text_list'],strings_xml,merge_folder_name)

                xml_show_tips_flag = False
                self.merge_log_text.config(state='normal')
                self.merge_log_text.insert(tk.END, '所有文件合并完成!!!\n')
                self.merge_log_text.insert(tk.END, '###########################\n')
                self.merge_log_text.config(state='disabled')

        self.merge_button_disable.place_forget()
        self.merge_button.place(x=200, y=150)



