#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,os,sys
import threading
import tkinter as tk
import tkinter.filedialog as filedialog

# 两个xml文件的比较

doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'  # 工具临时文件路径
trans_log_path = trans_file + 'trans_log'  # 翻译工具日志存储
compare_xml_file_path = trans_log_path + '\\compare_xml_file_path.log'  # 记录多国语言xml文件路径
compare_file_path = trans_log_path + '\\compare_file_path.log'  # 记录目标xml文件路径
new_xml_file_path = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\new_xml_da.xml'  # 新的xml文件路径


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径


def insert_colored_text(text_box,text, fg_color='', bg_color=''):
    # 插入带颜色的文本，其中fg_color是字体颜色，bg_color是字体的背景颜色，text_box是文本框组件，text是要插入的文本
    text_box.tag_configure(fg_color, foreground=fg_color)
    text_box.tag_configure(bg_color, background=bg_color)
    text_box.insert("insert", text, (fg_color, bg_color))


def compare_xml(xml_file_path1, xml_file_path2,text_box):
    """
    两个xml文件的比较
    :param xml_file_path1: 多国语言xml文件路径
    :param xml_file_path2: 目标xml文件路径
    :return text_box: 显示比较结果的文本框
    """
    # 两个xml对比逻辑
    # 读取多国语言xml文件，获取所有name值，然后与目标xml文件对比，如果两者name值一样，则继续对比文本内容，否则跳过；
    # 如果文本内容也一样则跳过，否则将多国语言xml文件中的整行内容添加到新的xml文件中（就是找同一name值但不一样的文本内容）
    # 获取两个xml的name值
    # 清空new_xml_da.xml文件
    with open(new_xml_file_path, 'w', encoding='utf-8') as f:
        f.write(f'<resources>\n')

    # 读取多国语言xml文件
    # values_name_list = []
    # target_name_list = []
    # with open(xml_file_path1, 'r', encoding='utf-8') as f:
    #     xml_line = f.readlines()
    #     # 读取目标xml文件
    #     with open(xml_file_path2, 'r', encoding='utf-8') as f2:
    #         target_xml_line = f2.readlines()
    #         # 如果多国语言xml文件中的name值在目标xml文件中存在，则提取出来
    #         for line in xml_line[1:-2]:
    #             # 正则表达式精准获取name，如果出现<!-- -->注释，则需要过滤掉注释的name
    #             if '<!--' not in line and 'name' in line:
    #                 try:
    #                     values_name = re.findall('<string name="(.*?)">.*?</string>', line)[0]
    #                 except Exception:
    #                     values_name = line.split('name="')[1].split('"')[0]
    #                 # print(values_name)    # 获取到的name值
    #                 values_name_list.append(values_name)
    #             elif 'name' not in line:
    #                 # 如果没有name，则将此行内容显示到text_box中
    #                 text_box.config(state='normal')
    #                 insert_colored_text(text_box, f'\n已过滤没有name的内容（此处提醒查漏补缺）:\n {line}', 'blue','yellow')
    #                 text_box.config(state='disabled')
    #         for target_line in target_xml_line:
    #             if 'name' in target_line:
    #                 # 正则表达式精准获取name，如果出现<!-- -->注释，则需要过滤掉注释的name
    #                 if '<!--' not in target_line:
    #                     try:
    #                         target_name = re.findall('<string name="(.*?)">.*?</string>', target_line)[0]
    #                     except Exception:
    #                         target_name = target_line.split('name="')[1].split('"')[0]
    #                     # print(target_name)    # 获取到的name值
    #                     target_name_list.append(target_name)
    #             elif 'name' not in line:
    #                 # 如果没有name，则将此行内容显示到text_box中
    #                 text_box.config(state='normal')
    #                 insert_colored_text(text_box, f'\n已过滤没有name的内容（此处提醒查漏补缺）:\n {line}', 'blue',
    #                                     'yellow')
    #                 text_box.config(state='disabled')

    # 优化后的代码，兼容没有name那行的情况
    values_name_list = []
    target_name_list = []
    with open(xml_file_path1, 'r', encoding='utf-8') as f:
        xml_line = f.read()
        # 读取目标xml文件
        with open(xml_file_path2, 'r', encoding='utf-8') as f2:
            target_xml_line = f2.read()
            if '<!--' not in xml_line:
                values_name = re.findall('<string name="(.*?)">.*?</string>', xml_line, re.S)  # re.S 匹配包括换行在内的所有字符
                # print(values_name)    # 获取到的name值
                values_name_list.extend(values_name)  # extend() 方法用于在列表末尾一次性追加另一个序列中的多个值
            if '<!--' not in target_xml_line:
                target_name = re.findall('<string name="(.*?)">.*?</string>', target_xml_line, re.S)
                # print(target_name)    # 获取到的name值
                target_name_list.extend(target_name)

    # 获取两个xml文件的文本内容
    # values_text_list = []
    # target_text_list = []
    # for line in xml_line:
    #     if 'name' in line:
    #         if '<!--' not in line:
    #             try:
    #                 values_text = re.findall('<string name=".*?">(.*?)</string>', line)[0]
    #             except Exception:
    #                 values_text = line.split('>')[1].split('<')[0]
    #             values_text_list.append(values_text)
    # for target_line in target_xml_line:
    #     if 'name' in target_line:
    #         if '<!--' not in target_line and target_line.strip().startswith('<string name'):
    #             try:
    #                 target_text = re.findall('<string name=".*?">(.*?)</string>', target_line)[0]
    #             except Exception:
    #                 target_text = target_line.split('>')[1].split('<')[0]
    #             target_text_list.append(target_text)

    # 优化后的代码，兼容文本内容换行后获取不到的情况
    values_text_list = []
    target_text_list = []
    if '<!--' not in xml_line:
        values_text = re.findall('<string name=".*?">(.*?)</string>', xml_line, re.S)
        values_text_list.extend(values_text)
        # print(values_text_list)
    if '<!--' not in target_xml_line:
        # 正则表达式匹配出所有的文本内容，包含换行符
        target_text = re.findall('<string name=".*?">(.*?)</string>', target_xml_line, re.S)  # re.S 匹配包括换行在内的所有字符
        target_text_list.extend(target_text)
        # print(target_text_list)

    # 对比两个xml文件的name值，如果相同则继续对比文本内容，否则跳过
    for values_name in values_name_list:
        for target_name in target_name_list:
            if values_name == target_name:
                # 对比两个xml文件的文本内容，如果相同则跳过，否则将多国语言xml文件中的整行内容添加到新的xml文件中
                # 根据相同的内容获取不同索引
                values_index = values_name_list.index(values_name)
                target_index = target_name_list.index(target_name)
                # 根据索引获取文本内容
                values_text = values_text_list[values_index]
                target_text = target_text_list[target_index]
                # 对比文本内容
                if values_text != target_text:
                    # 将多国语言xml文件中的整行内容添加到新的xml文件中
                    with open(new_xml_file_path, 'a', encoding='utf-8') as f3:
                        xml_name = values_name_list[values_index]
                        xml_text = values_text_list[values_index]
                        f3.write(f'    <string name="{xml_name}">{xml_text}</string>\n')
                        print(f'寻找到相同name但不同的文本内容并从多国语言xml文件提取出来: \n <string name="{xml_name}">{xml_text}</string>')
                        # 显示比较结果
                        text_box.config(state='normal')
                        text_box.insert(tk.END, f'\n寻找到相同name但不同的文本内容并从多国语言xml文件提取出来: \n <string name="{xml_name}">{xml_text}</string>\n')
                        text_box.config(state='disabled')
                        text_box.see(tk.END)

    # 最后添加</resources>标签
    with open(new_xml_file_path, 'a', encoding='utf-8') as f4:
        f4.write('</resources>')

    # 显示生成的新xml文件路径
    text_box.config(state='normal')
    insert_colored_text(text_box, f'\n比较完成，已生成的新xml文件路径为: {new_xml_file_path}', 'red')
    text_box.config(state='disabled')


