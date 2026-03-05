"""
对话框相关操作
"""
# -*- coding:utf-8 -*-
import time
import os
from dogtail.tree import root
from dogtail.config import config
import pyautogui
from function.uos_public_operation.config import CONFIG
config.defaults['childrenLimit'] = 1000
pyautogui.FAILSAFE = False


class Dialog:
    """
    弹出的对话框相关操作,要求在对话框弹出前构造
    """

    def __init__(self):
        self.desktop_dogtail = root.application(appName="dde-desktop", description="/usr/bin/dde-desktop")
        self.kill_all_dialog()

    def absolute_path(self, file_path):
        """
        替换路径中～为绝对路径
        :param file_path: 待搜索文件路径
        :return:文件绝对路径,文件所在目录，文件名
        """
        file_path = file_path.replace('~/', os.environ['HOME'] + "/")
        file_path = os.path.abspath(file_path)
        file_path_directory = ''
        file_name = ''
        # 获取文件路径和文件名

        file_path_directory, file_name = os.path.split(file_path)
        if not os.path.exists(file_path):
            file_path = ''
            file_name = ''
            file_path_directory = ''
            raise Exception('文件路径非法！')
        return file_path, file_path_directory, file_name

    def get_file_position(self, file_path):
        """
        获取文件坐标
        :param file_path: 待搜索文件全路径
        :return:(pos_x,pos_y) 文件坐标
        """
        file_path, file_path_directory, file_name = self.absolute_path(file_path)
        # 搜索文件
        # self.search_file(file_path)
        self.open_file_folder(file_path_directory)
        # 获取文件图标对象
        # self.refresh_main_window_node()
        self.desktop_dogtail = root.application(appName="dde-desktop", description="/usr/bin/dde-desktop")
        file = self.desktop_dogtail.child(file_name, roleName='list item')
        i = 0
        while file is None:
            if i >= 5:
                break
            i += 1
            time.sleep(CONFIG.wait_time_tree)
            self.desktop_dogtail = root.application(appName="dde-desktop", description="/usr/bin/dde-desktop")
            file = self.desktop_dogtail.child(file_name, roleName='list item')

        time.sleep(CONFIG.wait_time_one)
        return file.position[0] + int(file.size[0] / 2), file.position[1] + int(file.size[1] / 2)

    def click_file_right_menu(self, file_path, index):
        """
        点击文件右键菜单
        :param file_path: 待搜索文件全路径
        :param index: int右键菜单定位下标，从1开始，自上而下
        :return:None
        """
        file_path = self.absolute_path(file_path)[0]
        # 右键点击图标
        file_position = self.get_file_position(file_path)
        pyautogui.click(file_position[0], file_position[1], button='right')
        time.sleep(CONFIG.wait_time_one)
        # 选取菜单项
        for _ in range(0, index):
            pyautogui.press('down')
            time.sleep(CONFIG.wait_time_one)
        # 确定选项
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)

    def open_file_name(self, file_path):
        """
        打开文件夹，点击打开
        param file_path: 待搜索文件全路径
        """
        file_path, file_name = self.absolute_path(file_path)[0], self.absolute_path(file_path)[2]
        self.open_file_folder(file_path)
        object_path = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog '
                               '/com/deepin/filemanager/filedialogmanager com.deepin.filemanager.filedialogmanager.dialogs | grep '
                               'object | tr -s [:space:] | cut -d " " -f 4').read().strip().replace("\"", "").split('\n')
        for _, elementin in enumerate(object_path):
            os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.selectFile string:"' + file_name + '"')
            time.sleep(0.5)
            result = os.popen(
                'dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.selectedFiles | grep '
                                                                                                            'string | tr -s [:space:] | cut -d " " -f 3').read().strip()
            if result != '':
                os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.accept')
            else:
                os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.reject')
        time.sleep(1)

    def open_file_folder(self, file_path):
        """
        只打开文件夹文件
        param file_path: 待搜索文件全路径
        """
        file_path, file_path_directory = self.absolute_path(file_path)[0:2]
        object_path = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog '
                               '/com/deepin/filemanager/filedialogmanager com.deepin.filemanager.filedialogmanager.dialogs | grep '
                               'object | tr -s [:space:] | cut -d " " -f 4').read().strip().replace("\"", "").split('\n')
        for _, elementin in enumerate(object_path):
            if os.path.isdir(file_path):
                os.system(
                    'dbus-send --session --print-reply --dest=org.freedesktop.FileManager1 ' + elementin + " org.freedesktop.DBus.Properties.Set string:'com.deepin.filemanager.filedialog' string:'directory' variant:string:'" + file_path + "'")
            else:
                os.system(
                    'dbus-send --session --print-reply --dest=org.freedesktop.FileManager1 ' + elementin + " org.freedesktop.DBus.Properties.Set string:'com.deepin.filemanager.filedialog' string:'directory' variant:string:'" + file_path_directory + "'")
            os.system(
                'dbus-send --session --print-reply --dest=org.freedesktop.FileManager1 ' + elementin + " org.freedesktop.DBus.Properties.Set string:'com.deepin.filemanager.filedialog' string:'viewMode' variant:int32:0")
        time.sleep(1)

    def choose_file(self):
        """
        归档选择文件夹后点击右下角打开

        """
        object_path = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog '
                               '/com/deepin/filemanager/filedialogmanager com.deepin.filemanager.filedialogmanager.dialogs | grep '
                               'object | tr -s [:space:] | cut -d " " -f 4').read().strip().replace("\"", "").split('\n')
        for _, elementin in enumerate(object_path):
            result = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.selectedFiles | grep '
                                                                                                                          'string | tr -s [:space:] | cut -d " " -f 3').read().strip()
            if result != '':
                os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.accept')
            else:
                os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.reject')
        time.sleep(1)

    def cancle_open_file(self):
        """
        取消打开文件夹

        """
        object_path = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog '
                               '/com/deepin/filemanager/filedialogmanager com.deepin.filemanager.filedialogmanager.dialogs | grep '
                               'object | tr -s [:space:] | cut -d " " -f 4').read().strip().replace("\"", "").split('\n')
        for _, elementin in enumerate(object_path):
            os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.reject')
        time.sleep(1)

    def kill_all_dialog(self):
        """
        关闭所有对话框
        """
        object_path = os.popen('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog '
                               '/com/deepin/filemanager/filedialogmanager com.deepin.filemanager.filedialogmanager.dialogs | grep '
                               'object | tr -s [:space:] | cut -d " " -f 4').read().strip().replace("\"", "").split('\n')
        for _, elementin in enumerate(object_path):
            os.system('dbus-send --session --print-reply --dest=com.deepin.filemanager.filedialog ' + elementin + ' com.deepin.filemanager.filedialog.deleteLater')
        time.sleep(1)
