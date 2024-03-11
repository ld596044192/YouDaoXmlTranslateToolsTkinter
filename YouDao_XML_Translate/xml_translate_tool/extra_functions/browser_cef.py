#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 浏览器类

from cefpython3 import cefpython as cef  # 导入cefpython库

# Width and height of the main window  # 主窗口的宽度和高度
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class MainFrame:
    def __init__(self, url):
        self.url = url
        self.window_info = cef.WindowInfo()  # 创建一个窗口信息对象
        self.window_info.SetAsChild(0, [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT])  # 设置窗口信息对象
        self.browser = cef.CreateBrowserSync(self.window_info, url=self.url)  # 创建一个浏览器对象
        self.browser.SetClientHandler(LoadHandler())  # 设置浏览器对象的客户端处理程序

    def run(self):
        cef.MessageLoop()  # 进入消息循环

    def close_browser(self):
        self.browser.CloseBrowser()  # 关闭浏览器


class LoadHandler:
    def OnLoadingStateChange(self, browser, is_loading, **_):  # 当浏览器的加载状态发生变化时
        if not is_loading:  # 如果不在加载
            print("Page done loading")  # 打印加载完成
        else:
            print("Page loading...")

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):  # 当浏览器加载错误时
        print(f"Load error: {error_text_out}")  # 打印错误信息


def cef_main(url):
    try:
        cef.Initialize()  # 初始化
        print("CEF initialized successfully")
        frame = MainFrame(url)  # 创建一个浏览器对象
        frame.run()  # 进入消息循环
        frame.close_browser()  # 关闭浏览器
    except Exception as e:
        print("Error initializing CEF:", e)
    finally:
        print("Shutting down CEF")
        cef.Shutdown()  # 关闭
        cef.MessageLoopWork()  # 退出消息循环