class Context:
    pass


class CompareXml(object):
    def root_form(self,compare_xml_button,compare_xml_button_disable):
        self.compare_xml_root = tk.Toplevel()
        self.compare_xml_root.title('xml对比工具')
        screenWidth = self.compare_xml_root.winfo_screenwidth()
        screenHeight = self.compare_xml_root.winfo_screenheight()
        w = 500
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.compare_xml_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.compare_xml_root.resizable(0, 0)
        self.compare_xml_root.iconbitmap(tools_ico)
        self.compare_xml_root.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.compare_xml_root.attributes("-topmost", True)  # 窗口置顶

        self.compare_xml_button = compare_xml_button
        self.compare_xml_button_disable = compare_xml_button_disable

        self.compare_xml_button.place_forget()
        self.compare_xml_button_disable.place(x=400, y=210)

        # 使用反射机制，把按钮对象存储到全局变量中，方便在关闭窗口时，把按钮状态改为可用（确保按钮对象为同一个）
        setattr(Context,'compare_xml_button',self.compare_xml_button)
        setattr(Context,'compare_xml_button_disable',self.compare_xml_button_disable)

        self.compare_xml_root.protocol('WM_DELETE_WINDOW', self.compare_close_handle)  # 点击关闭按钮时执行的函数
        self.main_form()

    def compare_close_handle(self):
        print('关闭窗口')
        # 关闭窗口时，把按钮状态改为可用
        getattr(Context,'compare_xml_button').place(x=400, y=210)
        getattr(Context,'compare_xml_button_disable').place_forget()
        self.compare_xml_root.destroy()

    def main_form(self):
        # 多国语言xml文件路径提示
        self.compare_xml_label = tk.Label(self.compare_xml_root, text='多国语言xml文件路径：')
        self.compare_xml_label.place(x=10, y=10)

        # 多国语言xml文件路径输入框
        self.compare_xml_entry = tk.Entry(self.compare_xml_root, width=45)
        self.compare_xml_entry.place(x=30, y=40)
        # 打开记录的多国语言xml文件路径
        if not os.path.exists(compare_xml_file_path):
            with open(compare_xml_file_path, 'w', encoding='utf-8') as f:
                f.truncate()
        with open(compare_xml_file_path, 'r', encoding='utf-8') as f:
            self.compare_xml_entry.insert(0, f.read())

        # 多国语言xml文件路径选择按钮
        self.compare_xml_button = tk.Button(self.compare_xml_root, text='浏览多国xml路径')
        self.compare_xml_button_disable = tk.Button(self.compare_xml_root, text='浏览多国xml路径')
        self.compare_xml_button_disable.config(state='disabled')
        self.compare_xml_button.place(x=360, y=35)
        self.compare_xml_button.bind('<Button-1>', lambda x: threading.Thread(target=self.open_compare_xml_path).start())

        # 目标xml路径提示
        self.target_path_label = tk.Label(self.compare_xml_root, text='目标xml文件路径：')
        self.target_path_label.place(x=10, y=80)

        # 目标xml路径输入框
        self.target_path_entry = tk.Entry(self.compare_xml_root, width=45)
        self.target_path_entry.place(x=30, y=110)
        # 打开记录的目标xml文件路径
        if not os.path.exists(compare_file_path):
            with open(compare_file_path, 'w', encoding='utf-8') as f:
                f.truncate()
        with open(compare_file_path, 'r', encoding='utf-8') as f:
            self.target_path_entry.insert(0, f.read())

        # 目标xml路径选择按钮
        self.target_path_button = tk.Button(self.compare_xml_root, text='浏览目标xml路径')
        self.target_path_button_disable = tk.Button(self.compare_xml_root, text='浏览目标xml路径')
        self.target_path_button_disable.config(state='disabled')
        self.target_path_button.place(x=360, y=105)
        self.target_path_button.bind('<Button-1>', lambda x:threading.Thread(target=self.open_compare_path).start())

        # 创建点击xml比较按钮
        self.compare_button = tk.Button(self.compare_xml_root, text='Xml文件比较', width=10)
        self.compare_button_disable = tk.Button(self.compare_xml_root, text='Xml文件比较', width=10)
        self.compare_button_disable.config(state='disabled')
        self.compare_button.place(x=200, y=150)
        self.compare_button.bind('<Button-1>', lambda x: threading.Thread(target=self.compare_xml).start())

        # 显示合并日志信息框
        self.compare_log_text = tk.Text(self.compare_xml_root, width=60, height=13)
        self.compare_log_text.place(x=20, y=200)
        # 设置只读
        self.compare_log_text.config(state='disabled')

        # 创建滚动条
        self.compare_log_scroll = tk.Scrollbar(self.compare_xml_root)
        self.compare_log_scroll.place(x=445, y=195, height=180)
        # 绑定滚动条
        self.compare_log_scroll.config(command=self.compare_log_text.yview)
        self.compare_log_text.config(yscrollcommand=self.compare_log_scroll.set)
        # 创建横向滚动条
        self.compare_log_scroll_x = tk.Scrollbar(self.compare_xml_root, orient=tk.HORIZONTAL)
        self.compare_log_scroll_x.place(x=20, y=370, width=425)
        # 绑定横向滚动条
        self.compare_log_scroll_x.config(command=self.compare_log_text.xview)
        self.compare_log_text.config(xscrollcommand=self.compare_log_scroll_x.set)

    def open_compare_xml_path(self):
        # 打开多国语言xml文件路径，过滤出xml文件
        self.compare_xml_button.place_forget()
        self.compare_xml_button_disable.place(x=360, y=35)
        self.compare_xml_root.attributes("-topmost", False)
        self.compare_xml_path = filedialog.askopenfilename(title='选择多国语言xml文件', filetypes=[('xml文件', '*.xml')])
        # 先清空输入框
        self.compare_xml_entry.delete(0, tk.END)
        self.compare_xml_entry.insert(0, self.compare_xml_path)

        # 保存多国语言xml文件路径
        with open(compare_xml_file_path, 'w', encoding='utf-8') as f:
            f.write(self.compare_xml_path)
        self.compare_xml_root.attributes("-topmost", True)
        self.compare_xml_button_disable.place_forget()
        self.compare_xml_button.place(x=360, y=35)

    def open_compare_path(self):
        # 打开目标xml文件路径
        self.target_path_button.place_forget()
        self.target_path_button_disable.place(x=360, y=105)
        self.compare_xml_root.attributes("-topmost", False)
        self.target_path = filedialog.askopenfilename(title='选择项目路径',filetypes=[('xml文件', '*.xml')])
        # 先清空输入框
        self.target_path_entry.delete(0, tk.END)
        self.target_path_entry.insert(0, self.target_path)


        # 保存项目路径
        with open(compare_file_path, 'w', encoding='utf-8') as f:
            f.write(self.target_path)
        self.compare_xml_root.attributes("-topmost", True)
        self.target_path_button_disable.place_forget()
        self.target_path_button.place(x=360, y=105)

    def compare_xml(self):
        # 比较xml文件
        self.compare_button.place_forget()
        self.compare_button_disable.place(x=200, y=150)

        if not os.path.exists(self.compare_xml_entry.get()) or not os.path.exists(self.target_path_entry.get()):
            self.compare_log_text.config(state='normal')
            self.compare_log_text.insert(tk.END, '请检查多国语言xml文件路径或目标xml文件路径是否正确！\n')
            self.compare_log_text.config(state='disabled')
            self.compare_log_text.see(tk.END)
        else:
            # 日志信息清空
            self.compare_log_text.config(state='normal')
            self.compare_log_text.delete(1.0, tk.END)

            # 获取多国语言xml文件路径
            self.compare_xml_file_path = self.compare_xml_entry.get()
            # 获取目标xml文件路径
            self.target_xml_file_path = self.target_path_entry.get()
            # 执行比较逻辑
            self.compare_log_text.config(state='normal')
            self.compare_log_text.insert(tk.END,'开始比较xml文件，请稍等...\n')
            self.compare_log_text.config(state='disabled')
            compare_xml(self.compare_xml_file_path, self.target_xml_file_path, self.compare_log_text)
            self.compare_log_text.see(tk.END)

        self.compare_button_disable.place_forget()
        self.compare_button.place(x=200, y=150)



