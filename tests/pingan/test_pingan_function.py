# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
pingan test
"""

import os
import subprocess
import time

import pyautogui

from function.get_image import wait_for_img, get_image_path2, IMAGE_FOLDER_WPS, IMAGE_FOLDER_PINGAN, drag_img
from function.screen_actions import match_and_click, move_mouse_to_center_of_screen

home = os.popen('echo /home/$(getent passwd `who` | head -n 1 | cut -d : -f 1)').read().strip()


def setup():
    # 应用的命令行 可以从系统监视器该应用的属性中获取
    subprocess.Popen('', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')
    # 判断应用是否开启
    assert wait_for_img(get_image_path2(IMAGE_FOLDER_PINGAN) + '', max_wait_time=5) is not None


def teardown():
    # 关闭应用
    os.popen('killall -9 应用')


def test_pingan_function():
    """
    :return:
    """
    # 左击,需要右击就修改此方法的click_action参数
    match_and_click(get_image_path2(IMAGE_FOLDER_PINGAN), '')

    # 输入内容
    pyautogui.typewrite('')

    # 复制粘贴
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('right')
    pyautogui.hotkey('ctrl', 'v')

    # 截图
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(3)
    pyautogui.hotkey('enter')
    match_and_click(get_image_path2(IMAGE_FOLDER_PINGAN), 'wps_7.png')
    assert wait_for_img(get_image_path2(IMAGE_FOLDER_PINGAN) + '/') is not None

    # 拖拽
    drag_img(get_image_path2(IMAGE_FOLDER_PINGAN) + '/', 0, 0)