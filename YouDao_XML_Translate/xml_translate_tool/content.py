#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from xml.etree import ElementTree as ElementTree


def get_trans_name(file_path,trans_lang,input_text):
    """
    获取需要翻译的name值列表
    file_path: 需要翻译的文件夹路径(例如res文件夹)
    trans_lang: 需要翻译的语言（例如de）
    input_text: 需要翻译的xml文本，如果有则只取这些内容的name值，否则就取values文件夹下的strings.xml中的name值
    :return: trans_name_list 需要翻译的name值列表 values_string_path 模板strings.xml文件路径 target_string_path 目标strings.xml文件路径
    """
    # 遍历文件夹下的所有文件
    file_path = file_path
    # 遍历当前含values的文件夹
    value_dirs = []
    for root, dirs, files in os.walk(file_path):
        if dirs:
            # 查找含values的文件夹
            value_dirs = [dir for dir in dirs if 'values' in dir]
            # print(value_dirs)

    # 遍历模板values文件夹下的所有文件，替换 \ 为 /，并找到strings.xml文件
    values_file = os.path.join(file_path, value_dirs[0])
    string_path = os.path.join(values_file, 'strings.xml')

    if input_text == '':
        # 读取strings.xml文件
        with open(string_path, 'r', encoding='utf-8') as f:
            # lines = f.readlines()
            # for line in lines:
            #     # 获取所有name值（模板），如果还有 translatable="false" 则不用获取当前的name值
            #     if 'name' in line and 'translatable="false"' not in line:
            #         # 正则表达式精准获取name，如果出现<!-- -->注释，则需要过滤掉注释的name
            #         if '<!--' not in line:
            #             try:
            #                 values_name = re.findall('<string name="(.*?)">.*?</string>', line)[0]
            #             except Exception:  # 出现异常则使用split方法获取name
            #                 values_name = line.split('name="')[1].split('"')[0]
            #             values_name_list.append(values_name)
            values_line = f.read()
            values_name_list = re.findall('<string name="(.*?)">.*?</string>', values_line, re.S)

        print('模板翻译文件name列表：',values_name_list)

    # 寻找需要翻译的目标文件夹中的strings.xml文件
    # print('获取的语言：',trans_lang)
    # 首先判断语言遍历的只有一个，超出一个则需要找到values-后面的语言进行相等判断
    trans_dir_name = [dir for dir in value_dirs if trans_lang in dir.split('-')[-1]]
    # print(trans_dir_name)
    if len(trans_dir_name) > 1:
        # 首先获取values后面的语言
        trans_name = [dir.split('-')[-1] for dir in value_dirs]  # 获取values后面的语言
        # 获取准确的目标文件夹，比如es这种语言，哪个文件夹名称都包含，需要作语言相等判断
        for i in trans_name:
            for j in trans_dir_name:
                if i == j.split('-')[-1]:  # 判断语言是否相等，一定要确保values后面的语言是唯一的
                    target_dir_path = os.path.join(file_path, j)
                    # print(target_dir_path)
    else:
        target_dir_path = os.path.join(file_path,[dir for dir in value_dirs if trans_lang in dir][0])
    target_string_path = os.path.join(target_dir_path, 'strings.xml')
    # print('获取全部的目标路径：',target_dir_path)

    # 读取目标strings.xml文件并获取name值，如果目标文件夹中没有strings.xml文件，则创建一个
    if not os.path.exists(target_string_path):
        with open(target_string_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\r\n'
                    '<resources>\r\n'
                    '</resources>')
    if input_text == '':
        # target_name_list = []
        with open(target_string_path, 'r', encoding='utf-8') as f:
            # lines = f.readlines()
            # for line in lines:
            #     # 如果有 translatable="false" 则不用获取当前的name值
            #     if 'name' in line and 'translatable="false"' not in line:
            #         # 正则表达式精准获取name，如果出现<!-- -->注释，则需要过滤掉注释的name
            #         if '<!--' not in line:
            #             try:
            #                 target_name = re.findall('<string name="(.*?)">.*?</string>', line)[0]  # 正则表达式精准获取name，同时过滤掉注释后的name
            #             except Exception: # 出现异常则使用split方法获取name
            #                 target_name = line.split('name="')[1].split('"')[0]
            #             target_name_list.append(target_name)
            lines = f.read()
            target_name_list = re.findall('<string name="(.*?)">.*?</string>', lines,re.S)

        # print('目标翻译文件name列表：',target_name_list)

        # 对比两个name值列表，找出需要翻译的name值（target_name_list没有的name值）
        trans_name_list = [i for i in values_name_list if i not in target_name_list]
        # print('需要翻译的name值：',trans_name_list)
    else:  # 如果有输入需要翻译的文本，则直接使用输入的文本进行翻译
        # print('需要翻译的源文本内容：',input_text)
        trans_name_list = re.findall('<string name="(.*?)">.*?</string>', input_text, re.S)
        # print('需要翻译的name值：',trans_name_list)

    # 最后过滤掉不需要翻译的name值，比如含有translatable="false的name值
    trans_name_list = [i for i in trans_name_list if 'translatable="false' not in i]
    print('最终得到需要翻译的name值：', trans_name_list)

    return {'trans_name_list': trans_name_list,'values_string_path': string_path,'target_string_path': target_string_path}


