"""
文件管理器相关操作
"""
# -*- coding:utf-8 -*-
import os
import time
from dogtail.tree import root
import pyperclip
import pyautogui
from function.uos_public_operation.config import CONFIG

pyautogui.FAILSAFE = False


class FileManager:
    """
    文件管理器相关操作
    """

    def __init__(self, file_path_directory):
        """

        :param file_path_directory: 需要打开的路径
        """
        os.system('killall dde-file-manager')
        # 替换路径中～符号
        if file_path_directory.find('~') != -1:
            home_path = os.popen('echo $HOME').read().strip()
            file_path_directory = file_path_directory.replace('~', home_path)

        if not os.path.exists(file_path_directory):
            raise Exception("文件路径错误")
        time.sleep(CONFIG.wait_time_tree)
        os.popen('nohup dde-file-manager ' + file_path_directory + ' > /dev/null 2>&1 &')
        time.sleep(CONFIG.wait_time_one)
        self.file_dogtail = root.application(appName="dde-file-manager", description="/usr/bin/dde-file-manager")

    def __del__(self):
        os.system('killall dde-file-manager')

    def search_file(self, file_name):
        """
        搜索文件
        :param file_name: 文件名
        :return: None
        """
        self.file_dogtail.clearCache()
        # 获取搜索按钮
        search_button = \
            self.file_dogtail.child('DMainWindowTitlebar', roleName='frame').children[5].children[0].children[
                1].children[1].children[1]
        pyautogui.click(
            search_button.queryComponent().obj.extents[0] + int(search_button.queryComponent().obj.extents[2] / 2),
            search_button.queryComponent().obj.extents[1] + int(search_button.size[1] / 2), button='left')
        time.sleep(CONFIG.wait_time_one)
        # 拷贝文件名至剪贴板
        pyperclip.copy(file_name)
        time.sleep(CONFIG.wait_time_one)
        # 粘贴至搜索框
        pyautogui.hotkey('ctrlleft', 'v')
        time.sleep(CONFIG.wait_time_one)
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)
        # 点击列表显示模式按钮
        list_button = \
            self.file_dogtail.child('DMainWindowTitlebar', roleName='frame').children[5].children[0].children[
                2].children[1]
        pyautogui.click(
            list_button.queryComponent().obj.extents[0] + int(list_button.queryComponent().obj.extents[2] / 2),
            list_button.queryComponent().obj.extents[1] + int(list_button.queryComponent().obj.extents[3] / 2),
            button='left')
        time.sleep(CONFIG.wait_time_one)

    def get_file_position(self, file_name):
        """
        获取文件坐标
        :param file_name: 文件名
        :return:(pos_x,pos_y) 文件坐标
        """
        # 搜索文件
        self.search_file(file_name)
        self.file_dogtail.clearCache()
        # 获取文件图标对象
        file = \
            self.file_dogtail.child(file_name, roleName='list item')
        time.sleep(CONFIG.wait_time_one)
        return (file.queryComponent().obj.extents[0] + int(file.queryComponent().obj.extents[2] / 2),
                file.queryComponent().obj.extents[1] + int(file.queryComponent().obj.extents[3] / 2))

    def click_file_right_menu(self, file_name, index):
        """
        点击文件右键菜单
        :param file_name:文件名
        :param index: int右键菜单定位下标，从1开始，自上而下
        :return:None
        """
        # 右键点击图标
        file_position = self.get_file_position(file_name)
        pyautogui.click(file_position[0], file_position[1], button='right')
        time.sleep(CONFIG.wait_time_one)
        # 选取菜单项
        for _ in range(0, index):
            pyautogui.press('down')
            time.sleep(CONFIG.wait_time_one)
        # 确定选项
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)

    def close_search_file(self):
        """
        搜索文件
        :return: None
        """
        self.file_dogtail.clearCache()
        search_button = \
            self.file_dogtail.child('AddressToolBar', roleName='text').children[1]
        pyautogui.click(
            search_button.queryComponent().obj.extents[0] + int(search_button.queryComponent().obj.extents[2] / 2),
            search_button.queryComponent().obj.extents[1] + int(search_button.size[1] / 2), button='left')
        time.sleep(CONFIG.wait_time_one)
