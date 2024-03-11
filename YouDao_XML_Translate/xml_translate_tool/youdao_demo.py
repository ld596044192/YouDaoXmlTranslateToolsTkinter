#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 有道翻译demo
import os.path
import re
import sys
import uuid
from xml.etree.ElementTree import Element
import win32api,win32con
import tkinter as tk
import requests
import hashlib
import time,getpass
from imp import reload
from xml.etree import ElementTree as ElementTree

# 有道翻译api对接地址：
# https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html

doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file = doc_path + '\\xml_youdao_tool\\'
trans_file_path = trans_file + 'trans_file_dir'
if not os.path.exists(trans_file_path):
    os.makedirs(trans_file_path)


def youdao_id_key_all():
    # 获取有道翻译ID和KEY
    youdao_id_key_path = trans_file + '\\youdao_id_key.log'  # 记录有道翻译ID和KEY的文件路径
    YOUDAO_URL = 'https://openapi.youdao.com/api'  # 有道翻译的接口地址
    if not os.path.exists(youdao_id_key_path):
        with open(youdao_id_key_path, 'w', encoding='utf-8') as f:
            f.write('Your_Id=\nYour_Key=')
        # 隐藏文件
        win32api.SetFileAttributes(youdao_id_key_path, win32con.FILE_ATTRIBUTE_HIDDEN)
    with open(youdao_id_key_path, 'r', encoding='utf-8') as f:
        youdao_id_key = f.readlines()
        APP_KEY = youdao_id_key[0].split('=')[1].strip()  # 应用ID
        APP_SECRET = youdao_id_key[1].split('=')[1].strip()  # 应用密钥
    return [YOUDAO_URL, APP_KEY, APP_SECRET]


# def indent(elem, level=0):
#     # 用于格式化xml文件  但是此时的xml文件和我们平时常见的格式不太一样，如何转变成标准的格式呢？ 思路就是在每个节点之后添加"\n\t"
#     i = "\n" + level*"\t"  # 换行符+缩进符
#     if len(elem):  # 如果elem有子元素
#         if not elem.text or not elem.text.strip():  # 如果elem.text为空或者elem.text只包含空格
#             elem.text = i + "\t"  # 将elem.text设置为换行符+缩进符+缩进符
#         if not elem.tail or not elem.tail.strip():  # 如果elem.tail为空或者elem.tail只包含空格
#             elem.tail = i  # 将elem.tail设置为换行符+缩进符
#         for elem in elem:  # 遍历elem的子元素
#             indent(elem, level+1)  # 递归调用indent函数
#         if not elem.tail or not elem.tail.strip():  # 如果elem.tail为空或者elem.tail只包含空格
#             elem.tail = i  # 将elem.tail设置为换行符+缩进符
#     else:  # 如果elem没有子元素
#         if level and (not elem.tail or not elem.tail.strip()):  # 如果elem.tail为空或者elem.tail只包含空格
#             elem.tail = i  # 将elem.tail设置为换行符+缩进符


