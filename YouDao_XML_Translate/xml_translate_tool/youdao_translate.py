#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time,os
import tkinter as tk

import requests.exceptions
import urllib3

import content,getpass
import youdao_demo

# 翻译主流程
doc_path = os.path.join(os.path.expanduser("~"), 'Documents')
trans_file_path = doc_path + 'xml_youdao_tool'
if not os.path.exists(trans_file_path):
    os.makedirs(trans_file_path)


class Context:
    pass  # 空类，用于存储全局变量


def get_trans_lang(file_path):
    # 获取翻译语言
    trans_lang_list = []
    for root, dirs, files in os.walk(file_path):
        if dirs:
            # 查找含values-的文件夹
            values_dir = [dir for dir in dirs if 'values-' in dir]
            # 取出values-后面的语言
            for dir_name in values_dir:
                try:
                    if dir_name.split('-')[2]:
                        trans_lang_list.append(dir_name.split('-')[1] + '-' + dir_name.split('-')[2])
                except Exception as e:
                    trans_lang_list.append(dir_name.split('-')[1])

    # print('最终获取的翻译语言列表：',trans_lang_list)
    return trans_lang_list


class TranslateMain(object):
    def __init__(self):
        pass

    def translate_params(self,trans_lang,file_path,display_listbox,stop_event,trans_lock,input_text):
        # 获取翻译参数
        if not get_trans_lang(file_path):
            print('该文件夹下无需翻译！！！')
        else:
            trans_name_dict = content.get_trans_name(file_path,trans_lang,input_text)
            # print('获取的参数',trans_name_dict)
            trans_text_list = content.get_trans_text(trans_name_dict['values_string_path'],trans_name_dict['trans_name_list'],input_text)
            if not trans_name_dict or not trans_name_dict:
                print(f'该 {trans_lang} 语言无需翻译！！！')
            else:
                if trans_lang == 'zh-rTW':  # 台湾繁体中文修改为有道翻译支持的繁体语言
                    trans_lang = 'zh-CHT'
                if trans_lang == 'ar-rAE':  # 阿拉伯语修改为有道翻译支持的阿拉伯语言
                    trans_lang = 'ar'

                for trans_name,trans_text in zip(trans_name_dict['trans_name_list'],trans_text_list):
                    if stop_event.is_set():
                        print("Stop event is set, exiting thread")  # 停止有道翻译接口中的线程
                        return

                    if len(trans_name_dict['trans_name_list']) == 1:
                        trans_flag = 'one'  # 表示只有一个翻译的内容
                    else:
                        if trans_name == trans_name_dict['trans_name_list'][0]:  # 判断是否为第一个翻译的内容
                            trans_flag = 'first'
                        if trans_name == trans_name_dict['trans_name_list'][-1]:  # 判断是否为最后一个翻译的内容
                            trans_flag = 'end'

                    # print('翻译注释标志：',trans_flag)

                    try:
                        youdao = youdao_demo.YouDao(trans_text,trans_lang,trans_name,trans_name_dict['target_string_path'],
                                                display_listbox,'batch',input_text=input_text,trans_flag=trans_flag)  # batch表示批量翻译
                        youdao.connect()
                        time.sleep(1)
                    except (ConnectionResetError,urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError) as e:
                        print(e)
                        display_listbox.insert(tk.END,'翻译接口连接失败，请重新翻译！！！')
                        break

                    # 重置翻译标志
                    trans_flag = ''

                    if getattr(Context,'stop_event_flag'):
                        trans_lock.acquire()  # 获取锁


