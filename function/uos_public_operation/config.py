"""
lib库相关配置文件
"""
# -*- coding:utf-8 -*-
import os


class _Config():
    def __init__(self):
        self.wait_time_one = 0.6
        self.wait_time_two = 0.8
        self.wait_time_tree = 0.9
        self.wait_time_four = 1.5
        self.wait_time_five = 2.5
        self.wait_time_six = 3.5
        self.max_wait_time = 30

    def add_path(self, path):
        """
        天加路径缓存
        :param path: 搜索的关键字
        :return:True 搜索成功or搜索失败
        """
        command = 'dbus-send --system --print-reply --dest=com.deepin.anything /com/deepin/anything ' \
                  'com.deepin.anything.addPath string:"' + path + '"'
        content = os.popen(command).read().strip().split(' ')
        if content:
            return content[-1]
        return None


CONFIG = _Config()