class YouDao(object):
    """
    有道翻译
    """
    def __init__(self,trans_text,trans_lang,trans_name,trans_file_path,display_listbox,trans_model,input_text=None,trans_flag=None,single_new_path=None):
        # 获取用户输入的翻译参数
        self.q = trans_text
        self.origin_lang = 'zh-CHS'
        self.trans_lang = trans_lang
        self.app_name = trans_name
        self.trans_file_path = trans_file_path
        self.display_listbox = display_listbox
        self.trans_model = trans_model  # batch批量 single单个
        self.single_new_path = single_new_path  # 单个翻译的新文件路径
        self.input_text = input_text  # 单个翻译的输入框内容
        self.trans_flag = trans_flag  # 翻译标志

    def encrypt(self,signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self,data):
        # 获取有道翻译的接口地址
        youdao_id_key_all_list = youdao_id_key_all()
        YOUDAO_URL = youdao_id_key_all_list[0]
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL, data=data, headers=headers)

    def connect(self):
        # 获取有道翻译ID和KEY
        youdao_id_key_all_list = youdao_id_key_all()
        APP_KEY = youdao_id_key_all_list[1]
        APP_SECRET = youdao_id_key_all_list[2]

        data = {}
        data['from'] = self.origin_lang
        data['to'] = self.trans_lang
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + self.truncate(self.q) + salt + curtime + APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = self.q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = "您的用户词表ID"

        reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入

        response = self.do_request(data)
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            millis = int(round(time.time() * 1000))
            filePath = "合成的音频存储路径" + str(millis) + ".mp3"
            fo = open(filePath, 'wb')
            fo.write(response.content)
            fo.close()
        else:
            # print(response.content)
            translate = response.json()
            # print(translate)
            # print('翻译结果：',translate['translation'][0])
            translate_finally = f'<string name="{self.app_name}">{translate["translation"][0]}</string>'
            self.display_listbox.insert('end',f'{translate["translation"][0]}')
            if self.trans_model == 'batch':
                # 追加翻译结果到txt文件，以方便复制
                with open(trans_file_path+'\\'+self.trans_lang+'.txt','a',encoding='utf-8') as f:
                    f.write(translate_finally + '\n')
                print('最终翻译结果：',translate_finally)

                # 追加翻译结果到xml文件
                # tree = ElementTree.parse(self.trans_file_path)
                # root = tree.getroot()  # 获取根节点
                # element_tree = ElementTree.ElementTree(root)
                # name = Element("string", {"name": self.app_name})
                # name.text = translate['translation'][0]
                # root.append(name)
                # indent(root)  # 格式化xml文件
                # element_tree.write(self.trans_file_path,encoding='utf-8')

                if not os.path.exists(self.trans_file_path):
                    with open(self.trans_file_path, 'w', encoding='utf-8') as f:
                        f.write('<?xml version="1.0" encoding="utf-8"?>\r\n'
                                '<resources>\r\n')

                # 查看self.trans_file_path文件是否存在</resources>标签，如果存在则删除
                with open(self.trans_file_path,'r',encoding='utf-8') as f:
                    no_resources_line = f.read().replace('</resources>','')
                with open(self.trans_file_path,'w',encoding='utf-8') as f:
                    f.write(no_resources_line)

                # 首个追加注释到xml文件
                if self.trans_flag == 'first' or self.trans_flag == 'one':
                    if '<!--' in self.input_text:
                        # 获取input_text 输入框内容中的注释
                        trans_note = re.findall(r'<!--(.+?)-->',self.input_text,re.S)[0]
                        with open(self.trans_file_path,'a',encoding='utf-8') as f:
                            f.write(f'    <!--{trans_note}-->\n\n')

                # 追加翻译结果到xml文件
                with open(self.trans_file_path,'a',encoding='utf-8') as f:
                    f.write(f'    <string name="{self.app_name}">{translate["translation"][0]}</string>\n')

                # 末尾追加注释到xml文件
                if self.trans_flag == 'end' or self.trans_flag == 'one':
                    if '<!--' in self.input_text:
                        # 获取input_text 输入框内容中的注释
                        trans_note = re.findall(r'<!--(.+?)-->', self.input_text, re.S)[0]
                        with open(self.trans_file_path, 'a', encoding='utf-8') as f:
                            f.write(f'\n    <!--{trans_note}-->\n\n')

                # 最后添加</resources>标签
                with open(self.trans_file_path,'a',encoding='utf-8') as f:
                    f.write('</resources>')

            elif self.trans_model == 'single':
                # 翻译生成的xml文件路径
                new_xml_path = os.path.join(self.single_new_path,f'strings_{self.trans_lang}.xml')
                # 新建文件
                if not os.path.exists(new_xml_path):
                    with open(new_xml_path,'w',encoding='utf-8') as f:
                        f.write('<?xml version="1.0" encoding="utf-8"?>\r\n'
                                '<resources>\r\n')

                # 追加翻译结果到xml文件
                # tree = ElementTree.parse(new_xml_path)
                # root = tree.getroot()  # 获取根节点
                # element_tree = ElementTree.ElementTree(root)
                # name = Element("string", {"name": self.app_name})
                # name.text = translate['translation'][0]
                # root.append(name)
                # indent(root)  # 格式化xml文件
                # element_tree.write(new_xml_path,encoding='utf-8')

                # 查看self.trans_file_path文件是否存在</resources>标签，如果存在则删除
                with open(new_xml_path, 'r', encoding='utf-8') as f:
                    no_resources_line = f.read().replace('</resources>', '')
                with open(new_xml_path, 'w', encoding='utf-8') as f:
                    f.write(no_resources_line)

                # 追加翻译结果到xml文件
                with open(new_xml_path,'a',encoding='utf-8') as f:
                    f.write(f'    <string name="{self.app_name}">{translate["translation"][0]}</string>\n')

                # 最后添加</resources>标签
                with open(new_xml_path,'a',encoding='utf-8') as f:
                    f.write('</resources>')

            self.display_listbox.see(tk.END)



