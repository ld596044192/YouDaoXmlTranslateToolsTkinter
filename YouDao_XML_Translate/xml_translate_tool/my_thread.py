# !/usr/bin/python
# -*- coding:utf-8 -*-

# 定义一个线程类，用于控制线程的启动和停止
import threading


class MyThread(threading.Thread):
    def __init__(self, func):
        super().__init__()
        self.stop_event = threading.Event()  # 用于停止线程的标识
        self.func = func  # 传入线程函数逻辑
        self.stopped = False  # 线程停止标识，用于线程停止后的清理工作
        self.t_thread = threading.Thread(target=self.my_thread)  # 创建线程

    def my_thread(self):
        # try:
        self.func(self.stop_event)  # 调用线程函数
        # except Exception as e:
        #     print(f"Thread exception: {e}")

    def start(self):
        self.t_thread.start()  # 启动线程

    def stop(self):
        print('已调用停止线程函数')
        self.stop_event.set()  # 设置停止线程标识
        self.t_thread.join(0)  # 0表示立即返回，不等待线程结束
        self.stopped = True

    def restart(self):
        # 重启线程
        if self.stopped:
            self.stop_event.clear()  # 清除停止线程标识
            self.t_thread = threading.Thread(target=self.my_thread)
            self.t_thread.start()
            self.stopped = False  # 重置线程停止标识