def get_trans_text(values_string_path,trans_name_list,input_text):
    """
    获取需要翻译的文本
    :param values_string_path: 模板strings.xml文件路径
    :param trans_name_list: 需要翻译的name值列表
    :param input_text: 输入的需要翻译的文本，如果存在则直接取输入的文本里的文本内容
    :return: trans_text_list 需要翻译的文本列表
    """
    target_file_path = values_string_path
    # trans_text_list = []  # 需要翻译的文本列表

    # tree = ElementTree.parse(target_file_path)  # 载入xml数据,使用ElementTree代表整个XML文档，Element代表这个文档树中的单个节点
    # # root = tree.getroot()  # 获取根节点
    # strings = tree.findall('string')  # 查找当前元素下匹配Element对象的直系节点
    # for string in strings:
    #     # print(string.text)
    #     names = string.get('name')  # 获取name属性值
    #     if names in trans_name_list:
    #         if string.text is None:  # 如果这个name值对应的文本为空，则需要使用打开文本直接提取对应的文本内容
    #             with open(target_file_path, 'r', encoding='utf-8') as f:
    #                 string_line = f.readlines()
    #                 # 获取当前names对应的文本内容
    #                 for line in string_line:
    #                     if names in line:
    #                         # 使用正则表达式匹配文本内容
    #                         try:
    #                             text = re.findall('<string name=".*?">(.*?)</string>',line)[0]  # 精准匹配文本内容
    #                             string.text = text
    #                         except Exception:  # 如果出现文本内容多行的情况，则需要使用split进行分割
    #                             string.text = line.split('>')[1].split('<')[0]
    #
    #         trans_text_list.append(string.text)

    trans_text_list = []
    if input_text == '':
        # 使用直接读取文本的方式获取文本内容
        with open(target_file_path, 'r', encoding='utf-8') as f:
            target_xml_line = f.read()
            # 根据name值列表获取需要翻译的文本
            for name in trans_name_list:
                trans_text = re.findall(f'<string name="{name}">(.*?)</string>',target_xml_line,re.S)  # 使用正则表达式获取文本内容
                # print('正则获取的trans_text:',trans_text)
                trans_text_list.append(trans_text[0])
    else:
        for name in trans_name_list:
            trans_text = re.findall(f'<string name="{name}">(.*?)</string>', input_text, re.S)
            trans_text_list.append(trans_text[0])

    print('获取需要翻译的文本：',trans_text_list)
    return trans_text_list





