#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import threading
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import extra_functions.template_function as template_function
from xml_merge_demo.xml_merge import MergeXml
from xml_merge_demo.xml_compare import CompareXml
from extra_functions.single_xml_translate import SingleXmlTranslate
from extra_functions import module_illustrate
from Settings import Setting
import extra_functions.zhoufei_tools as zhoufei_tools
import youdao_translate
import pyperclip,os,sys
from my_thread import MyThread
import win32con, win32api
trans_main = youdao_translate.TranslateMain()  # 实例化翻译主类


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = os.path.join(sys._MEIPASS,r'YouDao_XML_Translate\xml_translate_tool')  # pylint: disable=no-member
    else:
        base_path = os.path.abspath('.')
    print('资源当前路径：',base_path)
    return os.path.join(base_path, relative_path)   # 拼接资源文件路径


# 获取Windows文档路径
doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'  # 工具临时文件路径
trans_file_path = trans_file + 'trans_file_dir'  # 翻译文件临时路径
trans_log_path = trans_file + 'trans_log'  # 翻译工具日志存储
trans_log_file_path = trans_log_path + '\\trans_path.log'  # 记录翻译文件路径
youdao_id_key_path = trans_file + '\\youdao_id_key.log'  # 记录有道翻译ID和KEY
version_file_path = resource_path(os.path.join('version', 'version_zh_CN.txt'))  # 版本文件路径
tools_ico = resource_path(os.path.join('icon', 'my-da.ico'))  # 工具图标路径
version = '1.1.3'  # 版本号

if not os.path.exists(trans_file_path):
    os.makedirs(trans_file_path)
elif not os.path.exists(trans_log_path):
    os.makedirs(trans_log_path)

# ListBox各项递归初始数据
label_offsety = 370
trans_label_offsety = 365
listbox_offsety = 400
# 暂停恢复标识
stop_event_flag = False


class Context:
    pass  # 用于存储全局变量


def pyperclip_copy_paste(button_id,content):
    print(f'获取当前点击的语言{button_id} button')
    if content.strip() == '':
        tk.messagebox.showinfo('粘贴失败', '粘贴内容为空！！！')
    else:
        # 通用复制粘贴
        pyperclip.copy(content)
        # 从剪贴板那粘贴
        pyperclip.paste()
        tk.messagebox.showinfo('粘贴提醒','已复制粘贴！！！\n温馨提示：可以Ctrl+V粘贴到任意地方啦~')


