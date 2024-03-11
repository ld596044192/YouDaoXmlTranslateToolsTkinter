#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 浏览器类
import sys
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QSystemTrayIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class Context:
    pass


class BrowserWindow(QMainWindow):
    def __init__(self,title):
        super().__init__()
        self.title = title
        self.init_ui()

    def init_ui(self):
        # Create the web view and add it to the central widget
        self.web_view = QWebEngineView(self)  # 创建浏览器
        setattr(Context,'self',self)  # 将浏览器对象添加到上下文中

        # 设置窗口标题
        self.setWindowTitle(self.title)  # 设置窗口标题
        self.setCentralWidget(self.web_view)  # 设置窗口中心部件

        # Create the navigation bar and add it to the window
        # 创建按钮并添加到导航栏
        nav_bar = QToolBar()  # 创建导航栏
        self.addToolBar(nav_bar)  # 添加导航栏到窗口
        mt_push_button = QPushButton("蒙恬扫描push测试")  # 创建按钮
        mt_push_button.clicked.connect(self.load_mt_push)  # 绑定按钮点击事件
        nav_bar.addWidget(mt_push_button)  # 添加按钮到导航栏

        merge_xml_button = QPushButton("合并多语言的多语言XML文件工具")
        merge_xml_button.clicked.connect(self.load_merge_xml)
        nav_bar.addWidget(merge_xml_button)

        xml_excel_button = QPushButton("XML文件转execl文件和execl文件转XML文件工具")
        xml_excel_button.clicked.connect(self.load_xml_excel)
        nav_bar.addWidget(xml_excel_button)

        xml_translate_button = QPushButton("XML文件翻译工具")
        xml_translate_button.clicked.connect(self.load_xml_translate)
        nav_bar.addWidget(xml_translate_button)

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)  # 创建托盘图标
        self.tray_icon.setIcon(QIcon('icon/my-da.ico'))  # 设置托盘图标
        self.tray_icon.setToolTip('Da Browser')  # 设置托盘图标提示
        self.tray_icon.activated.connect(self.on_tray_icon_activated)  # 绑定托盘图标点击事件

        self.resize(1024, 768)  # 设置窗口大小

    def load_mt_push(self):
        try:
            self.web_view.load(QUrl('https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/蒙恬扫描push测试.html'))
            self.title = '蒙恬扫描push测试窗口'
        except Exception as e:
            print("Error loading mt_push:", e)

    def load_merge_xml(self):
        try:
            self.web_view.load(QUrl('https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/languageXMLmerge.html'))
        except Exception as e:
            print("Error loading merge_xml:", e)

    def load_xml_excel(self):
        try:
            self.web_view.load(QUrl('https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/XmlchangeExecl.html'))
        except Exception as e:
            print("Error loading xml_excel:", e)

    def load_xml_translate(self):
        try:
            self.web_view.load(QUrl('https://down.dosmono.com/commons/libs/static/dosmono/DosmonoAllUtils/otherTest/test/XMLtranslateXML.html'))
        except Exception as e:
            print("Error loading xml_translate:", e)

    def closeEvent(self, event):
        # 重新实现closeEvent方法，点击关闭按钮时处理事件
        print("关闭浏览器")
        self.hide()  # 隐藏窗口
        event.ignore()  # 忽略关闭事件，阻止程序退出

        # try:
        #     self.web_view.deleteLater()  # 删除浏览器
        # except Exception as e:
        #     print(e)

        self.tray_icon.show()  # 显示托盘图标

        # Show a message to let the user know the program is still running
        # 显示一条消息让用户知道程序仍在运行
        # self.tray_icon.showMessage(
        #     'My Browser',  # 标题
        #     'My Browser has been minimized to the tray.',  # 内容
        #     QSystemTrayIcon.Information,  # 消息类型
        #     2000  # 消息持续时间
        # )

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # 单击托盘图标
            print("触发 单击托盘图标 事件")
            self.showNormal()  # 显示窗口
            print('self.showNormal() Finished')
            self.raise_()  # 置顶窗口
            self.activateWindow()  # 激活窗口
            print('self.activateWindow() Finished')


def show_browser_tray():
    getattr(Context,'self').tray_icon.activated.emit(QSystemTrayIcon.Trigger)  # 触发托盘图标点击事件


def browser_main():
    # 创建线程
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)  # 禁止应用程序自动退出
    browser = BrowserWindow('DosmonoAllUtils')
    browser.show()

    app.exec_()