class MainForm(object):
    def root_form(self):
        self.root = tk.Tk()
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        w = 500
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(0, 0)
        self.root.title(f'批量翻译xml文本 - 有道翻译 {version} windows版')  # 设置窗口标题
        self.root.iconbitmap(tools_ico)  # 设置图标
        # s.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        # s.root.overrideredirect(1)  # 隐藏标题栏 最大化最小化按钮
        # s.root.config(bg=bg)
        # 软件始终置顶
        # s.root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        self.root.protocol('WM_DELETE_WINDOW', self.close_handle)  # 退出程序需要处理或结束任务

        self.main_form()
        self.get_id_key()
        self.root.mainloop()

    def get_id_key(self):
        # 获取有道翻译的id和key
        if not os.path.exists(youdao_id_key_path):
            with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
                f.write('Your_Id=\nYour_Key=')
        # 隐藏文件
        win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_HIDDEN)

        # 读取有道翻译的id和key
        with open(youdao_id_key_path, 'r', encoding='utf-8') as f:
            id_key = f.readlines()
            if not id_key:
                with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
                    f.write('Your_Id=\nYour_Key=')
            you_id = id_key[0].split('=')[1].strip()
            you_key = id_key[1].split('=')[1].strip()
            f.close()
        if you_id == '' or you_key == '':
            # 先隐藏主窗口
            self.root.withdraw()

            # 有道翻译ID或KEY为空时，弹出窗口输入
            self.id_key_root = tk.Toplevel()
            self.id_key_root.title('有道翻译ID和KEY')
            screenWidth = self.root.winfo_screenwidth()
            screenHeight = self.root.winfo_screenheight()
            w = 350
            h = 350
            x = (screenWidth - w) / 2
            y = (screenHeight - h) / 2
            self.id_key_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            self.id_key_root.resizable(0, 0)
            self.id_key_root.iconbitmap(tools_ico)  # 设置图标
            self.id_key_root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
            self.id_key_root.wm_attributes('-topmost', 1)  # 窗口置顶

            # id输入框
            tk.Label(self.id_key_root, text='有道翻译ID：').place(x=10, y=10)
            self.you_id = tk.Entry(self.id_key_root, width=30)
            self.you_id.place(x=100, y=10)

            # key输入框
            tk.Label(self.id_key_root, text='有道翻译KEY：').place(x=10, y=50)
            self.you_key = tk.Entry(self.id_key_root, width=30)
            self.you_key.place(x=100, y=50)

            # 状态显示label
            self.id_key_status_str = tk.StringVar()
            self.id_key_status = tk.Label(self.id_key_root, textvariable=self.id_key_status_str, fg='red')
            self.id_key_status.place(x=100, y=75)
            self.id_key_status_str.set('有道翻译ID和KEY目前为空，需要填写！')

            # 保存按钮
            self.save_button = tk.Button(self.id_key_root, text='保存', width=10)
            self.save_button_disable = tk.Button(self.id_key_root, text='保存', width=10)
            self.save_button_disable.config(state='disabled')
            self.save_button.place(x=50, y=100)
            self.save_button.bind('<Button-1>', lambda x:threading.Thread(target=self.save_id_key).start())

            # 关闭按钮
            self.close_button = tk.Button(self.id_key_root, text='关闭', width=10)
            self.close_button_disable = tk.Button(self.id_key_root, text='关闭', width=10)
            self.close_button_disable.config(state='disabled')
            self.close_button.place(x=150, y=100)
            self.close_button.bind('<Button-1>', lambda x:self.second_id_key_close())

            # lj体验按钮
            self.lj_button = tk.Button(self.id_key_root, text='体验', width=10)
            self.lj_button_disable = tk.Button(self.id_key_root, text='体验', width=10)
            self.lj_button_disable.config(state='disabled')
            self.lj_button.place(x=250, y=100)
            self.lj_button.bind('<Button-1>',lambda x: threading.Thread(target=self.experience).start())

            # 内容显示label
            self.id_key_content_str = tk.StringVar()
            self.id_key_content = tk.Label(self.id_key_root, textvariable=self.id_key_content_str, fg='blue',wraplength=300,justify='left')
            self.id_key_content.place(x=10, y=130)
            id_key_content = "\t\t      说明：\n1.有道翻译ID和KEY需要自己去有道翻译官网申请，申请地址：http://ai.youdao.com/" \
                             "\n2.申请后，将ID和KEY填入上面的输入框中，然后点击保存按钮" \
                             "\n3.本工具目前仅支持有道翻译，不想使用点击关闭按钮关闭即可，但无法使用该工具" \
                             "\n4.如果已有申请的ID和KEY，输入后直接点击保存按钮正常使用" \
                             "\n5.如没有申请ID和KEY但想体验，点击“体验”按钮即可使用，注：该体验ID和KEY有体验金额度限制，超过后无法使用，由罗靖提供"
            self.id_key_content_str.set(id_key_content)

            self.id_key_root.protocol('WM_DELETE_WINDOW', self.id_key_close)

    def second_id_key_close(self):
        def t_second_id_key_close():
            self.close_button.place_forget()
            self.close_button_disable.place(x=150, y=100)
            with open(youdao_id_key_path, 'r', encoding='utf-8') as f:
                id_key = f.readlines()
                you_id_1 = id_key[0].split('=')[1].strip()
                you_key_1 = id_key[1].split('=')[1].strip()
                f.close()
            if not you_id_1 == '' or you_key_1 == '':
                self.id_key_root.wm_attributes('-topmost', 0)
                if tkinter.messagebox.askyesno('关闭提示','确定不保存有道翻译ID和KEY吗？\n不保存将无法正常使用有道翻译！\n下次将再次提示！'):
                    self.id_key_root.destroy()
                    self.root.destroy()
                    # 退出程序
                    sys.exit()
            else:
                self.id_key_root.destroy()
                self.root.deiconify()  # 显示主窗口

            self.close_button_disable.place_forget()
            self.close_button.place(x=150, y=100)

        t_second_id_key_close = threading.Thread(target=t_second_id_key_close)
        t_second_id_key_close.setDaemon(True)  # 设置为守护线程，主线程结束，子线程也结束
        t_second_id_key_close.start()

    def id_key_close(self):
        # 关闭有道翻译ID和KEY窗口
        you_id = self.you_id.get().strip()
        you_key = self.you_key.get().strip()
        if you_id == '' or you_key == '':
            self.id_key_root.wm_attributes('-topmost', 0)
            tkinter.messagebox.showinfo('提示', '有道翻译ID和KEY不能为空！\n否则无法正常使用有道翻译！')
            self.id_key_root.wm_attributes('-topmost', 1)
        else:
            self.id_key_root.destroy()
            self.root.deiconify()  # 显示主窗口

    def save_id_key(self):
        # 保存有道翻译的id和key
        self.save_button.place_forget()
        self.save_button_disable.place(x=50, y=100)
        you_id = self.you_id.get().strip()
        you_key = self.you_key.get().strip()
        if you_id == '' or you_key == '':
            self.id_key_status_str.set('有道翻译ID或KEY不能为空！')
        else:
            # 显示文件
            win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_NORMAL)

            # 写进文件
            with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
                f.write(f'Your_Id={you_id}\nYour_Key={you_key}')

            # 再次隐藏文件
            win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_HIDDEN)

            self.id_key_root.wm_attributes('-topmost', 0)
            tkinter.messagebox.showinfo('提示', '保存成功！\n现在您可以继续使用有道翻译了！')
            self.id_key_root.wm_attributes('-topmost', 1)

            # 关闭有道翻译ID和KEY窗口
            self.id_key_close()

        try:
            self.save_button_disable.place_forget()
            self.save_button.place(x=50, y=100)
        except Exception:
            pass

    def experience(self):
        # 体验有道翻译
        self.lj_button.place_forget()
        self.lj_button_disable.place(x=250, y=100)
        self.id_key_root.wm_attributes('-topmost', 0)
        if tkinter.messagebox.askokcancel('是否体验','是否免费体验本工具？\n注：该体验账号体验金有限，请勿过度使用，否则无法体验'):
            experience_id = '1a2fc055f4f9d8dc'
            experience_key = 'jznSJaGFw7PiglQ57rWCpY4ZhMlsPdBn'

            win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_NORMAL)
            with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
                f.write(f'Your_Id={experience_id}\nYour_Key={experience_key}')
            win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_HIDDEN)
            self.id_key_root.destroy()
            self.root.deiconify()  # 显示主窗口
        try:
            self.id_key_root.wm_attributes('-topmost', 1)
            self.lj_button_disable.place_forget()
            self.lj_button.place(x=250, y=100)
        except Exception:
            pass

    def close_handle(self):
        # 退出程序需要处理或结束任务
        try:
            shutil.rmtree(trans_file_path)  # 删除临时文件夹
        except Exception:
            pass
        self.root.destroy()
        # 结束该工具所有程序
        sys.exit()

    def generate_display_listbox(self,component,trans_lang,label_y,offset_y,listbox_offset_y):
        # 生成显示翻译的listbox并配置滚动条
        tk.Label(component, text='').grid(row=2, column=0, padx=0, pady=label_offsety + label_y)  # 占位
        tk.Label(component, text=f'下面翻译的语言是 {trans_lang}', fg='red').place(x=10, y=trans_label_offsety + offset_y)

        # copy按钮
        self.copy_button_lang = tk.Button(component, text='复制', width=10)
        self.copy_button_lang_disable = tk.Button(component, text='复制', width=10)
        self.copy_button_lang.place(x=300, y=trans_label_offsety + offset_y)
        self.copy_button_lang.config(command= lambda x=trans_lang,y=offset_y:self.copy_button_bind(x,y))  # 绑定按钮不同事件
        self.copy_button_lang_disable.config(state='disabled')

        # listbox
        self.display_listbox_scrollbar = tk.Scrollbar(component)
        self.display_listbox = tk.Listbox(component, width=52, height=10)
        self.display_listbox.bindtags((self.display_listbox, component, "all"))  # 禁止用户选中和修改listbox内容
        self.display_listbox.place(x=12, y=listbox_offsety + listbox_offset_y)
        self.display_listbox_scrollbar.place(x=380, y=listbox_offsety + offset_y, height=180)
        self.display_listbox.config(yscrollcommand=self.display_listbox_scrollbar.set)
        self.display_listbox_scrollbar.config(command=self.display_listbox.yview)

        # 创建横向的滚动条绑定listbox
        # tk.HORIZONTAL 水平滚动条 orient 滚动条方向
        self.display_listbox_scrollbar_x = tk.Scrollbar(component, orient=tk.HORIZONTAL)
        self.display_listbox_scrollbar_x.place(x=12, y=listbox_offsety + listbox_offset_y + 180, width=368)
        self.display_listbox.config(xscrollcommand=self.display_listbox_scrollbar_x.set)
        self.display_listbox_scrollbar_x.config(command=self.display_listbox.xview)

    def main_form(self):
        # 主窗口（超出范围会滚动）
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.component = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.component, anchor='nw')  # 创建组件

        # 创建说明文本Label
        tk.Label(self.component, text='翻译文件夹路径：').place(x=10, y=10)

        # 创建res翻译文件夹输入框 padx pady 为控件与控件之间的距离
        self.res_path = tk.StringVar()
        self.res_path_entry = tk.Entry(self.component, textvariable=self.res_path, width=40)
        self.res_path_entry.grid(row=0, column=1, padx=10, pady=40)
        if not os.path.exists(trans_log_file_path):
            with open(trans_log_file_path,'w') as f:
                f.write('')
        with open(trans_log_file_path, 'r') as f:
            res_path = f.read()
            self.res_path.set(res_path)

        # 点击浏览文件夹按钮
        self.browse_button = tk.Button(self.component, text='浏览',width=5)
        self.browse_button.grid(row=0, column=2,padx=10)
        self.browse_button.bind('<Button-1>', lambda x:self.browse_button_bind())

        # 创建翻译语言Label
        tk.Label(self.component, text='温馨提示：如果不清楚翻译文件夹，则点击右侧的“模板”按钮创建模板！',fg='red').place(x=10, y=70)
        tk.Label(self.component, text='').grid(row=1, column=0, padx=10, pady=10)  # 占位

        # 创建输入需要翻译的文本的Label
        tk.Label(self.component, text='下面输入要翻译的文本xml格式：（可在前面添加注释，注释不翻译）',fg='red').place(x=10, y=90)
        tk.Label(self.component, text='').grid(row=2, column=0, padx=10, pady=110)  # 占位

        # 创建输入需要翻译的文本的输入文本框，并绑定滚动条
        self.input_text = tk.Text(self.component, width=52, height=15)
        self.input_text.place(x=12, y=110)
        self.input_text_scrollbar = tk.Scrollbar(self.component)
        self.input_text_scrollbar.place(x=380, y=110, height=200)
        self.input_text.config(yscrollcommand=self.input_text_scrollbar.set)
        self.input_text_scrollbar.config(command=self.input_text.yview)

        # 翻译按钮
        self.trans_button = tk.Button(self.component, text='点击翻译', width=10)
        self.trans_button_disable = tk.Button(self.component, text='正在翻译中...', width=10)
        self.trans_button_disable.config(state='disabled')
        self.trans_button.place(x=30, y=320)
        self.trans_button.bind('<Button-1>', lambda x:self.start_trans_bind())

        # 停止翻译按钮
        self.stop_trans_button = tk.Button(self.component, text='停止翻译', width=10)
        self.stop_trans_button_disable = tk.Button(self.component, text='停止翻译', width=10)
        self.stop_trans_button_disable.config(state='disabled')
        self.stop_trans_button_disable.place(x=150, y=320)
        self.stop_trans_button.bind('<Button-1>',lambda x:self.stop_trans_bind())

        # 恢复暂停按钮
        self.stop_resume_button = tk.Button(self.component, text='暂停翻译', width=10)
        self.stop_resume_button_disable = tk.Button(self.component, text='暂停翻译', width=10)
        self.resume_button = tk.Button(self.component, text='恢复翻译', width=10)
        self.stop_resume_button_disable.config(state='disabled')
        self.stop_resume_button_disable.place(x=270, y=320)
        self.stop_resume_button.bind('<Button-1>', lambda x:self.stop_resume_bind())
        self.resume_button.bind('<Button-1>', lambda x:self.resume_bind())

        # 关于按钮，不随着滚动条滚动
        self.about_button = tk.Button(self.root, text='关于', width=10)
        self.about_button_disable = tk.Button(self.root, text='关于', width=10)
        self.about_button_disable.config(state='disabled')
        self.about_button.place(x=400, y=10)
        self.about_button.bind('<Button-1>', lambda x:self.about_version())

        # 模块说明按钮
        self.module_button = tk.Button(self.root, text='模块说明', width=10)
        self.module_button_disable = tk.Button(self.root, text='模块说明', width=10)
        self.module_button_disable.config(state='disabled')
        self.module_button.place(x=400, y=50)
        self.module_button.bind('<Button-1>', lambda x:threading.Thread(target=module_illustrate.ModuleIllustration().root_form,args=(self.module_button,self.module_button_disable)).start())

        # 创建模板按钮
        self.template_button = tk.Button(self.root, text='模板', width=10)
        self.template_button_disable = tk.Button(self.root, text='模板', width=10)
        self.template_button_disable.config(state='disabled')
        self.template_button.place(x=400, y=90)
        self.template_button.bind('<Button-1>', lambda x:threading.Thread(target=template_function.template_prompt,args=(self.template_button,self.template_button_disable)).start())

        # 创建单个xml文件翻译按钮
        self.single_xml_button = tk.Button(self.root, text='单个xml翻译', width=10)
        self.single_xml_button_disable = tk.Button(self.root, text='单个xml翻译', width=10)
        self.single_xml_button_disable.config(state='disabled')
        self.single_xml_button.place(x=400, y=130)
        self.single_xml_button.bind('<Button-1>', lambda x:threading.Thread(target=SingleXmlTranslate().root_form,args=(self.single_xml_button,self.single_xml_button_disable)).start())

        # 创建多国语言xml（第三方翻译）合并原文件组合成新string.xml文件（最终使用新文件）按钮
        self.merge_xml_button = tk.Button(self.root, text='xml文件合并', width=10)
        self.merge_xml_button_disable = tk.Button(self.root, text='xml文件合并', width=10)
        self.merge_xml_button_disable.config(state='disabled')
        self.merge_xml_button.place(x=400, y=170)
        self.merge_xml_button.bind('<Button-1>', lambda x:threading.Thread(target=MergeXml().root_form,args=(self.merge_xml_button,self.merge_xml_button_disable)).start())

        # 创建多国语言xml（第三方翻译）与单个xml文件比较最终生成或替换新string.xml文件（最终使用新文件）按钮
        self.compare_xml_button = tk.Button(self.root, text='xml文件比较', width=10)
        self.compare_xml_button_disable = tk.Button(self.root, text='xml文件比较', width=10)
        self.compare_xml_button_disable.config(state='disabled')
        self.compare_xml_button.place(x=400, y=210)
        self.compare_xml_button.bind('<Button-1>', lambda x:threading.Thread(target=CompareXml().root_form,args=(self.compare_xml_button,self.compare_xml_button_disable)).start())

        # 创建周飞工具集合按钮
        self.zhoufei_button = tk.Button(self.root, text='周飞工具', width=10)
        self.zhoufei_button_disable = tk.Button(self.root, text='周飞工具', width=10)
        self.zhoufei_button_disable.config(state='disabled')
        self.zhoufei_button.place(x=400, y=250)
        self.zhoufei_button.bind('<Button-1>', lambda x:threading.Thread(target=zhoufei_tools.ZFTools().root_form,args=(self.zhoufei_button,self.zhoufei_button_disable)).start())

        # 设置按钮
        self.setting_button = tk.Button(self.root, text='设置', width=10)
        self.setting_button_disable = tk.Button(self.root, text='设置', width=10)
        self.setting_button_disable.config(state='disabled')
        self.setting_button.place(x=400, y=290)
        self.setting_button.bind('<Button-1>', lambda x:threading.Thread(target=Setting().root_form,args=(self.setting_button,self.setting_button_disable)).start())

        def on_configure(event):  # 重置滚动区域
            self.canvas.update_idletasks()  # 更新组件
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

            # 重置滚动条位置，首先销毁已有或者不可见的滚动条，然后重新创建，保证滚动条一直可见
            try:
                self.input_text_scrollbar.place_forget()
            except Exception as e:
                print(e)
            self.input_text_scrollbar = tk.Scrollbar(self.component)
            self.input_text_scrollbar.place(x=380, y=110, height=200)
            self.input_text.config(yscrollcommand=self.input_text_scrollbar.set)
            self.input_text_scrollbar.config(command=self.input_text.yview)

        self.component.bind('<Configure>', on_configure)  # 绑定组件大小变化事件

    def about_version(self):
        # 关于版本
        # 新建窗口
        about_version = tk.Toplevel(self.root)
        about_version.title('关于版本')
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        w = 500
        h = 230
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        about_version.wm_attributes('-topmost', 1)  # 置顶
        about_version.geometry('%dx%d+%d+%d' % (w, h, x, y))  # 设置窗口大小和位置
        about_version.resizable(0, 0)  # 禁止调整窗口大小
        about_version.iconbitmap(tools_ico)

        self.about_button.place_forget()
        self.about_button_disable.place(x=400, y=10)

        # 新建listbox并配置滚动条到底部
        about_listbox = tk.Listbox(about_version, width=65, height=10)
        about_listbox.place(x=10, y=10)
        # 滚动条
        about_listbox_scrollbar = tk.Scrollbar(about_version)
        about_listbox_scrollbar.place(x=460, y=10, height=180)
        about_listbox.config(yscrollcommand=about_listbox_scrollbar.set)
        about_listbox_scrollbar.config(command=about_listbox.yview)
        # 添加横向滚动条
        about_listbox_scrollbar_x = tk.Scrollbar(about_version, orient=tk.HORIZONTAL)
        about_listbox_scrollbar_x.place(x=10, y=190, width=450)
        about_listbox.config(xscrollcommand=about_listbox_scrollbar_x.set)
        about_listbox_scrollbar_x.config(command=about_listbox.xview)

        # 读取关于文件
        with open(version_file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                about_listbox.insert(tk.END, line)

        # 关闭窗口执行的函数
        about_version.protocol('WM_DELETE_WINDOW', lambda : close_about_version())

        # 关闭窗口
        def close_about_version():
            self.about_button_disable.place_forget()
            self.about_button.place(x=400, y=10)
            about_version.destroy()

    def trans_bind(self,stop_event):
        # 翻译按钮绑定事件
        global stop_event_flag
        stop_event_flag = False

        self.trans_button.place_forget()
        self.trans_button_disable.place(x=30, y=320)
        self.stop_trans_button_disable.place_forget()
        self.stop_trans_button.place(x=150, y=320)
        self.stop_resume_button_disable.place_forget()
        self.stop_resume_button.place(x=270, y=320)

        # 存储res文件夹路径
        with open(trans_log_file_path,'w') as f:
            f.write(self.res_path.get())

        # 输入路径为空或者路径不存在或者路径下没有values文件夹或者values文件夹下没有strings.xml文件
        if self.res_path.get() == '':
            tk.messagebox.showerror('错误','文件夹路径不能为空')
        elif not os.path.exists(self.res_path.get()):
            tk.messagebox.showerror('错误', '文件夹路径不存在')
        elif not os.path.exists(self.res_path.get() + '/values'):
            tk.messagebox.showerror('错误', '路径下没有values文件夹')
        elif not os.path.exists(self.res_path.get() + '/values/strings.xml'):
            tk.messagebox.showerror('错误', 'values文件夹下没有strings.xml文件')
        else:
            # 删除临时文件夹
            shutil.rmtree(trans_file_path)
            # 创建临时文件夹
            os.makedirs(trans_file_path)

            # 销毁所有listbox
            for widget in self.component.winfo_children():  # 遍历组件
                if widget.winfo_class() == 'Listbox':
                    widget.destroy()

            # 销毁所有self.copy_button_lang
            for widget in self.component.winfo_children():  # 遍历组件
                if widget.winfo_class() == 'Button' and widget['text'] == '复制':
                    widget.destroy()

            # 销毁所有开头是“下面翻译的语言是”的label
            for widget in self.component.winfo_children():  # 遍历组件
                if widget.winfo_class() == 'Label' and widget['text'].startswith('下面翻译的语言是'):
                    widget.destroy()

            # 销毁关于批量翻译的self.display_listbox_scrollbar滚动条
            for widget in self.component.winfo_children():  # 遍历组件
                if widget.winfo_class() == 'Scrollbar':
                    widget.destroy()

            trans_lang_list = youdao_translate.get_trans_lang(self.res_path.get())

            if not trans_lang_list:
                tk.messagebox.showerror('错误', 'values文件夹下没有可翻译的文件夹')
            else:
                label_y = 0
                offset_y = 0
                listbox_offset_y = 0

                # 获取输入文本框input_text
                input_text = self.input_text.get('0.0', tk.END).strip()

                self.trans_lock = threading.Lock()  # 翻译锁
                setattr(youdao_translate.Context,'stop_event_flag',stop_event_flag)  # 设置停止翻译标志位 - 反射机制

                for trans_lang in trans_lang_list:
                    if stop_event.is_set():  # 停止接下来的所有翻译
                        print("Stopping all thread...")
                        return

                    # 生成显示翻译的listbox并配置滚动条
                    self.generate_display_listbox(self.component,trans_lang,label_y, offset_y,listbox_offset_y)

                    # 获取当前画布滚动条的高度
                    canvas_scrollregion = self.canvas['scrollregion']  # 获取画布的滚动范围
                    canvas_scrollregion_list = canvas_scrollregion.split(' ')  # 将画布的滚动范围转换为list
                    canvas_scrollregion_height = int(canvas_scrollregion_list[3])  # 获取画布的滚动范围的高度
                    # print('canvas_scrollregion_height',canvas_scrollregion_height)
                    # 获取当前复制按钮的y坐标
                    listbox_1 = self.copy_button_lang.winfo_y()
                    # print('listbox_1',listbox_1)
                    # 计算滚动条的偏移量
                    offset_y_1 = listbox_1 / canvas_scrollregion_height
                    # print('offset_y',offset_y_1)
                    # 设置滚动条的偏移量，使滚动条移动到当前复制按钮的位置（介于0和1之间）
                    self.canvas.yview_moveto(offset_y_1)

                    self.display_listbox.insert(tk.END, f'正在翻译的是 {trans_lang}')
                    try:
                        trans_main.translate_params(trans_lang,self.res_path.get(),self.display_listbox,stop_event,self.trans_lock,input_text)
                    except Exception as e:
                        print('Exception:',e)
                        self.display_listbox.insert(tk.END, '翻译出错，请检查有道翻译接口ID和KEY是否正确可用！！！')
                        self.display_listbox.insert(tk.END, '否则无法正常使用翻译！！！')
                        break

                    # 创建不存在的文件
                    if not os.path.exists(trans_file_path + '\\' + trans_lang + '.txt'):
                        with open(trans_file_path + '\\' + trans_lang + '.txt', 'w', encoding='utf-8') as f:
                            f.write('')

                    if stop_event.is_set():
                        self.display_listbox.insert(tk.END, '翻译已停止')
                    else:
                        with open(trans_file_path + '\\' + trans_lang + '.txt', 'r', encoding='utf-8') as f:
                            if f.read() == '':
                                self.display_listbox.insert(tk.END, '该语言已全部翻译完成，无需翻译！！！')
                            else:
                                self.display_listbox.insert(tk.END, '翻译完成')
                    self.display_listbox.see(tk.END)

                    # 计算下一个listbox的位置，如果出现组件显示不全的情况，可以修改这里的值（例如修改需要同时修改三个值，且增加减少的数值需要一致）
                    label_y += 125
                    offset_y += 255
                    listbox_offset_y += 255

        self.trans_button_disable.place_forget()
        self.trans_button.place(x=30, y=320)
        self.stop_trans_button.place_forget()
        self.stop_trans_button_disable.place(x=150, y=320)
        self.stop_resume_button.place_forget()
        self.stop_resume_button_disable.place(x=270, y=320)
        self.resume_button.place_forget()

    def copy_button_bind(self,trans_lang,offset_y):
        # 复制按钮绑定事件
        self.copy_button_lang.place_forget()
        self.copy_button_lang_disable.place(x=300, y=trans_label_offsety + offset_y)

        # 获取复制的文本
        if trans_lang == 'zh-rTW':  # 修改繁体中文的文件名
            trans_lang = 'zh-CHT'
        if trans_lang == 'ar-rAE':  # 阿拉伯语修改为有道翻译支持的阿拉伯语言
            trans_lang = 'ar'

        # 创建不存在的文件
        if not os.path.exists(trans_file_path + '\\' + trans_lang + '.txt'):
            with open(trans_file_path + '\\' + trans_lang + '.txt', 'w', encoding='utf-8') as f:
                f.write('')

        with open(trans_file_path + '\\' + trans_lang + '.txt', 'r', encoding='utf-8') as f:
            copy_text = f.read()
            print('复制的文本是：', copy_text)
            pyperclip_copy_paste(trans_lang,copy_text)

        self.copy_button_lang_disable.place_forget()
        self.copy_button_lang.place(x=300, y=trans_label_offsety + offset_y)

    def start_trans_bind(self):
        # 启动翻译按钮线程
        trans_thread = MyThread(self.trans_bind)  # 创建线程
        self.trans_thread = trans_thread
        self.trans_thread.start()  # 启动线程

    def stop_trans_bind(self):
        def t_stop_trans():
            # 停止翻译按钮绑定事件
            if tk.messagebox.askyesno('停止提示','正在翻译中，是否需要停止翻译？'):
                self.trans_thread.stop()

                try:
                    self.trans_lock.release()
                except Exception:
                    pass

                # 恢复按钮状态
                self.trans_button_disable.place_forget()
                self.trans_button.place(x=30, y=320)
                self.stop_trans_button.place_forget()
                self.stop_trans_button_disable.place(x=150, y=320)
                self.stop_resume_button.place_forget()
                self.stop_resume_button_disable.place(x=270, y=320)
                self.resume_button.place_forget()

        t_stop_trans = threading.Thread(target=t_stop_trans)
        t_stop_trans.setDaemon(True)
        t_stop_trans.start()

    def stop_resume_bind(self):
        def t_stop_resume():
            # 暂停翻译
            if tk.messagebox.askyesno('暂停提示', '正在翻译中，是否需要暂停翻译？'):
                global stop_event_flag
                stop_event_flag = True
                setattr(youdao_translate.Context, 'stop_event_flag', stop_event_flag)
                self.stop_resume_button.place_forget()
                self.resume_button.place(x=270, y=320)
                self.display_listbox.insert(tk.END, '已暂停翻译...')

        t_stop_resume = threading.Thread(target=t_stop_resume)
        t_stop_resume.setDaemon(True)
        t_stop_resume.start()

    def resume_bind(self):
        def t_resume():
            # 恢复翻译
            global stop_event_flag
            stop_event_flag = False
            setattr(youdao_translate.Context, 'stop_event_flag', stop_event_flag)
            self.trans_lock.release()  # 释放锁
            self.resume_button.place_forget()
            self.stop_resume_button.place(x=270, y=320)
            self.display_listbox.insert(tk.END, '已恢复翻译...')

        t_resume = threading.Thread(target=t_resume)
        t_resume.setDaemon(True)
        t_resume.start()

    def browse_button_bind(self):
        # 选择文件夹按钮绑定事件
        def t_browse_dir():
            # 禁用浏览按钮
            self.browse_button.config(state=tk.DISABLED)

            # 清空文本框
            self.res_path_entry.delete(0, tk.END)
            # 选择文件夹
            res_dir_path = filedialog.askdirectory()
            self.res_path.set(res_dir_path)
            # 记录结果到文件
            with open(trans_log_file_path, 'w', encoding='utf-8') as f:
                f.write(self.res_path.get())

            # 启用浏览按钮
            self.browse_button.config(state=tk.NORMAL)

        t_browse_dir = threading.Thread(target=t_browse_dir)
        t_browse_dir.setDaemon(True)
        t_browse_dir.start()


if __name__ == '__main__':
    MainForm().root_form()  # 主窗口

